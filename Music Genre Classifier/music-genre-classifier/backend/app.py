from flask import Flask, request, jsonify
from flask_cors import CORS
import librosa
import numpy as np
import base64
import io
import tempfile
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'flac'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_audio_features(audio_path):
    """Extract comprehensive audio features using librosa"""
    try:
        # Load audio file - analyze first 15 seconds for faster processing
        y, sr = librosa.load(audio_path, duration=15)
        
        # Extract various audio features
        features = {}
        
        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        
        # MFCC features (Mel-frequency cepstral coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        # Rhythm features
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # Harmonic features
        harmonic = librosa.effects.harmonic(y)
        harmonic_percussive = librosa.effects.hpss(y)
        
        # Zero crossing rate
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
        
        # Root Mean Square Energy
        rms = librosa.feature.rms(y=y)[0]
        
        # Store features
        features['tempo'] = float(tempo)
        features['spectral_centroid_mean'] = float(np.mean(spectral_centroids))
        features['spectral_rolloff_mean'] = float(np.mean(spectral_rolloff))
        features['spectral_bandwidth_mean'] = float(np.mean(spectral_bandwidth))
        features['mfcc_mean'] = [float(np.mean(mfcc)) for mfcc in mfccs]
        features['zero_crossing_rate_mean'] = float(np.mean(zero_crossing_rate))
        features['rms_mean'] = float(np.mean(rms))
        features['harmonic_ratio'] = float(np.mean(harmonic_percussive[0]) / (np.mean(harmonic_percussive[0]) + np.mean(harmonic_percussive[1]) + 1e-8))
        
        return features, sr
        
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None, None

