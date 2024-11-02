# app.py

import sys
import os

# Add the parent directory of api/ to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import librosa
import tensorflow as tf
import joblib
from werkzeug.utils import secure_filename

# Now you can import from the model module
from model.feature_extraction import extract_features

app = Flask(__name__)
CORS(app)

# Load the trained model and label encoder
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model', 'guitar_note_model.h5'))
encoder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model', 'label_encoder.joblib'))

model = tf.keras.models.load_model(model_path)
label_encoder = joblib.load(encoder_path)

# Allowed audio extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    file = request.files['audio']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)

        # Ensure the uploads directory exists
        os.makedirs('uploads', exist_ok=True)
        file.save(filepath)

        # Load and process the audio file
        y, sr = librosa.load(filepath, sr=22050)
        y_normalized = librosa.util.normalize(y)

        # Onset detection to find note/chord start times
        onset_frames = librosa.onset.onset_detect(y=y_normalized, sr=sr, units='time')
        onset_times = onset_frames.tolist()

        segments = []
        timestamps = []

        for i in range(len(onset_times)):
            start_time = onset_times[i]
            if i < len(onset_times) - 1:
                end_time = onset_times[i + 1]
            else:
                end_time = librosa.get_duration(y=y_normalized, sr=sr)
            # Extract the segment
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            y_segment = y_normalized[start_sample:end_sample]
            if len(y_segment) == 0:
                continue
            features = extract_features_from_audio(y_segment, sr)
            segments.append(features)
            timestamps.append(start_time)

        if not segments:
            return jsonify({'error': 'No valid audio segments found'}), 400

        X = np.array(segments)
        predictions = model.predict(X)
        predicted_labels = label_encoder.inverse_transform(np.argmax(predictions, axis=1))

        # Remove the uploaded file
        os.remove(filepath)

        # Prepare the response with timestamps
        response = []
        for label, time in zip(predicted_labels, timestamps):
            response.append({'time': time, 'label': label})

        return jsonify({'predictions': response})

    else:
        return jsonify({'error': 'Invalid file type'}), 400

def extract_features_from_audio(y, sr):
    # Extract features from audio segment
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

    # Concatenate features
    features = np.concatenate((
        np.mean(chroma, axis=1),
        np.mean(mfccs, axis=1),
        np.mean(spectral_contrast, axis=1)
    ))
    return features

if __name__ == '__main__':
    app.run(debug=True)
