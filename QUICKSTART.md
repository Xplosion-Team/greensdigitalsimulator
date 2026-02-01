# 🚀 Quick Start Guide

Get up and running with Greens Digital Simulator in 5 minutes!

---

## ⚡ 1-Minute Setup

```bash
# Clone and install
git clone https://github.com/Xplosion-Team/greensdigitalsimulator.git
cd builtin/greensdigitalsimulator

# Setup virtual environment (Mac/Linux)
python3 -m venv .venv
source .venv/bin/activate

# Install the package and dependencies
pip install -e .
pip install -r requirments.txt
```

> [!TIP]
> Always ensure your virtual environment is active (`source .venv/bin/activate`) before running any commands!

---

## 🎯 Your First Simulation (2 minutes)

### Option 1: Command Line

```bash
cd example
python runDigitalTwin.py
```

**What happens?**
- Loads a pre-trained digital twin
- Simulates 24 hours of glucose dynamics using `data_example/data_example.csv`
- Generates a 500 DPI visualization saved to `img/example_digitaltwin4.png`

**Output**: A high-quality chart showing glucose predictions vs actual CGM data!

---

### Option 2: Web Interface

```bash
cd example
python app.py
```

Then open your browser to: **http://localhost:5000**

**What you'll see?**
- 📊 Interactive glucose chart
- 🎮 Controls for simulation parameters
- 🎤 Voice food logging (if microphone available)
- 📈 Real-time statistics

---

## 🎨 Try These Examples

### Example 1: Compare Digital Twins

```python
from t1dsim_ai.individual_model import DigitalTwin
import pandas as pd

# Load sample data
data = pd.read_csv("data_example/data_example.csv")
data = data[~data.is_train].head(288)  # 24 hours

# Try different digital twins (0-4)
for twin_id in [0, 1, 2]:
    twin = DigitalTwin(n_digitalTwin=twin_id)
    results = twin.simulate(data)
    print(f"Twin {twin_id}: Mean glucose = {results.cgm_NNDT.mean():.1f} mg/dL")
```

---

### Example 2: Voice Food Logging

```bash
cd example
python debug_voice.py
```

Then speak: **"I ate two apples and a slice of bread"**

**Output**: Automatic carb calculation and nutrition info!

---

### Example 3: Custom Scenario

```python
from t1dsim_ai.create_scenarios import create_custom_scenario
from t1dsim_ai.individual_model import DigitalTwin

# Create a custom meal scenario
scenario = create_custom_scenario(
    initial_glucose=120,    # Starting at 120 mg/dL
    meal_carbs=60,          # 60g carb meal
    basal_insulin=1.0,      # 1.0 U/h basal
    meal_time=60            # Meal at 1 hour
)

# Simulate
twin = DigitalTwin(n_digitalTwin=1)
results = twin.simulate(scenario)

print(f"Peak glucose: {results.cgm_NNDT.max():.1f} mg/dL")
print(f"Time to peak: {results.cgm_NNDT.idxmax() * 5} minutes")
```

---

## 🎓 Next Steps

### Learn More
- 📖 Read the full [README.md](README.md) for detailed documentation
- 🔬 Check `example/` directory for more Python scripts
- 🌐 Explore the web app features

### Customize Your Experience
- 🎯 Adjust simulation parameters in the web interface
- 📊 Create your own scenarios with custom meals and insulin
- 🎤 Add foods to the voice recognition database

### Advanced Usage
- 🧪 Train a custom digital twin with your own data
- 🔬 Run virtual clinical trials with multiple digital twins
- 🌐 Deploy the web app to a cloud platform

---

## 🆘 Common Issues

### Import Error: "No module named 't1dsim_ai'"

**Solution**: Make sure you installed the package in editable mode:
```bash
pip install -e .
```

### Import Error: "No module named 'torch'" or "'librosa'"

**Solution**: Ensure you installed the latest dependencies:
```bash
pip install -e .
```
(We've added these to the core `pyproject.toml` dependencies).

### FileNotFoundError: "data_example/data_example.csv"

**Solution**: Ensure you are in the `example/` directory when running `runDigitalTwin.py`.

### Port 5000 Already in Use

**Solution**: Use a different port:
```bash
python app.py --port 8080
```

Or kill the process using port 5000:
```bash
# On macOS/Linux
lsof -ti:5000 | xargs kill -9

# On Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Voice Module Not Working

**Solution**: Install audio dependencies:

**macOS**:
```bash
brew install portaudio
pip install pyaudio
```

**Linux**:
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

**Windows**:
```bash
pip install pipwin
pipwin install pyaudio
```

---

## 📝 Cheat Sheet

### Load a Digital Twin
```python
from t1dsim_ai.individual_model import DigitalTwin
twin = DigitalTwin(n_digitalTwin=1)  # ID: 0-4
```

### Run a Simulation
```python
results = twin.simulate(data)
# Results include: cgm_NNDT, cgm_NNPop, cgm_Actual
```

### Calculate Statistics
```python
# Time in range (70-180 mg/dL)
tir = ((results.cgm_NNDT >= 70) & (results.cgm_NNDT <= 180)).mean() * 100

# Mean glucose
mean_glucose = results.cgm_NNDT.mean()

# Coefficient of variation
cv = (results.cgm_NNDT.std() / results.cgm_NNDT.mean()) * 100
```

### Web App Routes
- `/` - Main dashboard
- `/simulate` - Run simulation (POST)
- `/voice_log_food` - Voice food logging (POST)
- `/manual_log_food` - Manual food entry (POST)
- `/get_food_log` - Get food log (GET)

---

## 🎉 You're Ready!

You now know the basics of Greens Digital Simulator. 

**Explore more**:
- 🔬 Experiment with different scenarios
- 📊 Analyze glucose patterns
- 🎤 Try voice food logging
- 🌐 Customize the web interface

**Need help?** Check the [README.md](README.md) or open an [issue](https://github.com/Xplosion-Team/greensdigitalsimulator/issues).

---

<div align="center">

**Happy simulating! 🩺💙**

</div>
