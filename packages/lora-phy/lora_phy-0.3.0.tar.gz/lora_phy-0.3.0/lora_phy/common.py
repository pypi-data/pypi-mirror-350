import binascii
import math

import numpy as np

from .typing import Array1D


def chirp_in_place(
    up: bool,
    spreading_factor: int,
    bandwidth: float,
    sample_rate: float,
    out: Array1D[np.complex128],
    *,
    start_freq_offset: float = 0,
    cfo: float = 0,
    tdelta: float = 0,
    tscale: float = 1,
) -> None:
    """Generate a LoRa chirp symbol.

    Parameters
    ----------
    up : bool
        `True` for up-chirp, `False` for down-chirp.
    spreading_factor : int
        Spreading factor.
    bandwidth : float
        Bandwidth.
    sample_rate : float
        Sampling frequency.
    out : Array1D[np.complex128]
        Output array for the chirp symbol.
        The length of this array should be calculated using
        `chirp_len(spreading_factor, bandwidth, sample_rate)`.
    start_freq_offset : float
        Start frequency offset (0 to 2**spreading_factor-1).
    cfo : float
        Carrier frequency offset.
    tdelta : float
        Time offset (0 to 1/sample_rate).
    tscale : float
        Scaling the sampling frequency.
    """
    # See `chirp_len`
    num_symbols = 1 << spreading_factor
    samples_per_symbol = chirp_len(spreading_factor, bandwidth, sample_rate)
    # bandwidth / num_symbols -> number of symbols per second
    # num_symbols / bandwidth -> time for one symbol
    seconds_per_symbol = num_symbols / bandwidth
    int_start_freq_offset = round(start_freq_offset)
    cfo = cfo + (start_freq_offset - int_start_freq_offset) * \
        bandwidth / num_symbols
    if up:
        # slope of the chirp in Hz/s
        dfdt = bandwidth / seconds_per_symbol
        # frequency at t = 0
        f0 = -bandwidth / 2 + cfo
    else:
        dfdt = -bandwidth / seconds_per_symbol
        f0 = bandwidth / 2 + cfo
    # Generate the chirp in two parts: c1: before the frequency discontinuity, c2: after
    c2len = samples_per_symbol * int_start_freq_offset // num_symbols
    # One extra sample for calculating the phase
    # I believe the original MATLAB code has a bug here: its rounding
    # is wrong for non-integral `int_start_freq_offset/N`.
    # See test case `test_chirp_3_shouldfail` in `phytest.py`
    c1len = samples_per_symbol - c2len + 1
    if c2len == 0:
        # No need to generate c2 (int_start_freq_offset == 0)
        t = np.arange(c1len - 1) / sample_rate * tscale + tdelta
        f = f0 + dfdt * int_start_freq_offset / bandwidth + 0.5 * dfdt * t
        expn = 1j * 2 * np.pi * f * t
        np.exp(expn, out=out)
        return
    # The rest is unused for this module, but still implemented and tested
    t1 = np.arange(c1len) / sample_rate * tscale + tdelta
    # The original MATLAB code did not multiply by `tscale` here:
    # probably a mistake
    t2 = np.arange(c2len) / sample_rate * tscale + tdelta
    f1 = f0 + dfdt * int_start_freq_offset / bandwidth + 0.5 * dfdt * t1
    np.exp(1j * 2 * np.pi * f1 * t1, out=out[:c1len])
    phi = 0 if c1len <= 0 else np.angle(out[c1len-1])
    # Overwrite the last element of c1 with the first element of c2
    f2 = f0 + 0.5 * dfdt * t2
    np.exp(1j * (phi + 2 * np.pi * f2 * t2), out=out[c1len-1:])


def chirp_len(
    spreading_factor: int,
    bandwidth: float,
    sample_rate: float,
) -> int:
    """Find the length of a single chirp symbol.

    Parameters
    ----------
    spreading_factor : int
        Spreading factor.
    bandwidth : float
        Bandwidth.
    sample_rate : float
        Sampling frequency.
    """
    # `d_num_symbols` in `gr-lora` = area such that one chirp is its diagonal
    num_symbols = 1 << spreading_factor
    # `d_num_samples` in `gr-lora`
    return round(sample_rate * num_symbols / bandwidth)


def chirp(
    up: bool,
    spreading_factor: int,
    bandwidth: float,
    sample_rate: float,
    *,
    start_freq_offset: float = 0,
    cfo: float = 0,
    tdelta: float = 0,
    tscale: float = 1,
) -> Array1D[np.complex128]:
    """Generate a LoRa chirp symbol. See `chirp_in_place` for details."""
    result = np.empty(chirp_len(
        spreading_factor, bandwidth, sample_rate), dtype=np.complex128)
    chirp_in_place(
        up, spreading_factor, bandwidth, sample_rate, result,
        start_freq_offset=start_freq_offset, cfo=cfo, tdelta=tdelta,
        tscale=tscale)
    return result


