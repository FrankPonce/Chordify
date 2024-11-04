import React, { useEffect } from 'react';
import {
  Renderer,
  Stave,
  StaveNote,
  Accidental,
  Formatter,
  Voice,
  Articulation,
} from 'vexflow';
import './ScoreSheet.css';

function ScoreSheet({ predictions }) {
  useEffect(() => {
    const div = document.getElementById('score-sheet');
    div.innerHTML = ''; // Clear previous content
    const renderer = new Renderer(div, Renderer.Backends.SVG);
    const width = window.innerWidth * 0.9;
    const chordsPerMeasure = 4;

    // Calculate measures
    const measures = [];
    for (let i = 0; i < predictions.length; i += chordsPerMeasure) {
      measures.push(predictions.slice(i, i + chordsPerMeasure));
    }

    const height = 180 * measures.length;
    renderer.resize(width, height);
    const context = renderer.getContext();
    context.setFont('Arial', 10).setBackgroundFillStyle('transparent');

    measures.forEach((measurePredictions, measureIndex) => {
      const stave = new Stave(10, 40 + measureIndex * 180, width - 20);
      if (measureIndex === 0) {
        stave.addClef('treble').addTimeSignature('4/4');
      }
      stave.setContext(context).draw();

      const notes = [];
      measurePredictions.forEach((pred) => {
        console.log('Predicted chord:', pred.label);
        const chord = getChordNotes(pred.label);
        const staveNote = new StaveNote({
          clef: 'treble',
          keys: chord.keys,
          duration: 'q',
          auto_stem: true,
        });

        // Add accidentals where needed
        chord.accidentals.forEach((acc, idx) => {
          if (acc !== 'n') {
            const accidental = new Accidental(acc);
            staveNote.addModifier(accidental, idx);
          }
        });

        staveNote.setStyle({ fillStyle: 'white', strokeStyle: 'white' });
        notes.push(staveNote);
      });

      // Add rests if necessary
      const notesNeeded = chordsPerMeasure - notes.length;
      for (let i = 0; i < notesNeeded; i++) {
        const rest = new StaveNote({
          clef: 'treble',
          keys: ['b/4'],
          duration: 'qr',
          auto_stem: true,
        });
        rest.setStyle({ fillStyle: 'white', strokeStyle: 'white' });
        notes.push(rest);
      }

      const voice = new Voice({ num_beats: chordsPerMeasure, beat_value: 4 });
      voice.setMode(Voice.Mode.SOFT);
      voice.addTickables(notes);
      new Formatter().joinVoices([voice]).formatToStave([voice], stave);
      voice.draw(context, stave);
    });
  }, [predictions]);

  return (
    <div id="score-sheet-container">
      <div id="score-sheet"></div>
    </div>
  );
}

