// src/components/Predictions.js

import React, { useRef } from 'react';
import { useInView } from 'react-intersection-observer';
import './Predictions.css';

function Predictions({ predictions }) {
  if (predictions.length === 0) return null;

  const formatTimestamp = (timeInSeconds) => {
    const date = new Date(timeInSeconds * 1000);
    const minutes = date.getUTCMinutes().toString().padStart(2, '0');
    const seconds = date.getUTCSeconds().toString().padStart(2, '0');
    const milliseconds = date.getUTCMilliseconds().toString().padStart(3, '0');
    return `${minutes}:${seconds}.${milliseconds}`;
  };

  // Calculate total height required for the timeline
  const itemSpacing = 80; // Must match the spacing used in topPosition
  const totalHeight = (predictions.length - 1) * itemSpacing + 100; // Add extra for padding

  return (
    <div className="timeline-container">
      <h2>Timeline</h2>
      <div className="timeline" style={{ height: `${totalHeight}px` }}>
        {predictions.map((pred, index) => {
          const { ref, inView } = useInView({
            triggerOnce: true,
            threshold: 0.1,
          });

          // Position each item based on its index with consistent spacing
          const topPosition = index * itemSpacing; // 80px spacing between items

          const audioRef = useRef(null);

          const handlePlayAudio = () => {
            // Pause any currently playing audio
            document.querySelectorAll('audio').forEach(audio => {
              if (audio !== audioRef.current && !audio.paused) {
                audio.pause();
              }
            });
            // Play the selected audio
            if (audioRef.current) {
              audioRef.current.currentTime = 0;
              audioRef.current.play();
            }
          };

          return (
            <div
              ref={ref}
              key={index}
              className={`timeline-item ${inView ? 'slide-in' : ''} ${index % 2 === 0 ? 'left' : 'right'}`}
              style={{ top: `${topPosition}px` }}
              onClick={handlePlayAudio}
            >
              <span className="timeline-time">
                {formatTimestamp(pred.time)}
              </span>
              <div className="timeline-content">{pred.label}</div>
              {/* Set crossOrigin attribute */}
              <audio
                ref={audioRef}
                src={pred.audio_url}
                preload="auto"
                crossOrigin="anonymous"
              />
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Predictions;
