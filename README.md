
# Chordify 🎸

Chordify is a web application designed to detect and display guitar chords from audio files. Leveraging machine learning and audio processing, this app transforms sound into visual notation, making it easy to follow along with guitar chords.

🔗 **Live App**: [Chordify on Render](https://chordify-xu4e.onrender.com/)

---

## 📜 Table of Contents

- [About the Project](#about-the-project)
- [Showcase](#showcase)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🔍 About the Project

Chordify uses machine learning algorithms to recognize guitar chords from audio input and display them in a musical notation format. The project aims to provide musicians and learners with a seamless experience for visualizing chords from their favorite songs.

## 🎬 Showcase

<img src='./showcase.gif'>
*Example of chord detection and display in action.*

---

## ✨ Features

- **Chord Detection**: Identifies chords in guitar audio recordings.
- **Music Notation Display**: Converts detected chords into readable musical notation.
- **Responsive Design**: Adapts to various screen sizes for easy viewing.
- **Easy-to-Use Interface**: Simple and clean UI for seamless interaction.

---

## 💻 Tech Stack

- **Frontend**: React, VexFlow
- **Backend**: Flask, TensorFlow, librosa
- **Deployment**: Render.com
- **Other Libraries**: `flask-cors`, `joblib`, `scikit-learn`, `ABCJS`

---

## 🚀 Installation

### Prerequisites

- **Node.js** and **npm** for frontend setup.
- **Python 3** and **pip** for backend setup.

### Clone the Repository

```bash
git clone https://github.com/your-username/chordify.git
cd chordify
```

### Backend Setup

1. **Navigate to the API folder**:
   ```bash
   cd api
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Flask server**:
   ```bash
   python app.py
   ```

### Frontend Setup

1. **Navigate to the frontend folder**:
   ```bash
   cd ../frontend
   ```

2. **Install the required dependencies**:
   ```bash
   npm install
   ```

3. **Start the React app**:
   ```bash
   npm start
   ```

---

## 🕹️ Usage

1. **Upload a Guitar Audio File**: The app accepts isolated guitar tracks for chord detection.
2. **View Detected Chords**: Detected chords will appear as readable notation, allowing you to follow along.

*For best results, use isolated guitar audio files, as mixed instrument tracks may affect chord recognition accuracy.*

---

## 🌐 Deployment

The app is deployed on [Render.com](https://render.com) using the following steps:

1. **Backend Deployment**: Render Web Service using Python environment.
2. **Frontend Deployment**: Render Static Site using npm build.

*Check the [Render Documentation](https://render.com/docs) for further deployment guidance.*

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/AmazingFeature`.
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`.
4. Push to the branch: `git push origin feature/AmazingFeature`.
5. Open a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

Feel free to reach out with questions or suggestions, and enjoy using Chordify! 🎶
