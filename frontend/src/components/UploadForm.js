// src/components/UploadForm.js

import React, { useState } from 'react';
import axios from 'axios';
import Predictions from './Predictions';
import { BeatLoader } from 'react-spinners';

function UploadForm() {
  const [audioFile, setAudioFile] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setAudioFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!audioFile) {
      alert('Please select an audio file.');
      return;
    }

    const formData = new FormData();
    formData.append('audio', audioFile);

    setLoading(true);
    setError(null);
    setPredictions([]);

    axios.post('https://chordify-backend.onrender.com/predict', formData)
      .then(response => {
        setPredictions(response.data.predictions);
        setLoading(false);
      })
      .catch(error => {
        console.error('There was an error!', error);
        setError('An error occurred during prediction.');
        setLoading(false);
      });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="audio/*" onChange={handleFileChange} />
        <button type="submit">Upload and Predict</button>
      </form>
      
      {loading && (
        <div className="spinner-container">
          <BeatLoader color="#ff3399" loading={loading} size={15} />
        </div>
      )}
      
      {error && <p>{error}</p>}
      {predictions.length > 0 && (
        <Predictions predictions={predictions} />
      )}
    </div>
  );
}

export default UploadForm;
