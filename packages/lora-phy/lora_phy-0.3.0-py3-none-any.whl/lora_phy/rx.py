import logging
from typing import cast

import numpy as np
import scipy.signal  # type: ignore[import-untyped]
from numpy.typing import NDArray

from .common import calc_checksum, calc_crc, calc_sym_num, chirp, dewhiten
from .errors import InvalidCodingRateError, NoPreambleError, NoSyncError
from .typing import Array1D, ComplexOrReal, cast1D, concat1D, slice1D

log = logging.getLogger(__name__)


class LoRaReceiver:
    """LoRa PHY layer implementation.

    Parameters
    ----------
    rf_freq : float
        Carrier frequency (useful for dynamic compensation).
    spreading_factor : int
        Spreading factor.
    bandwidth : float
        LoRa bandwidth parameter.
    sample_rate : float
        Sampling rate of the signal.
    has_header : bool
        Whether the packet has a header (False for implicit header mode).
    implicit_header_payload_len : int
        Payload length.
        This is only used in implicit header mode.
    coding_rate : int
        Coding rate (1:4/5 2:4/6 3:4/7 4:4/8).
        This is only used in implicit header mode.
    enable_crc : bool
        Whether to enable CRC checking.
        This is only used in implicit header mode.
    preamble_len : int
        Number of preamble chirps.
    resample_to_2x : bool
        Whether to resample to 2x bandwidth.
        It simplifies processing by reducing the number of samples to process.
        It also mimics the original MATLAB implementation and seems to be
        more reliable.
    """

    def __init__(
        self,
        rf_freq: float,
        spreading_factor: int,
        bandwidth: float,
        sample_rate: float,
        *,
        has_header: bool = True,
        implicit_header_payload_len: int = 0,
        implicit_header_coding_rate: int = 4,
        implicit_header_enable_crc: bool = True,
        preamble_len: int = 6,
        resample_to_2x: bool = True,
    ):
        # Carrier frequency
        self._spreading_factor = spreading_factor
        self._bandwidth = bandwidth
        self._sample_rate = sample_rate
        self._has_header = has_header
        self._zero_padding_ratio = 10
        self._preamble_len = preamble_len
        self._fast_mode = False
        # `is_debug` is handled by logging in Python
        # The original MATLAB implementation has a separate function `init`
        # that calculates `bin_num`, `sample_num`, `fft_len`, chirps, and
        # `low_data_rate_optimization`. `init` is called again in `demodulate`
        # and (unused) `symbols_to_bytes`.
        # The calculations are dependent on `spreading_factor`, `bandwidth`,
        # `zero_padding_ratio`, which are stable (set once in the constructor),
        # and `cfo` (taken out), which always gets set to 0 before calling
        # `init` in `demodulate`. Therefore, there is really no reason to
        # regenerate these values every time `demodulate` is called.
        if resample_to_2x:
            self._sample_num = 2 * 2 ** spreading_factor
        else:
            sample_num: float = 2 ** spreading_factor * sample_rate / bandwidth
            if not sample_num.is_integer():
                log.warning("Sample rate is not an integer multiple of bandwidth.")
            self._sample_num = round(sample_num)
        self._bin_num: int = 2 ** spreading_factor * self._zero_padding_ratio
        self._fft_len = self._sample_num * self._zero_padding_ratio
        self._resample_to_2x = resample_to_2x
        if resample_to_2x:
            self._down_chirp = chirp(
                False, self._spreading_factor, self._bandwidth, 2 * self._bandwidth)
            self._up_chirp = chirp(
                True, self._spreading_factor, self._bandwidth, 2 * self._bandwidth)
        else:
            self._down_chirp = chirp(
                False, self._spreading_factor, self._bandwidth, self._sample_rate)
            self._up_chirp = chirp(
                True, self._spreading_factor, self._bandwidth, self._sample_rate)
        # These are effective only in implicit header mode
        self._implicit_header_payload_len = implicit_header_payload_len
        self._implicit_header_coding_rate = implicit_header_coding_rate
        self._implicit_header_enable_crc = implicit_header_enable_crc
        # Low Data Rate Optimization: if the chirp period is larger than 16ms,
        # then the least significant two bits are considered unreliable.
        low_data_rate_optimization: bool = (
            2 ** self._spreading_factor / self._bandwidth > 16e-3)
        self._proc = RxProcessing(
            rf_freq,
            spreading_factor,
            hamming_decoding_en=True,
            low_data_rate_optimization=low_data_rate_optimization,
        )

    def demodulate(self, signal_: NDArray[ComplexOrReal]) -> tuple[
        list[Array1D[np.uint16]], list[float], list[tuple[float, float]]
    ]:
        """Demodulate the signal.

        Parameters
        ----------
        signal_ : NDArray[np.complex_]
            Baseband complex IQ signal (must be one dimensional).

        Returns
        -------
        symbols : list[Array1D[np.uint16]]
             List of demodulated symbols in each packet.
        cfo : list[float]
            Calculated CFO for each packet.
        netid : list[tuple[float, float]]
            Calculated NetID for each packet.
        """
        signal = cast1D(signal_)
        if not self._fast_mode:
            signal = self.lowpass(signal)
        if self._resample_to_2x:
            signal = cast1D(scipy.signal.resample_poly(signal, 2 * self._bandwidth, self._sample_rate))
        symbols_l: list[Array1D[np.uint16]] = []
        cfo_l: list[float] = []
        netid: list[tuple[float, float]] = []
        start = 0
        while start < len(signal):
            try:
                start = self._detect(signal, start)
            except NoPreambleError:
                break
            log.debug(f"Detected preamble at {start}.")

            # Align symbols with SFD
            (start, preamble_bin, cfo) = self._sync(signal, start)
            log.debug(f"Aligned symbols at {start} with preamble bin {preamble_bin} and CFO {cfo}.")

            # NetID
            (_, netid1) = self._dechirp(
                signal, round(start - 4.25 * self._sample_num))
            (_, netid2) = self._dechirp(
                signal, round(start - 3.25 * self._sample_num))
            netid1 = self._peak_idx_to_symbol(netid1, preamble_bin)
            netid2 = self._peak_idx_to_symbol(netid2, preamble_bin)
            # Storage is delayed to the end of the loop,
            # so that skipped packets do not affect the output

            # The goal is to extract `payload_len` from the PHY header
            # The header is in the first 8 symbols
            header_symbols = np.empty(8, dtype=np.uint16)
            # This one seems to be dead code in the original MATLAB implementation
            # pk_list = []
            if start > len(signal) - self._sample_num * 8:
                log.warning("Samples ended before full header.")
                break
            for i in range(8):
                pk = self._dechirp(signal, start + i * self._sample_num)
                # pk_list.append(pk)
                header_symbols[i] = self._peak_idx_to_symbol(
                    pk[1], preamble_bin)
            if self._has_header:
                (valid, payload_len, coding_rate,
                 has_crc) = self._parse_header(header_symbols)
                if not valid:
                    log.warning("Invalid header detected. Skipping this header.")
                    start += 7 * self._sample_num
                    continue
            else:
                payload_len = self._implicit_header_payload_len
                coding_rate = self._implicit_header_coding_rate
                has_crc = self._implicit_header_enable_crc
            # Number of symbols in the packet
            sym_num = calc_sym_num(
                self._has_header,
                payload_len,
                coding_rate,
                has_crc,
                self._spreading_factor,
                self._proc.low_data_rate_optimization,
            )
            symbols = np.empty(sym_num, dtype=np.uint16)
            symbols[:8] = header_symbols
            # Demodulate the rest of the packet
            if start > len(signal) - sym_num * self._sample_num:
                log.warning("Samples ended before full packet.")
                # will be handled inside `_dechirp`
            for i in range(8, sym_num):
                pk = self._dechirp(signal, start + i * self._sample_num)
                # pk_list.append(pk)
                symbols[i] = self._peak_idx_to_symbol(pk[1], preamble_bin)
            start += sym_num * self._sample_num
            log.debug(f"Packet finished at {start}.")
            # Compensate CFO drift
            symbols = self._proc.dynamic_compensation(
                symbols, cfo).astype(np.uint16)
            symbols_l.append(symbols)
            netid.append((netid1, netid2))
            cfo_l.append(cfo)
        if not symbols_l:
            raise NoPreambleError()
        return (symbols_l, cfo_l, netid)

    def demodulate_file(self, filename: str) -> tuple[list[Array1D[np.uint16]], list[float], list[tuple[float, float]]]:
        """Demodulate the signal stored in a file as complex64 IQ samples (see `demodulate`).

        Parameters
        ----------
        filename : str
            The filename of the file to read.

        Returns
        -------
        tuple[list[Array1D[np.uint16]], list[float], list[tuple[float, float]]]
            See `demodulate`.
        """
        signal = np.fromfile(filename, dtype=np.complex64)
        return self.demodulate(cast1D(signal))

    def decode(self, symbols_: NDArray[np.uint16]) -> tuple[Array1D[np.uint8], tuple[np.uint8, np.uint8] | None]:
        """Decode the symbols.

        Parameters
        ----------
        symbols_ : NDArray[np.uint16]
            The symbols to decode (must be one dimensional).

        Returns
        -------
        data : Array1D[np.uint8]
            The decoded data. The last `len(checksum)` bytes are the expected
            CRC16 checksum.
        checksum : tuple[np.uint8, np.uint8] | None
            Actual calculated CRC16 checksum (two bytes or empty).
        """
        symbols = cast1D(symbols_)
        symbols_g = self._proc.gray_coding(symbols.astype(np.float64))
        codewords = diag_deinterleave(
            slice1D(symbols_g, slice(0, 8)), self._spreading_factor - 2)
        # I have no idea why the MATLAB code is so redundant here
        # Header uses CR 4/8
        nibbles = self._proc.hamming_decode(codewords, 4 + 4)
        if self._has_header:
            # Parse header
            (valid, payload_len, cr,
             crc) = self._parse_header_inner(slice1D(nibbles, slice(0, 5)))
            if not valid:
                log.warning("Invalid header detected while decoding.")
            nibbles = slice1D(nibbles, slice(5, None))
        else:
            payload_len = self._implicit_header_payload_len
            crc = self._implicit_header_enable_crc
            cr = self._implicit_header_coding_rate
        # Number of bits with redundancy
        # For example, CR 4/5 means rdd = 5
        rdd = cr + 4
        for i in range(8, len(symbols_g) - rdd + 1, rdd):
            ppm = self._spreading_factor
            if self._proc.low_data_rate_optimization:
                ppm -= 2
            codewords = diag_deinterleave(
                slice1D(symbols_g, slice(i, i + rdd)), ppm)
            # Hamming decode
            nibbles = concat1D(
                (nibbles, self._proc.hamming_decode(codewords, rdd)))
        if len(nibbles) % 2 == 1:
            nibbles = concat1D((nibbles, [np.uint8(0)]))
        # Combine nibbles into bytes
        data_len = len(nibbles) // 2
        if data_len > 255 + 2:
            # 255 is the maximum payload length and 2 is CRC
            log.warning("Payload longer than 255 bytes.")
        data = np.zeros(data_len, dtype=np.uint8)
        for n, byte in enumerate(nibbles.reshape(-1, 2)):
            data[n] = byte[1] << 4 | byte[0]
        # Dewhitening
        if crc:
            # The last two bytes are CRC16 checksum
            just_data = slice1D(data, slice(0, payload_len))
            dewhiten(just_data)
            checksum = calc_crc(just_data)
            # Now concatenation is not necessary because `just_data` is still
            # a view into `data`
            # data = concat1D((just_data, data[payload_len:payload_len+2]))
            return slice1D(data, slice(0, payload_len+2)), checksum
        dewhiten(data)
        return data, None

    def lowpass(self, signal: Array1D[ComplexOrReal]) -> Array1D[ComplexOrReal]:
        """Low-pass filter the signal to the bandwidth.

        Parameters
        ----------
        signal : Array1D
            The signal to filter.

        Returns
        -------
        Array1D
            The filtered signal.
        """
        # These parameters are not equivalent to the MATLAB version
        sos = scipy.signal.butter(
            10, self._bandwidth/2,
            fs=self._sample_rate, btype="low",
            output="sos",
            analog=False)
        return cast(Array1D[ComplexOrReal], scipy.signal.sosfilt(sos, signal))

    def _peak_idx_to_symbol(self, peak_idx: int, preamble_bin: int) -> int:
        """Convert peak index to symbol.

        This helper was not present in the original MATLAB code.
        Parameters
        ----------
        peak_idx : int
            Peak bin (as returned by `_dechirp`).
        preamble_bin : int
            Preamble reference bin in current decoding window (as returned by `_sync`).

        Returns
        -------
        int
            The symbol.
        """
        normalized_peak = peak_idx + self._bin_num - preamble_bin
        sym: float = normalized_peak / \
            self._zero_padding_ratio % (2**self._spreading_factor)
        return round(sym)

    def _dechirp(self, signal: NDArray[ComplexOrReal], x: int, is_up: bool = True) -> tuple[float, int]:
        """Apply dechirping on the symbol starting at index `x`.

        Parameters
        ----------
        signal : NDArray
            The signal to dechirp.
        x : int
            The starting index of the symbol (C-style index)
        is_up : bool
            `True` to apply up-chirp dechirping, `False` for down-chirp.

        Returns
        -------
        height : float
            The height of the peak (FFT magnitude).
        index : int
            The index of the peak (one less than MATLAB).
        """
        if is_up:
            chp = self._down_chirp
        else:
            chp = self._up_chirp
        to_use = signal[x:x + self._sample_num]
        signal_len = len(to_use)
        prod = to_use * chp[:signal_len]
        ft = np.fft.fft(prod, self._fft_len)
        r1 = ft[:self._bin_num]
        r2 = ft[self._fft_len-self._bin_num:self._fft_len]
        absft = np.abs(r1) + np.abs(r2)
        # The original MATLAB implements the rest as a separate function
        # `topn`, which is more general but only ever used here.
        # return _topn(absft[:self._bin_num], 1)
        # Excessive copying and abs removed: sort descending in-place
        # This implements [y, p] = sort(abs(ft_(:, 1)), 'descend'), except
        # that p uses C-style indexing
        # This is ascending sort
        p = np.argsort(absft)
        best = p[-1]
        # Was min(n, size(absft, 1)) in MATLAB where n = 1.
        # Actually always 1 for this function.
        # nn = min(1, self._bin_num)
        # The original MATLAB implementation horzcats an index array to find
        # the index. I find that unnecessary.
        return (float(absft[best]), best)

    def _detect(self, signal: Array1D[ComplexOrReal], start: int) -> int:
        """Detect preamble.

        Parameters
        ----------
        signal : Array1D[ComplexOrReal]
            The signal to detect preamble from.
        start : int
            Starting index.

        Returns
        -------
        int
            Preamble detected before this index.

        Raises
        ------
        NoPreambleError
            If no preamble is detected.
        """
        # Preamble peak bin list
        pk_bin_list: list[int] = []
        while start < len(signal) - self._sample_num * self._preamble_len - 1:
            if len(pk_bin_list) == self._preamble_len - 1:
                # Preamble detected
                # Coarse alignment: first shift the up peak to position 0
                # Current sampling frequency is 2 * bandwidth
                # XXX: magic?
                return start - round(pk_bin_list[-1] / self._zero_padding_ratio * 2)
            (_, pk0) = self._dechirp(signal, start)
            if pk_bin_list:
                bin_diff = (pk_bin_list[-1] - pk0) % self._bin_num
                if bin_diff > self._bin_num // 2:
                    bin_diff = self._bin_num - bin_diff
                if bin_diff <= self._zero_padding_ratio:
                    pk_bin_list.append(pk0)
                else:
                    pk_bin_list = [pk0]
            else:
                pk_bin_list = [pk0]
            start += self._sample_num
        raise NoPreambleError()

    def _sync(self, signal: Array1D[ComplexOrReal], start: int) -> tuple[int, int, float]:
        """Synchronize packet by the downchirp.

        Parameters
        ----------
        signal : Array1D
            The signal to synchronize.
        start : int
            Starting index.

        Returns
        -------
        new_start : int
            Index after up-down alignment.
        preamble_bin : int
            Preamble reference bin (index as returned by `_dechirp`) in
            current decoding window (for CFO elimination).
        cfo : float
            Detected carrier frequency offset.
        """
        # This loop logic is much cleaner in Python than in MATLAB
        while start < len(signal) - self._sample_num:
            (pku, _) = self._dechirp(signal, start)
            (pkd, _) = self._dechirp(signal, start, False)
            start += self._sample_num
            if abs(pkd) > abs(pku):
                # Downchirp detected
                break
        else:
            raise NoSyncError()
        # Up-Down alignment
        # preamble_len >= 6;
        # There are two NetID chirps between preamble and SFD
        # `_detect` has already shifted up peak to position 0 (XXX: what does this mean?)
        (_, pkd_bin) = self._dechirp(signal, start, False)
        if pkd_bin + 1 > self._bin_num / 2:
            start += round((pkd_bin - self._bin_num) /
                           self._zero_padding_ratio)
        else:
            start += round(pkd_bin / self._zero_padding_ratio)
        # Set preamble reference bin for CFO elimination
        (_, preamble_bin) = self._dechirp(signal, start - 4 * self._sample_num)
        if preamble_bin + 1 > self._bin_num / 2:
            cfo = (preamble_bin - self._bin_num) * \
                self._bandwidth / self._bin_num
        else:
            cfo = preamble_bin * self._bandwidth / self._bin_num
        # Set start to the beginning of data symbols
        (pku, _) = self._dechirp(signal, start - self._sample_num)
        (pkd, _) = self._dechirp(signal, start - self._sample_num, False)
        if abs(pku) > abs(pkd):
            # Current symbol is the first downchirp
            new_start = start + round(2.25 * self._sample_num)
        else:
            # Current symbol is the second downchirp
            new_start = start + round(1.25 * self._sample_num)
        return (new_start, preamble_bin, cfo)

    def _parse_header(self, symbols: Array1D[np.uint16]) -> tuple[bool, int, int, bool]:
        """Parse the header.

        Parameters
        ----------
        symbols : Array1D[np.uint16]
            A list of eight symbols containing the header.

        Returns
        -------
        valid : bool
            Whether the header is valid.
        payload_len : int
            The payload length.
        cr : int
            The coding rate.
        crc: bool
            Whether CRC is enabled.
        """
        # Compensate CFO drift
        csymbols = self._proc.dynamic_compensation(symbols)
        # Gray coding
        symbols = self._proc.gray_coding(csymbols)
        # Deinterleave
        codewords = diag_deinterleave(
            slice1D(symbols, slice(0, 8)), self._spreading_factor - 2)  # XXX: why -2?
        # Parse header
        log.debug(f"Header codewords: {codewords}")
        # Header uses CR 4/8
        nibbles = self._proc.hamming_decode(codewords, 4 + 4)
        log.debug(f"Header nibbles: {nibbles}")
        return self._parse_header_inner(nibbles)

    def _parse_header_inner(self, nibbles: Array1D[np.uint8]) -> tuple[bool, int, int, bool]:
        """Parse the header.

        Parameters
        ----------
        nibbles : Array1D[np.uint8]
            Hamming decoded header nibbles.

        Returns
        -------
        valid : bool
            Whether the header is valid.
        payload_len : int
            The payload length.
        cr : int
            The coding rate.
        crc: bool
            Whether CRC is enabled.
        """
        payload_len = nibbles[0] * 16 + nibbles[1]
        crc = bool(nibbles[2] & 1)
        cr = nibbles[2] >> 1
        # We only calculate header checksum on the first three nibbles
        # the valid header checksum is considered to be 5 bits
        # other 3 bits require further reverse engineering
        data = np.unpackbits(
            nibbles[:3].astype(np.uint8).reshape(-1, 1), axis=1
        )[:, -4:].flatten()
        calculated_csum = calc_checksum(data)
        valid = (calculated_csum[-5] == (nibbles[3] & 1)) \
            and (calculated_csum[-4] == (nibbles[4] >> 3 & 1)) \
            and (calculated_csum[-3] == (nibbles[4] >> 2 & 1)) \
            and (calculated_csum[-2] == (nibbles[4] >> 1 & 1)) \
            and (calculated_csum[-1] == (nibbles[4] & 1))
        if not valid:
            log.debug(f"Calculated checksum: {calculated_csum}")
            header_csum = (nibbles[3] & 1) << 4 | (nibbles[4] & 0xf)
            log.debug(f"Received checksum: {header_csum}")
            log.debug(f"{nibbles[3] & 1}")
            log.debug(f"{nibbles[4] & 0xf}")
        log.debug(
            f"Payload length: {payload_len}, code rate: {cr}, CRC: {crc}")
        return (valid, int(payload_len), int(cr), crc)


