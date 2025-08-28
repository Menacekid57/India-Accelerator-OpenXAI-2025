# Music Genre Classifier - Setup Guide

## What Changed

### Before (Filename Analysis)
- ❌ Only analyzed the filename for genre hints
- ❌ No actual audio content analysis
- ❌ Limited accuracy based on naming conventions

### After (Real Audio Analysis)
- ✅ **Extracts actual audio features** using librosa
- ✅ **Analyzes spectral characteristics** (brightness, frequency content)
- ✅ **Measures tempo and rhythm** (BPM, beat tracking)
- ✅ **Analyzes harmonic content** (musical vs noise ratio)
- ✅ **Uses MFCC coefficients** for timbre analysis
- ✅ **Much higher accuracy** in genre classification

## New Architecture

```
Frontend (Next.js) → Python Backend (Flask + librosa) → Ollama (AI Analysis)
     ↓                      ↓                           ↓
  File Upload         Audio Feature Extraction      Genre Classification
  (MP3/WAV/etc)      (Spectral, MFCC, Tempo)      (AI-powered)
```

## Quick Start

### 1. One-Command Launch (Recommended)
```bash
./start_full_app.sh
```

### 2. Manual Launch
```bash
# Terminal 1: Start Python Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# Terminal 2: Start Next.js Frontend
npm run dev
```

## What the System Now Does

1. **Upload Audio File**: Accepts MP3, WAV, M4A, FLAC
2. **Extract Features**: 
   - Tempo (BPM)
   - Spectral centroid (brightness)
   - Harmonic ratio (musical content)
   - MFCC coefficients (timbre)
   - Energy levels and complexity
3. **AI Analysis**: Sends extracted features to Ollama
4. **Genre Classification**: Returns genre + confidence + audio metrics

## Testing the Setup

```bash
cd backend
python3 test_setup.py
```

This will verify:
- ✅ Python packages are available
- ✅ Ollama connection works
- ✅ Backend is ready to run

## Troubleshooting

### Python Dependencies
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Ollama Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

### Port Conflicts
- Backend: http://localhost:5000
- Frontend: http://localhost:3000
- Ollama: http://localhost:11434

## File Structure

```
├── src/app/                 # Next.js frontend
│   ├── page.js             # Main page (updated for audio analysis)
│   └── layout.js           # App layout
├── backend/                 # Python Flask backend
│   ├── app.py              # Main Flask app with audio analysis
│   ├── requirements.txt    # Python dependencies
│   ├── test_setup.py      # Setup verification script
│   └── start_backend.sh    # Backend startup script
├── start_full_app.sh       # Complete application startup
└── README.md               # Comprehensive documentation
```

## Benefits of the New System

- 🎯 **Higher Accuracy**: Real audio analysis vs filename guessing
- 🔬 **Scientific Approach**: Uses established audio processing techniques
- 📊 **Rich Data**: Shows tempo, brightness, harmonic content
- 🚀 **Scalable**: Easy to add more audio features
- 🎵 **Genre-Aware**: Considers musical characteristics, not just names

## Next Steps

The system is now ready for:
- Production deployment
- Additional audio features
- Custom genre models
- Batch processing
- API integration with other services
