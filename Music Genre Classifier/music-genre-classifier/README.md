# Music Genre Classifier

A full-stack web application that uses AI to classify music genres from MP3 files by analyzing actual audio content. Built with Next.js frontend and Python Flask backend, powered by Ollama.

## Features

- 🎵 Upload MP3 files through a beautiful web interface
- 🧠 **Real audio analysis** using librosa (spectral features, MFCC, tempo, harmonics)
- 🤖 AI-powered genre classification using Ollama
- 📊 Display of extracted audio features (tempo, brightness, harmonic ratio)
- 🎨 Modern, responsive UI with Tailwind CSS
- ⚡ Fast and efficient audio processing
- 📱 Mobile-friendly design

## Architecture

- **Frontend**: Next.js 15 with React 19
- **Backend**: Python Flask with librosa audio analysis
- **AI**: Ollama with llama3:latest model
- **Audio Processing**: librosa for feature extraction

## Prerequisites

- Node.js 18+ installed
- Python 3.8+ installed
- Ollama installed and running locally
- A music model available in Ollama (e.g., llama3:latest)

## Quick Start

### Option 1: One-Command Startup (Recommended)
```bash
./start_full_app.sh
```

This script will:
- Set up Python virtual environment
- Install all dependencies
- Start both backend and frontend servers
- Open the application at http://localhost:3000

### Option 2: Manual Setup

#### 1. Install Node.js Dependencies
```bash
npm install
```

#### 2. Set up Python Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. Start Backend Server
```bash
cd backend
python app.py
```
Backend will run on http://localhost:5000

#### 4. Start Frontend Server (in new terminal)
```bash
npm run dev
```
Frontend will run on http://localhost:3000

## How It Works

1. **File Upload**: Users upload MP3 files through the web interface
2. **Audio Processing**: Python backend uses librosa to extract audio features:
   - Spectral features (centroid, rolloff, bandwidth)
   - MFCC coefficients (mel-frequency cepstral coefficients)
   - Rhythm features (tempo, beat tracking)
   - Harmonic analysis (harmonic vs percussive separation)
   - Energy features (RMS, zero crossing rate)
3. **Feature Analysis**: Extracted features are sent to Ollama with a specialized prompt
4. **Genre Classification**: Ollama analyzes the audio characteristics and determines the genre
5. **Result Display**: Genre and audio features are displayed to the user

## Audio Features Extracted

- **Tempo**: Beats per minute (BPM)
- **Spectral Centroid**: Indicates brightness of the sound
- **Spectral Rolloff**: High-frequency content analysis
- **Spectral Bandwidth**: Frequency spread of the audio
- **MFCC**: Mel-frequency cepstral coefficients for timbre analysis
- **Harmonic Ratio**: Musical vs noise content ratio
- **Zero Crossing Rate**: Audio complexity indicator
- **RMS Energy**: Overall audio energy level

## Supported Genres

The system can detect various music genres including:
- Rock, Jazz, Hip Hop, Classical
- Electronic, Pop, Country, Blues
- Reggae, Folk, R&B, Metal
- Punk, Indie, Alternative, World Music

## Configuration

### Backend Configuration (`backend/app.py`)
- Change Ollama model: Update `MODEL_NAME` variable
- Adjust audio analysis: Modify `extract_audio_features()` function
- Customize prompts: Edit the `analyze_genre_from_features()` function

### Frontend Configuration
- Backend URL: Update the fetch URL in `page.js` if needed
- UI customization: Modify Tailwind classes and components

## Troubleshooting

- **Backend Connection Error**: Ensure Python backend is running on port 5000
- **Ollama Connection Error**: Ensure Ollama is running on `localhost:11434`
- **Audio Processing Error**: Check that the audio file is valid and not corrupted
- **Python Dependencies**: Ensure all requirements are installed in the virtual environment

## Development

### Backend Development
- Audio analysis algorithms in `backend/app.py`
- Add new audio features in `extract_audio_features()`
- Customize Ollama prompts for different analysis types

### Frontend Development
- React components in `src/app/`
- Styling with Tailwind CSS
- API integration with Python backend

## File Structure

```
music-genre-classifier/
├── src/app/                 # Next.js frontend
│   ├── page.js             # Main application page
│   └── layout.js           # App layout
├── backend/                 # Python Flask backend
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── start_backend.sh    # Backend startup script
├── start_full_app.sh       # Complete application startup
├── package.json            # Node.js dependencies
└── README.md               # This file
```

## License

MIT License - feel free to use and modify as needed!