def xorbits16(data: NDArray[np.uint16], mask: int) -> NDArray[np.uint8]:
    """XOR bits in a 16-bit integer with a mask.

    In LoRaPHY.m:
    ```matlab
    LoRaPHY.bit_reduce(@bitxor, data, (bits of mask))
    ```

    Parameters
    ----------
    data : NDArray[np.uint16]
        The data to process.
    mask : int
        The mask showing which bits to XOR.

    Returns
    -------
    NDArray[np.uint8]
        The result of XORing the bits.
    """
    # XOR 0 is a nop, so just AND mask and XOR all bits
    # This should be much faster than the MATLAB implementation
    new = data & mask
    # Now the original function XORs all bits. This is equivalent to
    # the multi-input XOR in boolean algebra (odd function),
    bits = np.unpackbits(new.view(np.uint8)).reshape(-1, 16)
    result: NDArray[np.uint8] = np.bitwise_xor.reduce(bits, axis=1)
    return result


def diag_deinterleave(symbols: Array1D[np.uint16], ppm: int) -> Array1D[np.uint16]:
    """Diagonal deinterleaving.

    Parameters
    ----------
    symbols : Array1D[np.uint16]
        Symbols after gray coding.
    ppm : int
        Size with parity bits.

    Returns
    -------
    Array1D[np.uint16]
        Codewords after deinterleaving.

    Examples
    --------
    >>> diag_deinterleave(np.arange(10, dtype=np.uint16), 5)
    array([ 32, 274, 736, 204, 648], dtype=uint16)
    >>> diag_deinterleave(np.arange(10, dtype=np.uint16), 4)
    array([712, 674,  16, 492], dtype=uint16)
    """
    # The original MATLAB implementation is MATLAB magic
    # b is a matrix: each row is an element of `symbols` and the `ppm`
    # columns are the bits of the element
    # b = de2bi(symbols, double(ppm), 'left-msb')
    # Take the `x`th row, circular right shift by 1-x (i.e. left shift by
    # x-1), and downshift by 1. The `x`th row in MATLAB is the `x-1`th here
    # Since this is a row, the downshift part is nop
    # @(x) circshift(b(x,:), [1 1-x]
    # Do this for all rows, make a matrix out of it, and transpose
    # cell2mat(arrayfun(_, (1:length(symbols))', 'un', 0))'
    # This NumPy implementation should also be fully vectorizable
    lensymbols = len(symbols)
    # modulo: Be careful not to shift everything out of the array
    shiftamount = np.arange(lensymbols, dtype=np.uint16) % ppm
    # circular left shift by index
    shifted = (symbols << shiftamount & ((1 << ppm) - 1)) \
        | (symbols >> (ppm - shiftamount))
    # Prepare for bit unpacking
    shifted = shifted.reshape(lensymbols, 1)
    masks = 1 << np.arange(ppm, dtype=np.uint16).reshape(1, ppm)
    # MATLAB bi2de is right-msb, and this code also produces so
    unpacked = (shifted & masks).astype(bool).astype(
        np.uint8).reshape(lensymbols, ppm)
    # Now transpose and pack the bits back
    unpacked = unpacked.transpose()
    bitweights = 1 << np.arange(lensymbols, dtype=np.uint16)
    codewords: Array1D[np.uint16] = unpacked.dot(bitweights)
    return codewords


