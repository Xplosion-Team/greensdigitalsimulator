#!/bin/bash

# T1D Simulator Voice-Enabled Deployment Script
# This script helps prepare and deploy to Render

echo "🚀 T1D Simulator Voice-Enabled Deployment Script"
echo "================================================"

# Check if we're in the right directory
if [ ! -f "app_production.py" ]; then
    echo "❌ Error: app_production.py not found!"
    echo "Please run this script from the example/ directory"
    exit 1
fi

echo "✅ Found app_production.py"

# Check for required files
required_files=(
    "requirements.txt"
    "render.yaml"
    "voice_module.py"
    "templates/index.html"
    "data_example/data_example.csv"
)

echo "📋 Checking required files..."
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
    fi
done

echo ""
echo "🔧 Environment Variables to set in Render:"
echo "=========================================="
echo ""
echo "Core Application:"
echo "PYTHON_VERSION=3.9.0"
echo "FLASK_ENV=production"
echo "FLASK_DEBUG=false"
echo "PORT=8080"
echo "HOST=0.0.0.0"
echo ""
echo "Voice Module Configuration:"
echo "VOICE_ENABLED=true"
echo "SPEECH_RECOGNITION_ENABLED=true"
echo "TTS_ENABLED=false"
echo "FLAC_PATH=/usr/bin/flac"
echo "MICROPHONE_PERMISSIONS=enabled"
echo "GOOGLE_SPEECH_API_KEY="
echo ""
echo "Feature Flags:"
echo "FOOD_LOG_ENABLED=true"
echo "NUTRITION_ANALYSIS_ENABLED=true"
echo "SIMULATION_UPDATE_ENABLED=true"
echo ""

echo "📝 Deployment Steps:"
echo "==================="
echo "1. Push your code to GitHub"
echo "2. Go to https://dashboard.render.com"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Connect your GitHub repository"
echo "5. Configure:"
echo "   - Name: t1d-simulator-voice"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python app_production.py"
echo "   - Plan: Starter (free)"
echo "6. Add the environment variables listed above"
echo "7. Click 'Create Web Service'"
echo "8. Wait for deployment (5-10 minutes)"
echo ""

echo "🔍 Troubleshooting Tips:"
echo "======================="
echo "• Check Render logs for errors"
echo "• Voice recognition may not work on Render (use manual entry)"
echo "• TTS is disabled on Render (no audio output)"
echo "• All other features should work normally"
echo ""

echo "🌐 Your app will be available at:"
echo "https://your-app-name.onrender.com"
echo ""

echo "✅ Ready for deployment!"
echo "Good luck! 🎉"
