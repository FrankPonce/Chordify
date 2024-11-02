// src/App.js

import React, { useState } from 'react';
import Header from './components/Header';
import Predictions from './components/Predictions';
import axios from 'axios';
import { BeatLoader } from 'react-spinners';
import './styles.css';

function App() {
  const [audioFile, setAudioFile] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setAudioFile(e.target.files[0]);
  };

  const handlePredict = () => {
    if (!audioFile) {
      alert('Please upload an audio file first!');
      return;
    }

    const formData = new FormData();
    formData.append('audio', audioFile);

    setLoading(true);
    setError(null);
    setPredictions([]);

    axios.post('http://localhost:5000/predict', formData)
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
    <div className="App">
      {/* Background animation container */}
      <div className="background-animation">
      <div className="soundwave small"></div>
  <div className="soundwave medium"></div>
  <div className="soundwave large"></div>
      </div>

      <Header onFileChange={handleFileChange} onPredict={handlePredict} />
      {loading ? (
        <div className="spinner-container">
          <BeatLoader color="#ff3399" loading={loading} size={15} />
        </div>
      ) : (
        predictions.length > 0 && <Predictions predictions={predictions} />
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;