class RxProcessing:
    """Various data processing functions for LoRaReceiver."""

    def __init__(
        self,
        rf_freq: float,
        spreading_factor: int,
        low_data_rate_optimization: bool,
        hamming_decoding_en: bool = True,
    ):
        self.rf_freq = rf_freq
        self.spreading_factor = spreading_factor
        self.hamming_decoding_en = hamming_decoding_en
        self.low_data_rate_optimization = low_data_rate_optimization

    def dynamic_compensation(self, data: Array1D[np.uint16], cfo: float = 0.0) -> Array1D[np.float64]:
        """Compensate bin drift.

        Parameters
        ----------
        data : Array1D[np.uint16]
            Symbols with bin drift.
        cfo : float
            Current carrier frequency offset.

        Returns
        -------
        Array1D[np.float64]
            Symbols after compensation.

        Examples
        --------
        >>> proc = RxProcessing(913e6, 12, True)
        >>> proc.dynamic_compensation(np.array([1, 2, 3, 4, 5, 45, 46, 47, 99, 127]))
        array([  1.,   1.,   1.,   1.,   1.,  41.,  41.,  41.,  93., 121.])
        >>> proc = RxProcessing(913e6, 12, False)
        >>> proc.dynamic_compensation(np.array([1, 2, 3, 4, 5, 45, 46, 47, 99, 127]), 0.1)
        array([  0.9999991 ,   1.99999865,   2.99999821,   3.99999776,
                 4.99999731,  44.99999686,  45.99999641,  46.99999596,
                98.99999551, 126.99999507])
        """
        sfo_drift: NDArray[np.float64] = np.arange(2, len(data) + 2) * \
            2**self.spreading_factor * cfo / self.rf_freq
        symbols: Array1D[np.float64] = (
            data - sfo_drift) % 2**self.spreading_factor
        if self.low_data_rate_optimization:
            bin_offset = 0.0
            v_last = 1.0
            modulus = 4
            for i, v in enumerate(symbols):
                bin_delta = (v - v_last) % modulus
                if bin_delta < modulus / 2:
                    bin_offset -= bin_delta
                else:
                    bin_offset -= bin_delta - modulus
                v_last = v
                symbols[i] = (v + bin_offset) % 2**self.spreading_factor
        return symbols

    def gray_coding(self, data: Array1D[np.float64]) -> Array1D[np.uint16]:
        """Gray coding (used in the decoding process).

        Parameters
        ----------
        data : Array1D[np.float64]
            Symbols with bin drift.

        Returns
        -------
        Array1D[np.uint16]
            Symbols after bin calibration.

        Examples
        --------
        >>> proc = RxProcessing(1, 8, False) # No LDO
        >>> proc.gray_coding(np.array(
        ...  [5.51551554, 5.83092023, 2.75949233, 2.42150821, 7.9605089,
        ...   9.49095554, 4.11876407, 6.88723312, 4.23367174, 7.573479]
        ... ))
        array([1, 1, 0, 0, 1, 3, 1, 1, 2, 4], dtype=uint16)
        >>> proc = RxProcessing(1, 8, True) # LDO
        >>> proc.gray_coding(np.array(
        ...  [5.51551554, 5.83092023, 2.75949233, 2.42150821, 7.9605089,
        ...   9.49095554, 4.11876407, 6.88723312, 4.23367174, 7.573479]
        ... ))
        array([1, 1, 0, 0, 1, 3, 1, 1, 1, 1], dtype=uint16)
        """
        result = np.empty(len(data), dtype=np.uint16)
        result[:8] = np.floor(data[:8] / 4)
        if self.low_data_rate_optimization:
            result[8:] = np.floor(data[8:] / 4)
        else:
            # This is float modulo, and note that MATLAB uint16() does rounding
            # instead of truncation
            result[8:] = ((data[8:] - 1) % (2**self.spreading_factor)).round()
        return cast1D(np.bitwise_right_shift(result, 1) ^ result)

    def hamming_decode(self, codewords: Array1D[np.uint16], rdd: int) -> Array1D[np.uint8]:
        """Hamming decoding.

        Parameters
        ----------
        codewords : Array1D[np.uint16]
            Codewords after deinterleaving.
        rdd : int
            Number of redundant bits (see `LoRaPHY.decode`).

        Returns
        -------
        nibbles : Array1D[np.uint8]
            Decoded nibbles.
        """
        _p1 = xorbits16(codewords, 0b10001101)  # 1,3,4,8
        p2 = xorbits16(codewords, 0b01001011)  # 1,2,4,7
        p3 = xorbits16(codewords, 0b00010111)  # 1,2,3,5
        _p4 = xorbits16(codewords, 0b00011111)  # 1,2,3,4,5
        p5 = xorbits16(codewords, 0b00101110)  # 2,3,4,6

        @np.vectorize
        def parity_fix(p: int) -> int:
            t = {
                3: 4,  # 011 wrong b3
                5: 8,  # 101 wrong b4
                6: 1,  # 110 wrong b1
                7: 2,  # 111 wrong b2
            }
            return t.get(p, 0)
        if self.hamming_decoding_en:
            if rdd in (7, 8):
                parity = p2 * 4 + p3 * 2 + p5
                pf = parity_fix(parity)
                codewords ^= pf.astype(np.uint16)
            elif rdd not in (5, 6):
                raise InvalidCodingRateError()
        return cast1D((codewords & 0xf).astype(np.uint8))
