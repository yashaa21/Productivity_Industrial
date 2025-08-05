#!/bin/bash

# Productivity Calculator Streamlit App Launcher
echo "🚀 Starting Productivity Calculator..."

# Check if virtual environment exists
if [ ! -d "productivity_env" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv productivity_env
    source productivity_env/bin/activate
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found. Activating..."
    source productivity_env/bin/activate
fi

# Run the Streamlit app
echo "📊 Launching Productivity Calculator..."
echo "🌐 The app will open in your browser at: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the app"
echo ""

streamlit run streamlit_app.py 