def analyze_genre_from_features(features, filename):
    """Analyze genre based on extracted audio features using improved rule-based classification"""
    
    tempo = features['tempo']
    spectral_centroid = features['spectral_centroid_mean']
    harmonic_ratio = features['harmonic_ratio']
    zero_crossing_rate = features['zero_crossing_rate_mean']
    rms_energy = features['rms_mean']
    
    # Initialize genre scores with more balanced starting points
    genre_scores = {
        'Electronic': 0,
        'Rock': 0,
        'Pop': 0,
        'Hip Hop': 0,
        'Jazz': 0,
        'Classical': 0,
        'Country': 0,
        'Blues': 0
    }
    
    # More nuanced tempo-based scoring
    if tempo >= 140:
        genre_scores['Electronic'] += 4
        genre_scores['Rock'] += 2
    elif tempo >= 125:
        genre_scores['Electronic'] += 3
        genre_scores['Rock'] += 3
        genre_scores['Pop'] += 2
    elif tempo >= 100:
        genre_scores['Rock'] += 4
        genre_scores['Pop'] += 3
        genre_scores['Electronic'] += 1
    elif tempo >= 85:
        genre_scores['Pop'] += 3
        genre_scores['Hip Hop'] += 4
        genre_scores['Rock'] += 2
    elif tempo >= 70:
        genre_scores['Hip Hop'] += 3
        genre_scores['Jazz'] += 2
        genre_scores['Pop'] += 1
    else:
        genre_scores['Classical'] += 3
        genre_scores['Jazz'] += 3
        genre_scores['Blues'] += 2
        genre_scores['Country'] += 1
    
    # Improved spectral centroid scoring with better thresholds
    if spectral_centroid > 2500:
        genre_scores['Electronic'] += 4
        genre_scores['Pop'] += 1
    elif spectral_centroid > 2000:
        genre_scores['Electronic'] += 3
        genre_scores['Pop'] += 2
        genre_scores['Rock'] += 1
    elif spectral_centroid > 1500:
        genre_scores['Rock'] += 3
        genre_scores['Pop'] += 2
        genre_scores['Electronic'] += 1
    elif spectral_centroid > 1000:
        genre_scores['Pop'] += 2
        genre_scores['Rock'] += 1
        genre_scores['Jazz'] += 1
        genre_scores['Hip Hop'] += 1
    else:
        genre_scores['Classical'] += 4
        genre_scores['Jazz'] += 2
        genre_scores['Blues'] += 2
        genre_scores['Country'] += 2
    
    # Enhanced harmonic ratio scoring
    if harmonic_ratio > 0.8:
        genre_scores['Classical'] += 4
        genre_scores['Jazz'] += 3
        genre_scores['Blues'] += 2
    elif harmonic_ratio > 0.6:
        genre_scores['Classical'] += 2
        genre_scores['Jazz'] += 3
        genre_scores['Blues'] += 2
        genre_scores['Country'] += 1
    elif harmonic_ratio > 0.4:
        genre_scores['Rock'] += 2
        genre_scores['Pop'] += 2
        genre_scores['Jazz'] += 1
        genre_scores['Hip Hop'] += 1
    else:
        genre_scores['Electronic'] += 3
        genre_scores['Hip Hop'] += 1
        genre_scores['Rock'] += 1
    
    # Improved zero crossing rate scoring
    if zero_crossing_rate > 0.15:
        genre_scores['Rock'] += 3
        genre_scores['Electronic'] += 2
        genre_scores['Hip Hop'] += 1
    elif zero_crossing_rate > 0.08:
        genre_scores['Rock'] += 2
        genre_scores['Pop'] += 2
        genre_scores['Electronic'] += 1
        genre_scores['Hip Hop'] += 1
    else:
        genre_scores['Classical'] += 2
        genre_scores['Jazz'] += 2
        genre_scores['Blues'] += 2
        genre_scores['Country'] += 1
        genre_scores['Hip Hop'] += 1
    
    # Add RMS energy-based scoring for better differentiation
    if rms_energy > 0.1:
        genre_scores['Rock'] += 2
        genre_scores['Electronic'] += 1
        genre_scores['Pop'] += 1
    elif rms_energy > 0.05:
        genre_scores['Pop'] += 1
        genre_scores['Hip Hop'] += 2
        genre_scores['Electronic'] += 1
    else:
        genre_scores['Classical'] += 1
        genre_scores['Jazz'] += 1
        genre_scores['Blues'] += 1
    
    # Apply genre-specific bonuses and penalties
    # Rock gets bonus for high energy and complexity
    if tempo >= 100 and rms_energy > 0.08:
        genre_scores['Rock'] += 2
    
    # Classical gets bonus for low tempo and high harmonic content
    if tempo < 80 and harmonic_ratio > 0.7:
        genre_scores['Classical'] += 3
    # Additional Classical bonus for very low brightness
    if spectral_centroid < 1000 and harmonic_ratio > 0.8:
        genre_scores['Classical'] += 2
    
    # Electronic gets bonus for high brightness and low harmonic content
    if spectral_centroid > 2000 and harmonic_ratio < 0.5:
        genre_scores['Electronic'] += 3
    # Additional Electronic bonus for very high brightness
    if spectral_centroid > 2500 and harmonic_ratio < 0.4:
        genre_scores['Electronic'] += 2
    
    # Hip Hop gets bonus for medium tempo and medium energy
    if 80 <= tempo <= 110 and rms_energy > 0.06:
        genre_scores['Hip Hop'] += 2
    # Additional Hip Hop bonus for rhythmic complexity
    if 80 <= tempo <= 110 and zero_crossing_rate > 0.08:
        genre_scores['Hip Hop'] += 1
    
    # Jazz gets bonus for medium tempo and high harmonic content
    if 70 <= tempo <= 120 and harmonic_ratio > 0.6:
        genre_scores['Jazz'] += 2
    
    # Find the genre with highest score
    best_genre = max(genre_scores, key=genre_scores.get)
    
    # Add confidence based on score difference
    max_score = max(genre_scores.values())
    other_scores = [score for genre, score in genre_scores.items() if genre != best_genre]
    score_diff = max_score - max(other_scores) if other_scores else 0
    
    if score_diff >= 4:
        confidence = "High"
    elif score_diff >= 2:
        confidence = "Medium"
    else:
        confidence = "Low"
    
    return best_genre, confidence

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    """Main endpoint for audio analysis"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only MP3, WAV, M4A, FLAC allowed'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_path)
        
        try:
            # Extract audio features
            features, sr = extract_audio_features(temp_path)
            
            if features is None:
                return jsonify({'error': 'Failed to extract audio features'}), 500
            
            # Analyze genre using fast rule-based classification
            genre, confidence = analyze_genre_from_features(features, filename)
            
            return jsonify({
                'genre': genre,
                'confidence': confidence,
                'model': 'Fast Rule-Based Classification',
                'features': {
                    'tempo': features['tempo'],
                    'spectral_centroid': features['spectral_centroid_mean'],
                    'harmonic_ratio': features['harmonic_ratio']
                }
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        print(f"Error in analyze_audio: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'audio-analyzer'})

@app.route('/debug', methods=['POST'])
def debug_analysis():
    """Debug endpoint to see feature extraction and scoring"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only MP3, WAV, M4A, FLAC allowed'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_path)
        
        try:
            # Extract audio features
            features, sr = extract_audio_features(temp_path)
            
            if features is None:
                return jsonify({'error': 'Failed to extract audio features'}), 500
            
            # Get genre scores for debugging
            tempo = features['tempo']
            spectral_centroid = features['spectral_centroid_mean']
            harmonic_ratio = features['harmonic_ratio']
            zero_crossing_rate = features['zero_crossing_rate_mean']
            rms_energy = features['rms_mean']
            
            # Calculate scores manually for debugging
            genre_scores = {
                'Electronic': 0,
                'Rock': 0,
                'Pop': 0,
                'Hip Hop': 0,
                'Jazz': 0,
                'Classical': 0,
                'Country': 0,
                'Blues': 0
            }
            
            # Apply the same scoring logic
            if tempo >= 140:
                genre_scores['Electronic'] += 4
                genre_scores['Rock'] += 2
            elif tempo >= 120:
                genre_scores['Electronic'] += 3
                genre_scores['Rock'] += 3
                genre_scores['Pop'] += 2
            elif tempo >= 100:
                genre_scores['Rock'] += 4
                genre_scores['Pop'] += 3
                genre_scores['Electronic'] += 1
            elif tempo >= 85:
                genre_scores['Pop'] += 3
                genre_scores['Hip Hop'] += 3
                genre_scores['Rock'] += 2
            elif tempo >= 70:
                genre_scores['Hip Hop'] += 2
                genre_scores['Jazz'] += 2
                genre_scores['Pop'] += 1
            else:
                genre_scores['Classical'] += 3
                genre_scores['Jazz'] += 3
                genre_scores['Blues'] += 2
                genre_scores['Country'] += 1
            
            if spectral_centroid > 2500:
                genre_scores['Electronic'] += 3
                genre_scores['Pop'] += 1
            elif spectral_centroid > 2000:
                genre_scores['Electronic'] += 2
                genre_scores['Pop'] += 2
                genre_scores['Rock'] += 1
            elif spectral_centroid > 1500:
                genre_scores['Rock'] += 3
                genre_scores['Pop'] += 2
                genre_scores['Electronic'] += 1
            elif spectral_centroid > 1000:
                genre_scores['Pop'] += 2
                genre_scores['Rock'] += 1
                genre_scores['Jazz'] += 1
            else:
                genre_scores['Classical'] += 3
                genre_scores['Jazz'] += 2
                genre_scores['Blues'] += 2
                genre_scores['Country'] += 2
            
            if harmonic_ratio > 0.8:
                genre_scores['Classical'] += 4
                genre_scores['Jazz'] += 3
                genre_scores['Blues'] += 2
            elif harmonic_ratio > 0.6:
                genre_scores['Classical'] += 2
                genre_scores['Jazz'] += 3
                genre_scores['Blues'] += 2
                genre_scores['Country'] += 1
            elif harmonic_ratio > 0.4:
                genre_scores['Rock'] += 2
                genre_scores['Pop'] += 2
                genre_scores['Jazz'] += 1
            else:
                genre_scores['Electronic'] += 2
                genre_scores['Hip Hop'] += 2
                genre_scores['Rock'] += 1
            
            if zero_crossing_rate > 0.15:
                genre_scores['Rock'] += 3
                genre_scores['Electronic'] += 2
                genre_scores['Hip Hop'] += 1
            elif zero_crossing_rate > 0.08:
                genre_scores['Rock'] += 2
                genre_scores['Pop'] += 2
                genre_scores['Electronic'] += 1
            else:
                genre_scores['Classical'] += 2
                genre_scores['Jazz'] += 2
                genre_scores['Blues'] += 2
                genre_scores['Country'] += 1
            
            if rms_energy > 0.1:
                genre_scores['Rock'] += 2
                genre_scores['Electronic'] += 1
                genre_scores['Pop'] += 1
            elif rms_energy > 0.05:
                genre_scores['Pop'] += 1
                genre_scores['Hip Hop'] += 1
            else:
                genre_scores['Classical'] += 1
                genre_scores['Jazz'] += 1
                genre_scores['Blues'] += 1
            
            # Apply genre-specific bonuses
            if tempo >= 100 and rms_energy > 0.08:
                genre_scores['Rock'] += 2
            
            if tempo < 80 and harmonic_ratio > 0.7:
                genre_scores['Classical'] += 2
            
            if spectral_centroid > 2000 and harmonic_ratio < 0.5:
                genre_scores['Electronic'] += 2
            
            if 70 <= tempo <= 120 and harmonic_ratio > 0.6:
                genre_scores['Jazz'] += 2
            
            return jsonify({
                'features': {
                    'tempo': tempo,
                    'spectral_centroid': spectral_centroid,
                    'harmonic_ratio': harmonic_ratio,
                    'zero_crossing_rate': zero_crossing_rate,
                    'rms_energy': rms_energy
                },
                'genre_scores': genre_scores,
                'best_genre': max(genre_scores, key=genre_scores.get),
                'max_score': max(genre_scores.values())
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        print(f"Error in debug_analysis: {e}")
        return jsonify({'error': f'Debug analysis failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("🎵 Audio Analysis Backend Starting...")
    print("🎯 Using fast rule-based genre classification")
    print("🚀 Server will start on http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
