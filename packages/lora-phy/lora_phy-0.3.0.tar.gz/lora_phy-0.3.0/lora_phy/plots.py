import numpy as np
from scipy.signal import ShortTimeFFT  # type: ignore[import-untyped]

from .typing import Array1D, ComplexOrReal


def lora_spectrogram(signal: Array1D[ComplexOrReal], chirp_samples: int, fs: float, bw: float) -> None:
    """Plot a spectrogram."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("Plotting requires the 'matplotlib' package. "
                          "Please install it with 'pip install matplotlib'") from e
    N = len(signal)
    win_str = 'hamming'  # 'hann', 'hamming'
    stft_nfft = chirp_samples
    stft_window = chirp_samples // 4
    hop_length = stft_window // 8
    noverlap = stft_window - hop_length
    fft_mode = 'centered'
    lora_bw = bw+50e3  # 100e3 offset for plotting

    SFT = ShortTimeFFT.from_window(win_param=win_str, fs=fs, nperseg=stft_window,
                                   noverlap=noverlap, mfft=stft_nfft, fft_mode=fft_mode, scale_to='magnitude')
    gRx_stft = SFT.stft(signal)
    gRx_stft_dB = 20 * np.log10(np.abs(gRx_stft))

    fig, ax = plt.subplots(figsize=(6, 4))
    extent0 = SFT.extent(N, center_bins=True)
    im = ax.imshow(gRx_stft_dB, aspect='auto', origin='lower',
                   extent=extent0, cmap='turbo', interpolation='nearest')
    ax.set_title('LoRa Signal Spectrogram')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_ylim(-lora_bw/2, lora_bw/2)  # Limit y-axis to bw
    cbar = fig.colorbar(im)
    cbar.set_label('Power/Frequency (dB/Hz)')
    plt.tight_layout()
    plt.show()
