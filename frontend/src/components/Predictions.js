// src/components/Predictions.js

import React from 'react';
import { useInView } from 'react-intersection-observer';
import './Predictions.css';

function Predictions({ predictions }) {
  if (predictions.length === 0) return null;

  // Calculate the total song length based on the last prediction timestamp
  const songLength = Math.max(...predictions.map(pred => pred.time));
  
  return (
    <div className="timeline-container">
      <h2>Timeline</h2>
      <div className="timeline" style={{ height: `${songLength * 100}px` }}>
        {predictions.map((pred, index) => {
          const { ref, inView } = useInView({
            triggerOnce: true,
            threshold: 0.1,
          });

          // Calculate the vertical position based on timestamp relative to song length
          const topPosition = (pred.time / songLength) * 100;

          return (
            <div
              ref={ref}
              key={index}
              className={`timeline-item ${inView ? 'slide-in' : ''} ${index % 2 === 0 ? 'left' : 'right'}`}
              style={{ top: `${topPosition}%` }}
            >
              <span className="timeline-time">{new Date(pred.time * 1000).toISOString().substr(14, 5)}</span>
              <div className="timeline-content">{pred.label}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Predictions;
