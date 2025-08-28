#!/usr/bin/env python3
"""
Test script to verify the Python backend setup
"""

def test_imports():
    """Test if all required packages can be imported"""
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError:
        print("❌ Flask not available")
        return False
    
    try:
        import librosa
        print("✅ librosa imported successfully")
    except ImportError:
        print("❌ librosa not available")
        return False
    
    try:
        import numpy
        print("✅ numpy imported successfully")
    except ImportError:
        print("❌ numpy not available")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError:
        print("❌ requests not available")
        return False
    
    return True

def test_ollama_connection():
    """Test connection to Ollama"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama connection successful")
            return True
        else:
            print("❌ Ollama connection failed")
            return False
    except Exception as e:
        print(f"❌ Ollama connection error: {e}")
        return False

def main():
    print("🧪 Testing Python Backend Setup")
    print("=" * 40)
    
    # Test imports
    print("\n📦 Testing package imports...")
    imports_ok = test_imports()
    
    # Test Ollama connection
    print("\n🤖 Testing Ollama connection...")
    ollama_ok = test_ollama_connection()
    
    print("\n" + "=" * 40)
    if imports_ok and ollama_ok:
        print("🎉 All tests passed! Backend is ready to run.")
        print("\nTo start the backend:")
        print("  cd backend")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate")
        print("  pip install -r requirements.txt")
        print("  python app.py")
    else:
        print("❌ Some tests failed. Please check the setup.")
        if not imports_ok:
            print("   - Install missing Python packages")
        if not ollama_ok:
            print("   - Ensure Ollama is running (ollama serve)")

if __name__ == "__main__":
    main()
