# model/feature_extraction.py

import numpy as np
import librosa

def extract_features_from_audio(y, sr):
    y_trimmed, _ = librosa.effects.trim(y)
    y_normalized = librosa.util.normalize(y_trimmed)

    # Determine appropriate n_fft
    n_fft = 2048 if len(y_normalized) >= 2048 else len(y_normalized)

    # Adjust hop_length and win_length accordingly
    hop_length = n_fft // 4
    win_length = n_fft

    # Extract features with adjusted n_fft
    chroma = librosa.feature.chroma_stft(y=y_normalized, sr=sr, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
    mfccs = librosa.feature.mfcc(y=y_normalized, sr=sr, n_mfcc=40, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
    spectral_contrast = librosa.feature.spectral_contrast(y=y_normalized, sr=sr, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
    zcr = librosa.feature.zero_crossing_rate(y_normalized, hop_length=hop_length)
    rolloff = librosa.feature.spectral_rolloff(y=y_normalized, sr=sr, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
    mel_spectrogram = librosa.feature.melspectrogram(y=y_normalized, sr=sr, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    mel_spectrogram_db_mean = np.mean(mel_spectrogram_db, axis=1)

    # Concatenate features
    features = np.concatenate((
        np.mean(chroma, axis=1),
        np.mean(mfccs, axis=1),
        np.mean(spectral_contrast, axis=1),
        np.mean(zcr, axis=1),
        np.mean(rolloff, axis=1),
        mel_spectrogram_db_mean
    ))
    return features
