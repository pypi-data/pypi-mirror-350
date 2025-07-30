"""A multi-channel LoRa simulator."""


import math
from collections.abc import Callable

import numpy as np

from .tx import LoRaTransmitter
from .typing import Array1D, concat1D


class MultiTxDevice:
    """Represents one LoRa transmitter with some associated delay and channel.

    Parameters
    ----------
    tx : LoRaTransmitter
        The LoRa transmitter.
        The `LoRaTransmitter` class is reentrant, so you can use the same instance for multiple transmitters.
    payload : Array1D[np.uint8]
        The payload to be transmitted from this transmitter.
    granularity : int
        The minimum time step for the simulation in samples.
    t0 : int, optional
        The starting time of the transmission in samples after the simulation starts.
        Default is 0, which means the transmission starts as soon as the simulation starts.
    channel_fn : ChannelFunction, optional
        A function that maps the transmitted signal to the received signal at the specified time.
        Default is None, which means no channel effect is applied.
    """

    def __init__(
        self,
        tx: LoRaTransmitter,
        payload: Array1D[np.uint8],
        granularity: int,
        t0: int = 0,
        channel_fn: Callable[[Array1D[np.complex128], float],
                             Array1D[np.complex128]] | None = None,
    ):
        self.tx = tx
        self.payload = payload
        self.t0 = t0
        self.granularity = granularity
        self.channel_fn = channel_fn

    def make_signal(self) -> tuple[Array1D[np.complex128], int, int]:
        """Generate the signal from this transmitter.

        Returns
        -------
        Array1D[np.complex128]
            The generated signal.
        int
            The actual time where the signal should be inserted in the simulation in granularity units.
        int
            The number of segments in the signal.
        """
        symbols = self.tx.encode(self.payload)
        signal = self.tx.modulate(symbols)
        # Apply the channel effect if a channel function is provided
        if self.channel_fn is not None:
            signal = self.channel_fn(signal, self.t0)
        # Determine where this signal should be inserted in the simulation
        start_idx, start_padding_len = divmod(self.t0, self.granularity)
        # Pad the signal from the previous granularity with zeros
        start_padding = np.zeros(start_padding_len, dtype=signal.dtype)
        # Pad the end until the next granularity
        start_padded_len = start_padding_len + len(signal)
        total_nseg = math.ceil(start_padded_len / self.granularity)
        end_padding_len = (total_nseg * self.granularity) - start_padded_len
        end_padding = np.zeros(end_padding_len, dtype=signal.dtype)
        padded_signal = concat1D((start_padding, signal, end_padding))
        print(f"Orig {len(signal)}, Padded {len(padded_signal)}, idx {
              start_idx}:{start_idx + total_nseg}")
        return padded_signal, start_idx, total_nseg


class MultiTxSimulator:
    """Simulates a multi-channel LoRa system indefinitely.

    Use `add_tx` to add a new transmitter to the simulation.

    Parameters
    ----------
    granularity : int
        The minimum time step for the simulation in samples.
    initial_transmitters : list[TxDevice], optional
        A list of initial transmitters to be added to the simulation.
        Default is None, which means no initial transmitters are added.
    """

    def __init__(
        self,
        granularity: int,
        initial_transmitters: list[MultiTxDevice] | None = None
    ):
        """
        Initialize the MultiTxSimulator.
        """
        # (start_idx, end_idx, signal)
        self.signals: list[tuple[int, int, Array1D[np.complex128]]] = []
        # in samples
        self.granularity = granularity
        # in granularity units
        self.idx = 0
        for tx in initial_transmitters or []:
            self.add_tx(tx)

    def add_tx(
        self,
        tx_device: MultiTxDevice,
    ) -> None:
        """Add a new transmitter to the simulation.

        Parameters
        ----------
        tx_device : TxDevice
            The transmitter device to be added.
        """
        if tx_device.t0 < self.idx * self.granularity:
            raise ValueError("Too late to add this transmitter.")
        (signal, start_idx, n_segments) = tx_device.make_signal()
        self.signals.append((start_idx, start_idx + n_segments, signal))
        self.signals.sort(key=lambda x: x[0])

    def get_end_index(self) -> int:
        """Get the end index of the simulation for the signals we have so far.

        Returns
        -------
        int
            The end index of the simulation (exclusive).
        """
        if not self.signals:
            return 0
        # The end index is the maximum end index of all signals
        return max(end for _, end, _ in self.signals)

    def get_segments(
        self,
        n: int,
    ) -> Array1D[np.complex128]:
        """Get one or multiple segments of the signal in terms of granularity.
        After this function, the internal time index is updated and those that have
        already been fully transmitted are removed.

        Parameters
        ----------
        n : slice
            The number of segments to get.

        Returns
        -------
        Array1D[np.complex128]
            The segments of the signal.
        """
        # We care about segments numbered from self.idx to self.idx + n - 1
        result = np.zeros(self.granularity * n, dtype=np.complex128)
        to_remove_indices = []
        # Iterate over the signals and add them to the result
        for i, (start, end, signal) in enumerate(self.signals):
            if start <= self.idx < end:
                # The signal is in the range we care about
                # Calculate the start and end indices in the signal
                start_idx = (self.idx - start) * self.granularity
                end_idx = start_idx + self.granularity * n
                # Add the signal to the result
                this_signal = signal[start_idx:end_idx]
                # Deal with some signals being shorter than the requested length
                this_signal_len = len(this_signal)
                result[:this_signal_len] += this_signal
            if end <= self.idx:
                # The signal is fully transmitted, mark it for removal
                to_remove_indices.append(i)
        # Remove fully transmitted signals
        for i in reversed(to_remove_indices):
            del self.signals[i]
        self.idx += n
        return result
