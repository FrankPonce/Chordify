# data_preprocessing.py

import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
import librosa
from feature_extraction import extract_features, augment_audio

def load_data(data_dir):
    train_file_paths = []
    train_labels = []
    test_file_paths = []
    test_labels = []

    # Load Training data
    training_dir = os.path.join(data_dir, 'Training')
    for label in os.listdir(training_dir):
        label_dir = os.path.join(training_dir, label)
        if os.path.isdir(label_dir):
            for file in os.listdir(label_dir):
                if file.endswith('.wav'):
                    train_file_paths.append(os.path.join(label_dir, file))
                    train_labels.append(label)

    # Load Test data
    test_dir = os.path.join(data_dir, 'Test')
    for label in os.listdir(test_dir):
        label_dir = os.path.join(test_dir, label)
        if os.path.isdir(label_dir):
            for file in os.listdir(label_dir):
                if file.endswith('.wav'):
                    test_file_paths.append(os.path.join(label_dir, file))
                    test_labels.append(label)

    return train_file_paths, train_labels, test_file_paths, test_labels

def preprocess_data(train_file_paths, train_labels, test_file_paths, test_labels):
    # Process Training data
    train_features_list = []
    augmented_features_list = []
    augmented_labels = []
    for file, label in zip(train_file_paths, train_labels):
        y, sr = librosa.load(file, sr=22050)
        features = extract_features(y, sr)
        train_features_list.append(features)

        # Data augmentation
        y_augmented = augment_audio(y, sr)
        augmented_features = extract_features(y_augmented, sr)
        augmented_features_list.append(augmented_features)
        augmented_labels.append(label)

    # Combine original and augmented features
    train_features_list.extend(augmented_features_list)
    train_labels.extend(augmented_labels)  # Duplicate labels for augmented data

    # Process Test data
    test_features_list = []
    for file in test_file_paths:
        y, sr = librosa.load(file, sr=22050)
        features = extract_features(y, sr)
        test_features_list.append(features)

    # Encode labels
    le = LabelEncoder()
    y_train_encoded = le.fit_transform(train_labels)
    y_test_encoded = le.transform(test_labels)  # Use transform to maintain consistency

    # Create feature matrices and target vectors
    X_train = np.array(train_features_list)
    y_train = np.array(y_train_encoded)
    X_test = np.array(test_features_list)
    y_test = np.array(y_test_encoded)

    return X_train, X_test, y_train, y_test, le