function getChordNotes(chordLabel) {
  // Define base positions for each root note (using middle C as reference)
  const basePositions = {
    'C': 4, 'D': 4, 'E': 4, 'F': 4, 'G': 4, 'A': 4, 'B': 4
  };

  // Comprehensive chord mapping
  const chordMap = {
    // Major chords
    'C': { keys: ['C/4', 'E/4', 'G/4'], accidentals: ['n', 'n', 'n'] },
    'C#': { keys: ['C#/4', 'E#/4', 'G#/4'], accidentals: ['#', '#', '#'] },
    'Db': { keys: ['Db/4', 'F/4', 'Ab/4'], accidentals: ['b', 'n', 'b'] },
    'D': { keys: ['D/4', 'F#/4', 'A/4'], accidentals: ['n', '#', 'n'] },
    'D#': { keys: ['D#/4', 'F##/4', 'A#/4'], accidentals: ['#', '##', '#'] },
    'Eb': { keys: ['Eb/4', 'G/4', 'Bb/4'], accidentals: ['b', 'n', 'b'] },
    'E': { keys: ['E/4', 'G#/4', 'B/4'], accidentals: ['n', '#', 'n'] },
    'F': { keys: ['F/4', 'A/4', 'C/5'], accidentals: ['n', 'n', 'n'] },
    'F#': { keys: ['F#/4', 'A#/4', 'C#/5'], accidentals: ['#', '#', '#'] },
    'Gb': { keys: ['Gb/4', 'Bb/4', 'Db/5'], accidentals: ['b', 'b', 'b'] },
    'G': { keys: ['G/4', 'B/4', 'D/5'], accidentals: ['n', 'n', 'n'] },
    'G#': { keys: ['G#/4', 'B#/4', 'D#/5'], accidentals: ['#', '#', '#'] },
    'Ab': { keys: ['Ab/4', 'C/5', 'Eb/5'], accidentals: ['b', 'n', 'b'] },
    'A': { keys: ['A/4', 'C#/5', 'E/5'], accidentals: ['n', '#', 'n'] },
    'A#': { keys: ['A#/4', 'C##/5', 'E#/5'], accidentals: ['#', '##', '#'] },
    'Bb': { keys: ['Bb/4', 'D/5', 'F/5'], accidentals: ['b', 'n', 'n'] },
    'B': { keys: ['B/4', 'D#/5', 'F#/5'], accidentals: ['n', '#', '#'] },

    // Minor chords
    'Cm': { keys: ['C/4', 'Eb/4', 'G/4'], accidentals: ['n', 'b', 'n'] },
    'C#m': { keys: ['C#/4', 'E/4', 'G#/4'], accidentals: ['#', 'n', '#'] },
    'Dm': { keys: ['D/4', 'F/4', 'A/4'], accidentals: ['n', 'n', 'n'] },
    'D#m': { keys: ['D#/4', 'F#/4', 'A#/4'], accidentals: ['#', '#', '#'] },
    'Ebm': { keys: ['Eb/4', 'Gb/4', 'Bb/4'], accidentals: ['b', 'b', 'b'] },
    'Em': { keys: ['E/4', 'G/4', 'B/4'], accidentals: ['n', 'n', 'n'] },
    'Fm': { keys: ['F/4', 'Ab/4', 'C/5'], accidentals: ['n', 'b', 'n'] },
    'F#m': { keys: ['F#/4', 'A/4', 'C#/5'], accidentals: ['#', 'n', '#'] },
    'Gm': { keys: ['G/4', 'Bb/4', 'D/5'], accidentals: ['n', 'b', 'n'] },
    'G#m': { keys: ['G#/4', 'B/4', 'D#/5'], accidentals: ['#', 'n', '#'] },
    'Am': { keys: ['A/4', 'C/5', 'E/5'], accidentals: ['n', 'n', 'n'] },
    'A#m': { keys: ['A#/4', 'C#/5', 'E#/5'], accidentals: ['#', '#', '#'] },
    'Bbm': { keys: ['Bb/4', 'Db/5', 'F/5'], accidentals: ['b', 'b', 'n'] },
    'Bm': { keys: ['B/4', 'D/5', 'F#/5'], accidentals: ['n', 'n', '#'] },

    // Diminished chords
    'Cdim': { keys: ['C/4', 'Eb/4', 'Gb/4'], accidentals: ['n', 'b', 'b'] },
    'C#dim': { keys: ['C#/4', 'E/4', 'G/4'], accidentals: ['#', 'n', 'n'] },
    'Ddim': { keys: ['D/4', 'F/4', 'Ab/4'], accidentals: ['n', 'n', 'b'] },
    'Ebdim': { keys: ['Eb/4', 'Gb/4', 'A/4'], accidentals: ['b', 'b', 'n'] },

    // Augmented chords
    'Caug': { keys: ['C/4', 'E/4', 'G#/4'], accidentals: ['n', 'n', '#'] },
    'C#aug': { keys: ['C#/4', 'E#/4', 'A/4'], accidentals: ['#', '#', 'n'] },
    'Daug': { keys: ['D/4', 'F#/4', 'A#/4'], accidentals: ['n', '#', '#'] },

    // Seventh chords
    'C7': { keys: ['C/4', 'E/4', 'G/4', 'Bb/4'], accidentals: ['n', 'n', 'n', 'b'] },
    'Cmaj7': { keys: ['C/4', 'E/4', 'G/4', 'B/4'], accidentals: ['n', 'n', 'n', 'n'] },
    'Cm7': { keys: ['C/4', 'Eb/4', 'G/4', 'Bb/4'], accidentals: ['n', 'b', 'n', 'b'] },
    'Cdim7': { keys: ['C/4', 'Eb/4', 'Gb/4', 'A/4'], accidentals: ['n', 'b', 'b', 'n'] }
  };

  if (!chordMap[chordLabel]) {
    console.warn(`Chord "${chordLabel}" not found in chordMap. Using default C major.`);
    return {
      keys: ['C/4', 'E/4', 'G/4'],
      accidentals: ['n', 'n', 'n'],
    };
  }

  return chordMap[chordLabel];
}

export default ScoreSheet;