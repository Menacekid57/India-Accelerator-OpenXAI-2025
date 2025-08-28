'use client';

import { useState } from 'react';
import { Upload, Music, Loader2, FileAudio, Waveform } from 'lucide-react';

export default function Home() {
  const [file, setFile] = useState(null);
  const [genre, setGenre] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [features, setFeatures] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'audio/mpeg') {
      setFile(selectedFile);
      setError('');
      setGenre('');
      setFeatures(null);
    } else {
      setError('Please select a valid MP3 file');
      setFile(null);
    }
  };

  const classifyGenre = async () => {
    if (!file) return;

    setLoading(true);
    setError('');
    setGenre('');
    setFeatures(null);

    try {
      // Create FormData to send file to Python backend
      const formData = new FormData();
      formData.append('audio', file);
      
      // Call Python backend API
      const response = await fetch('http://localhost:5001/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to analyze audio');
      }

      const result = await response.json();
      setGenre(result.genre);
      setFeatures(result.features);
    } catch (err) {
      setError('Error analyzing audio: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen custom-gradient text-white">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto text-center">
          <div className="mb-8">
            <Music className="w-16 h-16 mx-auto mb-4 text-purple-300" />
            <h1 className="text-4xl font-bold mb-4">Music Genre Classifier</h1>
          </div>

          <div className="bg-slate-800/90 backdrop-blur-lg rounded-2xl p-8 border border-purple-500/30 shadow-2xl">
            <div className="mb-6">
              <label className="block text-sm font-medium mb-2 text-purple-200">
                Select MP3 File
              </label>
              <div className="border-2 border-dashed border-purple-400 rounded-lg p-6 hover:border-purple-300 transition-colors bg-slate-900/60">
                <input
                  type="file"
                  accept=".mp3,audio/mpeg"
                  onChange={handleFileChange}
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer flex flex-col items-center"
                >
                  <Upload className="w-12 h-12 text-purple-300 mb-3" />
                  <span className="text-lg font-medium">
                    {file ? file.name : 'Choose MP3 file'}
                  </span>
                  <span className="text-sm text-purple-300/70 mt-1">
                    or drag and drop
                  </span>
                </label>
              </div>
            </div>

            {file && (
              <div className="mb-6 p-4 bg-purple-600/30 rounded-lg border border-purple-400/40 bg-slate-800/60">
                <div className="flex items-center justify-center space-x-2">
                  <FileAudio className="w-5 h-5 text-purple-300" />
                  <span className="font-medium">{file.name}</span>
                  <span className="text-sm text-purple-200">
                    ({(file.size / 1024 / 1024).toFixed(2)} MB)
                  </span>
                </div>
              </div>
            )}

            {error && (
              <div className="mb-6 p-4 bg-red-600/30 rounded-lg border border-red-400/40 text-red-200 bg-slate-800/60">
                {error}
              </div>
            )}

            <button
              onClick={classifyGenre}
              disabled={!file || loading}
              className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg"
            >
              {loading ? (
                <div className="flex items-center justify-center space-x-2">
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Analyzing Audio...</span>
                </div>
              ) : (
                'Analyze Audio & Classify Genre'
              )}
            </button>

            {genre && (
              <div className="mt-6 p-6 bg-emerald-600/30 rounded-lg border border-emerald-400/40 bg-slate-800/60">
                <h3 className="text-lg font-semibold mb-2 text-emerald-200">
                  Genre Detected:
                </h3>
                <p className="text-2xl font-bold text-emerald-100">{genre}</p>
                <p className="text-sm text-emerald-200 mt-2">
                  Based on actual audio analysis using AI
                </p>
                
                {features && (
                  <div className="mt-4 p-4 bg-emerald-700/30 rounded-lg bg-slate-700/40">
                    <h4 className="text-sm font-semibold mb-2 text-emerald-200">
                      Audio Features:
                    </h4>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <span className="text-emerald-300">Tempo:</span>
                        <br />
                        <span className="font-mono text-emerald-100">{features.tempo} BPM</span>
                      </div>
                      <div>
                        <span className="text-emerald-300">Brightness:</span>
                        <br />
                        <span className="font-mono text-emerald-100">{features.spectral_centroid?.toFixed(0)} Hz</span>
                      </div>
                      <div>
                        <span className="text-emerald-300">Harmonic:</span>
                        <br />
                        <span className="font-mono text-emerald-100">{(features.harmonic_ratio * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
