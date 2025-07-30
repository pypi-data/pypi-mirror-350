import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
 
 



 


def load_audio_to_mel(file_path:str, sr:int=22050, n_fft:int=4096, hop_length:int=200, win_length:int=2048, n_mels:int=128, fmin:int=50, fmax:int=11025) -> np.ndarray:
    """
    Converts an audio file to a mel spectrogram.

    This function loads an audio file, normalizes its amplitude, and computes 
    its mel spectrogram in decibel scale. It allows for fine-grained customization 
    of parameters related to audio processing and mel spectrogram generation.

    Args:
        file_path (str): Path to the audio file to be processed.
        sr (int, optional): Sampling rate for audio loading. Defaults to 22050 Hz.
        n_fft (int, optional): Number of FFT components for the Short-Time Fourier Transform (STFT). Defaults to 4096.
        hop_length (int, optional): Number of samples between successive frames. Controls time resolution. Defaults to 200.
        win_length (int, optional): Number of samples in each frame window for STFT. Defaults to 2048.
        n_mels (int, optional): Number of mel bands to generate. Defaults to 128.
        fmin (int, optional): Lowest frequency (in Hz) for the mel filter bank. Defaults to 50 Hz.
        fmax (int, optional): Highest frequency (in Hz) for the mel filter bank. Defaults to 11025 Hz.

    Returns:
        np.ndarray: A 2D NumPy array representing the mel spectrogram in decibel scale.

    Features:
        - Loads the audio file and resamples it to the specified sampling rate.
        - Normalizes the audio waveform to ensure values are within [-1, 1].
        - Computes a mel spectrogram with customizable frequency and time resolutions.
        - Converts the mel spectrogram to decibel scale for better interpretability.

    Notes:
        - The function uses Librosa for audio processing.
        - Ensure the audio file format is supported by Librosa.
        - `fmax` should not exceed half the sampling rate (`sr/2`) to comply with the Nyquist theorem.

    Example:
        >>> mel_db = load_audio_to_mel("example.wav", sr=16000, n_fft=2048, n_mels=64, fmin=20, fmax=8000)
        >>> print(mel_db.shape)
        (64, 801)  # Example output dimensions for 64 mel bands and ~5 seconds of audio.

    Dependencies:
        - `librosa`: For audio loading and spectrogram computation.
        - `numpy`: For waveform normalization and numerical operations.
    """
    
    audio, _ = librosa.load(file_path, sr=sr)
    audio = audio / np.abs(audio).max()
    mel_spectrogram = librosa.feature.melspectrogram(
        y=audio, sr=sr, n_fft=n_fft, hop_length=hop_length, win_length=win_length,
        n_mels=n_mels, fmin=fmin, fmax=fmax
    )
    mel_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    return mel_db



def graph_mel_spectrogram(spectrogram:np.ndarray, output_dir:str='', fig_size:tuple[int, int]=(12,6), name:str='Spectrogram', cmap:str='magma', show:bool=True, save:bool=False) -> None:
    """
    Visualizes and optionally saves a mel spectrogram as an image.

    This function generates a visualization of a mel spectrogram using Matplotlib.
    It allows customization of the figure size, colormap, and whether the image 
    is saved, displayed, or both.

    Args:
        spectrogram (np.ndarray): A 2D NumPy array representing the mel spectrogram to be visualized.
        output_dir (str): Directory where the spectrogram image will be saved if `save` is True.
        fig_size (tuple[int, int], optional): Size of the figure in inches (width, height). Defaults to (12, 6).
        name (str, optional): Name of the spectrogram, used as the title and filename. Defaults to 'Spectrogram'.
        cmap (str, optional): Colormap for the spectrogram visualization. Defaults to 'magma'.
        show (bool, optional): If True, displays the plot using `plt.show()`. Defaults to True.
        save (bool, optional): If True, saves the spectrogram image to `output_dir` with the specified `name`. Defaults to False.

    Returns:
        None: The function performs visualization and optionally saves or displays the plot.

    Features:
        - Uses `plt.imshow` to plot the mel spectrogram with the specified colormap.
        - Adds a color bar to represent amplitude levels in the spectrogram.
        - Automatically adjusts the layout for a clean appearance with `plt.tight_layout`.
        - Allows the user to control whether the plot is saved, displayed, or both.

    Notes:
        - The function assumes that `output_dir` exists. Ensure the directory is created beforehand.
        - To avoid clutter, the figure is not explicitly closed with `plt.close()`; however, adding it can help manage memory when generating multiple plots.

    Example:
        >>> spectrogram = np.random.rand(128, 500)
        >>> graph_mel_spectrogram(
        ...     spectrogram, output_dir='outputs', name='Example', fig_size=(10, 5), save=True, show=False
        ... )
        # This will save the spectrogram as 'outputs/Example.png'.

    Limitations:
        - The input spectrogram is expected to be in decibel or similar units. Ensure the scale is appropriate for visualization.

    Dependencies:
        - Requires Matplotlib for visualization and os for saving files.

    """
    
    plt.figure(figsize=fig_size)
    plt.imshow(spectrogram, origin='lower', aspect='auto', cmap=cmap)
    plt.colorbar()
    plt.title(f'Mel-espectrograma {name}')
    plt.xlabel('Frames')
    plt.ylabel('Mels')
    plt.tight_layout()
    if save:
        output_path = os.path.join(output_dir, f'{name}.png')
        plt.savefig(output_path)
    if show:
        plt.show() 
    if save or show:
        plt.close()
    