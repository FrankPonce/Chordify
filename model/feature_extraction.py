# feature_extraction.py

import numpy as np
import librosa

def extract_features(file_name):
    sample_rate = 22050
    y, sr = librosa.load(file_name, sr=sample_rate)
    y_trimmed, _ = librosa.effects.trim(y)
    y_normalized = librosa.util.normalize(y_trimmed)

    # Extract features
    chroma = librosa.feature.chroma_stft(y=y_normalized, sr=sr)
    mfccs = librosa.feature.mfcc(y=y_normalized, sr=sr, n_mfcc=40)
    spectral_contrast = librosa.feature.spectral_contrast(y=y_normalized, sr=sr)

    # Concatenate features
    features = np.concatenate((
        np.mean(chroma, axis=1),
        np.mean(mfccs, axis=1),
        np.mean(spectral_contrast, axis=1)
    ))
    return features
