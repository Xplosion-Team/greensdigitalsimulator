# T1D Simulator Voice-Enabled Deployment Guide

## 🚀 Deploy to Render

This guide will help you deploy your enhanced T1D Simulator with voice-enabled nutrition analysis to Render.

## 📋 Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Environment Variables**: Configure the necessary environment variables

## 🔧 Deployment Steps

### Step 1: Prepare Your Repository

Ensure your repository contains these files:
- `app_production.py` - Production Flask app
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration
- `voice_module.py` - Voice recognition module
- `templates/index.html` - Web interface
- `data_example/data_example.csv` - Sample data

### Step 2: Create Render Web Service

1. **Go to Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service**:
   - **Name**: `t1d-simulator-voice`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app_production.py`
   - **Plan**: `Starter` (free tier)

### Step 3: Set Environment Variables

In your Render service settings, add these environment variables:

#### Core Application
```
PYTHON_VERSION=3.9.0
FLASK_ENV=production
FLASK_DEBUG=false
PORT=8080
HOST=0.0.0.0
```

#### Voice Module Configuration
```
VOICE_ENABLED=true
SPEECH_RECOGNITION_ENABLED=true
TTS_ENABLED=false
FLAC_PATH=/usr/bin/flac
MICROPHONE_PERMISSIONS=enabled
GOOGLE_SPEECH_API_KEY=
```

#### Feature Flags
```
FOOD_LOG_ENABLED=true
NUTRITION_ANALYSIS_ENABLED=true
SIMULATION_UPDATE_ENABLED=true
```

### Step 4: Deploy

1. **Click "Create Web Service"**
2. **Wait for deployment** (5-10 minutes)
3. **Check logs** for any errors
4. **Access your app** at the provided URL

## 🔍 Troubleshooting

### Common Issues

#### 1. Build Failures
**Problem**: Dependencies not installing
**Solution**: Check `requirements.txt` and ensure all packages are compatible

#### 2. Voice Module Not Working
**Problem**: Speech recognition fails
**Solution**: 
- Set `TTS_ENABLED=false` (TTS doesn't work on Render)
- Use manual food entry as fallback
- Check microphone permissions

#### 3. Import Errors
**Problem**: T1DSim_AI module not found
**Solution**: Ensure the `src/` directory is properly included

#### 4. Port Issues
**Problem**: App not starting
**Solution**: Ensure `PORT` environment variable is set to `8080`

### Debug Commands

Check your deployment logs in Render dashboard for:
- Python import errors
- Missing dependencies
- Environment variable issues
- Port binding problems

## 🌐 Access Your App

Once deployed, your app will be available at:
```
https://your-app-name.onrender.com
```

## 🔧 Environment Variable Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `PYTHON_VERSION` | `3.9.0` | Python version to use |
| `FLASK_ENV` | `production` | Flask environment |
| `FLASK_DEBUG` | `false` | Enable debug mode |
| `PORT` | `8080` | Port to bind to |
| `HOST` | `0.0.0.0` | Host to bind to |
| `VOICE_ENABLED` | `true` | Enable voice features |
| `SPEECH_RECOGNITION_ENABLED` | `true` | Enable speech recognition |
| `TTS_ENABLED` | `false` | Enable text-to-speech |
| `FOOD_LOG_ENABLED` | `true` | Enable food logging |
| `NUTRITION_ANALYSIS_ENABLED` | `true` | Enable nutrition analysis |

## 📱 Features Available on Render

### ✅ Working Features
- **T1D Simulation**: Full digital twin simulation
- **Web Interface**: Interactive charts and controls
- **Manual Food Entry**: Add foods via web interface
- **Nutrition Analysis**: Calculate carbs, protein, fat, fiber
- **Blood Sugar Impact**: Predict glucose response
- **Food Logging**: Track meals and nutrition
- **Statistics**: Time-in-range, mean, min, max

### ⚠️ Limited Features
- **Voice Recognition**: May not work due to microphone access
- **Text-to-Speech**: Disabled on Render (no audio output)
- **Real-time Voice**: Requires microphone permissions

### 🔄 Fallback Options
- **Manual Food Entry**: Use the web interface to log foods
- **Quick Add Buttons**: Pre-defined common foods
- **Nutrition Calculator**: Manual nutrition analysis

## 🚀 Next Steps

1. **Test the deployment**: Verify all features work
2. **Monitor logs**: Check for any errors
3. **Customize**: Add your own data or models
4. **Scale**: Upgrade to paid plan if needed

## 📞 Support

If you encounter issues:
1. Check the Render deployment logs
2. Verify environment variables
3. Test locally first
4. Contact Render support if needed

---

**Happy Deploying! 🎉**
