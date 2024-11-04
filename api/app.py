# app.py

import sys
import os

# Add the parent directory of api/ to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
import numpy as np
import tensorflow as tf
import joblib
from werkzeug.utils import secure_filename
import soundfile as sf
import librosa

# Import your feature extraction function
from model.feature_extraction import extract_features_from_audio

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load the trained model, label encoder, and scaler
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model', 'guitar_note_model.h5'))
encoder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model', 'label_encoder.joblib'))
scaler_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model', 'scaler.joblib'))

model = tf.keras.models.load_model(model_path)
label_encoder = joblib.load(encoder_path)
scaler = joblib.load(scaler_path)

# Allowed audio extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/static/segments/<path:filename>')
def serve_audio(filename):
    response = make_response(send_from_directory('static/segments', filename))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Range'
    response.headers['Access-Control-Expose-Headers'] = 'Accept-Ranges, Content-Encoding, Content-Length, Content-Range'
    return response

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

        # Improved segmentation using onset detection
        segments, timestamps = segment_chords(y_normalized, sr)

        if not segments:
            return jsonify({'error': 'No valid audio segments found'}), 400

        response = []

        for i, (y_segment, start_time) in enumerate(zip(segments, timestamps)):
            if len(y_segment) == 0:
                continue
            features = extract_features_from_audio(y_segment, sr)
            features_scaled = scaler.transform([features])

            # Reshape for model input
            features_scaled = features_scaled.reshape(-1, features_scaled.shape[1], 1)

            prediction = model.predict(features_scaled)
            predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])

            # Save the audio segment
            segment_filename = f'segment_{i}.wav'
            segment_filepath = os.path.join('static', 'segments', segment_filename)
            os.makedirs(os.path.dirname(segment_filepath), exist_ok=True)
            sf.write(segment_filepath, y_segment, sr)
            segment_url = request.url_root + 'static/segments/' + segment_filename
            response.append({'time': start_time, 'label': predicted_label[0], 'audio_url': segment_url})

        # Remove the uploaded file
        os.remove(filepath)

        return jsonify({'predictions': response})

    else:
        return jsonify({'error': 'Invalid file type'}), 400

# Include the updated segment_chords function
def segment_chords(y_normalized, sr):
    import numpy as np
    import librosa

    # Detect onset frames
    onset_frames = librosa.onset.onset_detect(y=y_normalized, sr=sr, hop_length=512, backtrack=True)

    # Convert onset frames to sample indices
    onset_samples = librosa.frames_to_samples(onset_frames)

    # Add the start and end of the audio
    boundaries = np.concatenate(([0], onset_samples, [len(y_normalized)]))

    # Filter out short segments
    min_segment_duration = 0.5  # Minimum duration in seconds
    min_segment_length = int(min_segment_duration * sr)

    segments = []
    timestamps = []

    for i in range(len(boundaries) - 1):
        start_sample = boundaries[i]
        end_sample = boundaries[i + 1]
        segment_length = end_sample - start_sample

        if segment_length < min_segment_length:
            continue  # Skip short segments

        y_segment = y_normalized[start_sample:end_sample]
        segments.append(y_segment)
        timestamps.append(start_sample / sr)

    return segments, timestamps

if __name__ == '__main__':
    app.run(debug=True)
