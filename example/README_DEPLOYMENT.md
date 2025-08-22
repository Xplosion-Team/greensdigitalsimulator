# 🚀 T1D Simulator Voice-Enabled - Render Deployment

Your enhanced T1D Simulator with voice-enabled nutrition analysis is ready for deployment to Render!

## 📁 Project Structure

```
example/
├── app_production.py          # Production Flask app
├── requirements.txt           # Python dependencies
├── render.yaml               # Render configuration
├── voice_module.py           # Voice recognition module
├── templates/
│   └── index.html            # Web interface
├── data_example/
│   └── data_example.csv      # Sample data
├── deploy_to_render.sh       # Deployment helper script
├── RENDER_DEPLOYMENT.md      # Detailed deployment guide
└── README_DEPLOYMENT.md      # This file
```

## 🎯 What's Included

### ✅ Core Features
- **T1D Digital Twin Simulation**: Real-time glucose prediction
- **Interactive Web Interface**: Beautiful charts and controls
- **Voice Food Logging**: Speech-to-text food recognition
- **Nutrition Analysis**: Carbs, protein, fat, fiber calculation
- **Blood Sugar Impact**: Predict glucose response to meals
- **Food Logging**: Track meals and nutrition over time
- **Statistics Dashboard**: Time-in-range, mean, min, max

### 🎤 Voice Features
- **Speech Recognition**: "I ate an apple" → automatic logging
- **Food Database**: 50+ common foods with nutrition data
- **Quantity Detection**: "Two slices of bread" → 2 servings
- **Real-time Processing**: Instant nutrition calculation

### 📊 Enhanced UI
- **Progress Bars**: Visual nutrition breakdown
- **Glycemic Indicators**: Blood sugar impact warnings
- **Quick Add Buttons**: Common foods with one click
- **Responsive Design**: Works on desktop and mobile

## 🚀 Quick Deploy

### Option 1: Automated Script
```bash
./deploy_to_render.sh
```

### Option 2: Manual Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add voice-enabled T1D simulator"
   git push origin main
   ```

2. **Create Render Service**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   - **Name**: `t1d-simulator-voice`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app_production.py`
   - **Plan**: `Starter` (free)

4. **Set Environment Variables**
   ```
   PYTHON_VERSION=3.9.0
   FLASK_ENV=production
   FLASK_DEBUG=false
   PORT=8080
   HOST=0.0.0.0
   VOICE_ENABLED=true
   SPEECH_RECOGNITION_ENABLED=true
   TTS_ENABLED=false
   FOOD_LOG_ENABLED=true
   NUTRITION_ANALYSIS_ENABLED=true
   SIMULATION_UPDATE_ENABLED=true
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes
   - Access at `https://your-app-name.onrender.com`

## 🔧 Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `PYTHON_VERSION` | `3.9.0` | Python version |
| `FLASK_ENV` | `production` | Flask environment |
| `PORT` | `8080` | Port to bind |
| `VOICE_ENABLED` | `true` | Enable voice features |
| `TTS_ENABLED` | `false` | Disable TTS (Render limitation) |

## 📱 Features on Render

### ✅ Fully Working
- **T1D Simulation**: Complete digital twin functionality
- **Web Interface**: All interactive features
- **Manual Food Entry**: Add foods via web form
- **Nutrition Analysis**: Calculate all nutrition values
- **Blood Sugar Impact**: Predict glucose response
- **Food Logging**: Track and display meals
- **Statistics**: Time-in-range, averages, etc.

### ⚠️ Limited on Render
- **Voice Recognition**: May not work (microphone access)
- **Text-to-Speech**: Disabled (no audio output)

### 🔄 Fallback Options
- **Manual Food Entry**: Use web interface
- **Quick Add Buttons**: Pre-defined common foods
- **Nutrition Calculator**: Manual analysis

## 🎮 How to Use

### 1. Access the App
- Open your deployed URL
- You'll see the T1D simulation dashboard

### 2. Voice Food Logging (if available)
- Click "Start Voice Logging"
- Say "I ate an apple" or similar
- Watch the nutrition analysis update

### 3. Manual Food Entry
- Use the "Manual Food Entry" section
- Type food name, quantity, and unit
- Click "Log Food"

### 4. Quick Add Foods
- Click "Apple", "Bread", "Rice", or "Pizza"
- Instantly add common foods

### 5. View Analysis
- See nutrition breakdown (carbs, protein, fat, fiber)
- Check blood sugar impact prediction
- View glycemic index indicator

### 6. Monitor Simulation
- Watch the T1D simulation update
- See how your meal affects glucose levels
- Check statistics and time-in-range

## 🔍 Troubleshooting

### Common Issues

**Build Fails**
- Check `requirements.txt` for compatibility
- Ensure all files are in the repository

**Voice Not Working**
- Normal on Render (microphone limitations)
- Use manual food entry instead

**Import Errors**
- Verify `src/` directory is included
- Check Python version compatibility

**App Won't Start**
- Ensure `PORT=8080` environment variable
- Check Render logs for errors

### Debug Steps
1. Check Render deployment logs
2. Verify environment variables
3. Test locally first
4. Contact Render support if needed

## 📊 Performance

### Render Free Tier Limits
- **Build Time**: 5-10 minutes
- **Cold Start**: 30-60 seconds
- **Memory**: 512MB
- **CPU**: Shared

### Optimization Tips
- Use manual food entry for faster response
- Keep food log entries minimal
- Monitor Render usage dashboard

## 🎉 Success!

Once deployed, you'll have:
- ✅ **Live T1D Simulator** accessible worldwide
- ✅ **Voice-enabled nutrition tracking**
- ✅ **Real-time glucose prediction**
- ✅ **Beautiful interactive interface**
- ✅ **Comprehensive food logging**

## 📞 Support

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Voice Module**: See `VOICE_MODULE_README.md`

---

**Your enhanced T1D Simulator is ready for the world! 🌍**
