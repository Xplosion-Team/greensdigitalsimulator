# 🔧 Troubleshooting Guide

Solutions to common problems when using Greens Digital Simulator.

---

## 📋 Table of Contents

1. [Installation Issues](#installation-issues)
2. [Import Errors](#import-errors)
3. [Voice Module Problems](#voice-module-problems)
4. [Web Interface Issues](#web-interface-issues)
5. [Simulation Errors](#simulation-errors)
6. [Data Format Problems](#data-format-problems)
7. [Performance Issues](#performance-issues)
8. [Deployment Issues](#deployment-issues)

---

## 1️⃣ Installation Issues

### Problem: `pip install -e .` fails

**Error Message**:
```
ERROR: File "setup.py" not found. Directory cannot be installed in editable mode
```

**Solution**:
```bash
# Make sure you're in the correct directory
cd /path/to/greensdigitalsimulator

# Verify pyproject.toml exists
ls pyproject.toml

# If it exists, try:
pip install --upgrade pip
pip install -e .
```

---

### Problem: Requirements installation fails

**Error Message**:
```
ERROR: Could not find a version that satisfies the requirement Flask==3.0.3
```

**Solution**:
```bash
# Update pip and setuptools
pip install --upgrade pip setuptools wheel

# Install requirements with fallback
pip install -r requirments.txt --use-deprecated=legacy-resolver

# Or install individually
pip install Flask pandas numpy matplotlib torch
```

---

### Problem: PyTorch installation issues

**Error Message**:
```
ERROR: Could not find a version of torch
```

**Solution**:

**For CPU-only (recommended for most users)**:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**For GPU (CUDA 11.8)**:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**For macOS (Apple Silicon)**:
```bash
pip install torch torchvision torchaudio
```

---

## 2️⃣ Import Errors

### Problem: `ModuleNotFoundError: No module named 't1dsim_ai'`

**Error Message**:
```python
ModuleNotFoundError: No module named 't1dsim_ai'
```

**Solutions**:

**Option 1**: Install in editable mode
```bash
cd /path/to/greensdigitalsimulator
pip install -e .
```

**Option 2**: Add to Python path
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from t1dsim_ai.individual_model import DigitalTwin
```

**Option 3**: Install as package
```bash
cd /path/to/greensdigitalsimulator
pip install .
```

---

### Problem: Import succeeds but class not found

**Error Message**:
```python
AttributeError: module 't1dsim_ai' has no attribute 'DigitalTwin'
```

**Solution**:
```python
# Wrong import
from t1dsim_ai import DigitalTwin  # ❌

# Correct import
from t1dsim_ai.individual_model import DigitalTwin  # ✅
```

---

## 3️⃣ Voice Module Problems

### Problem: Microphone not detected

**Error Message**:
```
OSError: No Default Input Device Available
```

**Solutions**:

**macOS**:
```bash
# Grant microphone permissions
# System Preferences → Security & Privacy → Microphone → Python/Terminal

# Install portaudio
brew install portaudio

# Reinstall pyaudio
pip uninstall pyaudio
pip install --global-option='build_ext' \
    --global-option='-I/opt/homebrew/include' \
    --global-option='-L/opt/homebrew/lib' pyaudio
```

**Linux**:
```bash
# Install audio dependencies
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev alsa-utils

# Test microphone
arecord -l

# Install pyaudio
pip install pyaudio
```

**Windows**:
```bash
# Install using pipwin
pip install pipwin
pipwin install pyaudio

# Or download wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl
```

---

### Problem: Speech recognition not working

**Error Message**:
```
speech_recognition.UnknownValueError: Could not understand audio
```

**Solutions**:

1. **Check internet connection** (Google API requires internet)
```python
# Test connection
import requests
try:
    requests.get('https://www.google.com', timeout=5)
    print("Internet connected")
except:
    print("No internet - voice recognition won't work")
```

2. **Adjust for ambient noise**
```python
from example.voice_module import VoiceFoodLogger

logger = VoiceFoodLogger()

# Increase timeout for ambient noise calibration
logger.recognizer.pause_threshold = 1.0
logger.recognizer.energy_threshold = 4000
```

3. **Test microphone**
```bash
cd example
python test_microphone.py
```

4. **Use manual input as fallback**
```python
# If voice fails, use manual entry
logger.parse_food_from_text("two apples and one banana")
```

---

### Problem: `ImportError: No module named 'pyaudio'`

**Solution**:

See installation instructions above for your platform. If issues persist:

```bash
# Alternative: Use voice-free version
cd example
# Edit app.py and set:
VOICE_MODULE_AVAILABLE = False
```

---

## 4️⃣ Web Interface Issues

### Problem: Port 5000 already in use

**Error Message**:
```
OSError: [Errno 48] Address already in use
```

**Solutions**:

**Option 1**: Use different port
```python
# Edit app.py
if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Change to 8080
```

**Option 2**: Kill process on port 5000

**macOS/Linux**:
```bash
# Find process
lsof -ti:5000

# Kill it
kill -9 $(lsof -ti:5000)
```

**Windows**:
```bash
# Find process
netstat -ano | findstr :5000

# Kill it (replace <PID> with actual PID)
taskkill /PID <PID> /F
```

---

### Problem: Flask app won't start

**Error Message**:
```
ImportError: cannot import name 'Flask'
```

**Solution**:
```bash
# Reinstall Flask
pip uninstall Flask
pip install Flask==3.0.3

# Verify installation
python -c "import flask; print(flask.__version__)"
```

---

### Problem: Static files not loading

**Symptoms**: CSS/JS not loading, broken images

**Solution**:
```python
# Check Flask static folder configuration
# In app.py, verify:
app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Ensure directory structure:
# example/
#   ├── app.py
#   ├── templates/
#   │   └── index.html
#   └── static/
#       ├── css/
#       └── js/
```

---

### Problem: CORS errors in browser

**Error Message** (in browser console):
```
Access to fetch at 'http://localhost:5000/simulate' has been blocked by CORS policy
```

**Solution**:
```bash
# Install flask-cors
pip install flask-cors

# Add to app.py
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
```

---

## 5️⃣ Simulation Errors

### Problem: `KeyError` on required columns

**Error Message**:
```python
KeyError: 'output_cgm'
```

**Solution**:
```python
import pandas as pd

# Check your data has all required columns
required_columns = [
    'output_cgm', 'input_insulin', 'input_meal_carbs',
    'heart_rate', 'sleep_efficiency', 'is_train',
    'feat_hour_of_day_sin', 'feat_hour_of_day_cos',
    'feat_is_weekend', 'heart_rate_WRTbaseline'
]

data = pd.read_csv("your_data.csv")
missing = [col for col in required_columns if col not in data.columns]

if missing:
    print(f"Missing columns: {missing}")
    
    # Add missing columns with defaults
    for col in missing:
        if col == 'output_cgm':
            data[col] = 110
        elif 'input_' in col:
            data[col] = 0
        else:
            data[col] = 0
```

---

### Problem: Simulation produces NaN values

**Error Message**:
```
RuntimeWarning: invalid value encountered in simulation
```

**Solutions**:

1. **Check input data ranges**
```python
# Verify data is in valid ranges
print("Glucose range:", data.output_cgm.min(), "-", data.output_cgm.max())
print("Insulin range:", data.input_insulin.min(), "-", data.input_insulin.max())

# Clip to valid ranges
data['output_cgm'] = data['output_cgm'].clip(20, 500)
data['input_insulin'] = data['input_insulin'].clip(0, 50)
data['input_meal_carbs'] = data['input_meal_carbs'].clip(0, 200)
```

2. **Check for missing values**
```python
# Find NaN values
print(data.isnull().sum())

# Fill missing values
data = data.fillna(method='ffill')  # Forward fill
```

3. **Verify model loaded correctly**
```python
from t1dsim_ai.individual_model import DigitalTwin

twin = DigitalTwin(n_digitalTwin=1)

# Check model is loaded
if twin.model is None:
    print("Error: Model not loaded!")
else:
    print("Model loaded successfully")
```

---

### Problem: FileNotFoundError for model weights

**Error Message**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'example_model/digital_twin_1.pt'
```

**Solution**:
```python
import os

# Check if model files exist
model_path = "example_model/"
if not os.path.exists(model_path):
    print(f"Error: {model_path} not found!")
    print("Available paths:", os.listdir('.'))
    
# Use correct path
from t1dsim_ai.individual_model import DigitalTwin

# If in example/ directory
twin = DigitalTwin(n_digitalTwin=1)

# If in root directory
os.chdir('example')
twin = DigitalTwin(n_digitalTwin=1)
```

---

## 6️⃣ Data Format Problems

### Problem: Date parsing errors

**Error Message**:
```
ValueError: time data '3/20/20 00:05' does not match format
```

**Solution**:
```python
import pandas as pd

# Explicitly specify date format
data = pd.read_csv("data.csv", parse_dates=['datetime_local'],
                   date_format='%m/%d/%y %H:%M')

# Or convert after loading
data['datetime_local'] = pd.to_datetime(data['datetime_local'], 
                                        format='%m/%d/%y %H:%M')
```

---

### Problem: Boolean column type mismatch

**Error Message**:
```
ValueError: cannot convert string 'TRUE' to bool
```

**Solution**:
```python
# CSV uses strings for booleans
data = pd.read_csv("data.csv")

# Convert to actual boolean
data['is_train'] = data['is_train'].map({'TRUE': True, 'FALSE': False})

# Or use numeric (1/0)
data['is_train'] = data['is_train'].map({'TRUE': 1, 'FALSE': 0})
```

---

## 7️⃣ Performance Issues

### Problem: Simulation is very slow

**Symptoms**: Takes > 10 seconds for 24-hour simulation

**Solutions**:

1. **Use CPU-optimized PyTorch**
```bash
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

2. **Reduce data size**
```python
# Simulate shorter periods
data_24h = data.iloc[0:288]  # 24 hours only
```

3. **Batch processing**
```python
# Process multiple simulations efficiently
results = []
for twin_id in range(5):
    twin = DigitalTwin(n_digitalTwin=twin_id)
    result = twin.simulate(data)
    results.append(result)
    del twin  # Free memory
```

---

### Problem: High memory usage

**Symptoms**: Python process using > 2GB RAM

**Solutions**:

1. **Clear unused data**
```python
import gc

# After simulation
results = twin.simulate(data)
del twin
gc.collect()
```

2. **Process in chunks**
```python
# Process data day by day
chunk_size = 288  # 24 hours
for i in range(0, len(data), chunk_size):
    chunk = data.iloc[i:i+chunk_size]
    result = twin.simulate(chunk)
    # Save result and free memory
    result.to_csv(f'output_{i}.csv')
    del result
```

---

## 8️⃣ Deployment Issues

### Problem: Render deployment fails

**Error Message**:
```
Build failed: Command "pip install -r requirements.txt" failed
```

**Solutions**:

1. **Check requirements.txt format**
```bash
# Ensure proper formatting (no typos, correct versions)
Flask==3.0.3
gunicorn==21.2.0
pandas==2.2.2
numpy==1.26.4
matplotlib==3.9.2
```

2. **Add runtime.txt**
```bash
# Create runtime.txt
echo "python-3.9.0" > runtime.txt
```

3. **Use production app**
```bash
# Ensure render.yaml points to app_production.py
# Start command: python app_production.py
```

---

### Problem: Render app crashes on startup

**Error Message**:
```
Application failed to start
```

**Solutions**:

1. **Check environment variables**
```bash
# In Render dashboard, set:
PYTHON_VERSION=3.9.0
PORT=8080
HOST=0.0.0.0
```

2. **Use gunicorn properly**
```python
# In app_production.py
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
```

3. **Check logs**
```bash
# In Render dashboard → Logs
# Look for specific error messages
```

---

## 🆘 Still Having Issues?

### Debugging Checklist

- [ ] Python version 3.9 or higher
- [ ] All dependencies installed (`pip list`)
- [ ] In correct directory
- [ ] Model files present
- [ ] Data formatted correctly
- [ ] No firewall blocking ports

### Get Help

1. **Check existing issues**: [GitHub Issues](https://github.com/Xplosion-Team/greensdigitalsimulator/issues)
2. **Search documentation**: [README.md](README.md), [API.md](API.md)
3. **Ask in discussions**: [GitHub Discussions](https://github.com/Xplosion-Team/greensdigitalsimulator/discussions)
4. **Open new issue**: Provide:
   - Error message (full stack trace)
   - Python version (`python --version`)
   - OS and version
   - Steps to reproduce
   - What you've tried

### Diagnostic Script

Run this to collect system information:

```python
import sys
import platform

print("=== System Information ===")
print(f"Python version: {sys.version}")
print(f"Platform: {platform.platform()}")

print("\n=== Package Versions ===")
try:
    import flask; print(f"Flask: {flask.__version__}")
except: print("Flask: NOT INSTALLED")

try:
    import pandas; print(f"Pandas: {pandas.__version__}")
except: print("Pandas: NOT INSTALLED")

try:
    import numpy; print(f"NumPy: {numpy.__version__}")
except: print("NumPy: NOT INSTALLED")

try:
    import torch; print(f"PyTorch: {torch.__version__}")
except: print("PyTorch: NOT INSTALLED")

try:
    import t1dsim_ai; print("t1dsim_ai: INSTALLED")
except: print("t1dsim_ai: NOT INSTALLED")

print("\n=== Directory Information ===")
import os
print(f"Current directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")
```

Save as `diagnostic.py` and run:
```bash
python diagnostic.py
```

---

<div align="center">

**Troubleshooting guide for Greens Digital Simulator** 🔧

[Back to README](README.md) • [Quick Start](QUICKSTART.md) • [Examples](EXAMPLES.md)

</div>