def calc_crc(data: Array1D[np.uint8]) -> tuple[np.uint8, np.uint8]:
    """Calculate CRC.

    Parameters
    ----------
    data : Array1D[np.uint8]
        Data in bytes.

    Returns
    -------
    tuple[np.uint8, np.uint8]
        The CRC checksum.

    Examples
    --------
    >>> calc_crc(np.array([1, 2, 3, 4, 5, 45, 46, 47, 99, 127], dtype=np.uint8))
    (np.uint8(31), np.uint8(139))
    >>> calc_crc(np.array([], dtype=np.uint8))
    (np.uint8(0), np.uint8(0))
    >>> calc_crc(np.array([1], dtype=np.uint8))
    (np.uint8(1), np.uint8(0))
    """
    if len(data) == 0:
        return (np.uint8(0), np.uint8(0))
    if len(data) == 1:
        return (data[-1], np.uint8(0))
    if len(data) == 2:
        return (data[-1], data[-2])
    seq = binascii.crc_hqx(data[:-2].tobytes(order="C"), 0)
    high = (seq >> 8) ^ data[-2]
    low = (seq & 0xff) ^ data[-1]
    return (low, high)


def calc_checksum(data: Array1D[np.uint8]) -> Array1D[np.uint8]:
    header_csum_mtx = np.array(
        [[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
         [0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0],
         [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1],
         [0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1]],
        dtype=np.uint8
    )
    result = np.empty(5, dtype=np.uint8)
    header_csum_mtx.dot(data, out=result)
    result &= 1
    return result


def dewhiten(data: Array1D[np.uint8]) -> None:
    """Data dewhitening or whitening. This operation is its own inverse.

    Generation algorithm directly translated from
    https://github.com/jkadbear/LoRaPHY/blob/master/LoRaPHY.m,
    in which "The whitening sequence is generated by an LFSR"
    $$x^8+x^6+x^5+x^4+1$$.

    Bastille Reasearch's `gr-lora` seems to have a different set:
    https://github.com/BastilleResearch/gr-lora/blob/master/include/lora/lora.h

    Parameters
    ----------
    data : Array1D[np.uint8]
        Bytes after deinterleaving.

    Returns
    -------
    None
        Input data is dewhitened in-place.

    Examples
    --------
    >>> data = np.array([1, 2, 3, 4, 5, 45, 46, 47, 99, 127])
    >>> dewhiten(data)
    >>> data
    array([254, 252, 255, 252, 245, 204, 236, 170, 104, 104])
    """
    reg = 0xff
    for i in range(len(data)):
        data[i] ^= reg
        reg = (reg << 1 & 0xff) ^ (reg >> 7 & 1) ^ (
            reg >> 5 & 1) ^ (reg >> 4 & 1) ^ (reg >> 3 & 1)


def calc_sym_num(
    has_header: bool,
    payload_len: int,
    cr: int,
    enable_crc: bool,
    spreading_factor: int,
    low_data_rate_optimization: bool,
) -> int:
    """Calculate the number of symbols.

    Parameters
    ----------
    has_header : bool
        Whether header is explicit.
    payload_len : int
        The payload length.
    cr : int
        Coding rate.
    enable_crc : bool
        Whether CRC is enabled.
    spreading_factor : int
        Spreading factor.
    low_data_rate_optimization : bool
        Whether low data rate optimization is enabled.

    Returns
    -------
    int
        The number of symbols.

    Examples
    --------
    >>> calc_sym_num(True, 10, 1, True, 7, False)
    28
    >>> calc_sym_num(True, 10, 2, True, 7, False)
    32
    >>> calc_sym_num(False, 10, 1, True, 7, False)
    23
    >>> calc_sym_num(False, 9, 1, False, 7, False)
    18
    """
    # Branchless version:
    # return 8 + max((4+cr)*np.ceil((2*payload_len-spreading_factor+7+4*enable_crc-5*(1-has_header))/(spreading_factor-2*low_data_rate_optimization)), 0)
    # Rewritten for logic clarity
    total = 2 * payload_len
    total -= spreading_factor
    total += 7
    if enable_crc:
        total += 4
    if not has_header:
        total -= 5
    per_sym = spreading_factor
    if low_data_rate_optimization:
        per_sym -= 2
    result = math.ceil(total / per_sym) * (cr + 4)
    return 8 + max(0, result)
