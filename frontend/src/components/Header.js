// src/components/Header.js

import React from 'react';
import './Header.css';

function Header({ onFileChange, onPredict }) {
  return (
    <div className="header">
      <img src="/chordify.png" alt="Chordify.ai Logo" className="logo" />
      <p>
        Discover the chords and notes of your favorite music in an interactive, stylish way.
        Upload your audio file to see it come to life in real-time!
      </p>
      <div className="button-container">
        <label htmlFor="audio-upload">UPLOAD</label>
        <input 
          id="audio-upload" 
          type="file" 
          accept="audio/*" 
          onChange={onFileChange} 
        />
        <button onClick={onPredict}>PREDICT</button>
      </div>
    </div>
  );
}

export default Header;
