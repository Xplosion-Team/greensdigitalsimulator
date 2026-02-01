# 📡 API Documentation

Complete reference for the Greens Digital Simulator API and Web Interface.

---

## 🐍 Python API

### Core Classes

#### `DigitalTwin`

**Location**: `src/t1dsim_ai/individual_model.py`

**Description**: Represents an individual digital twin for glucose simulation.

**Constructor**:
```python
DigitalTwin(n_digitalTwin, scale_dx=1.0)
```

**Parameters**:
- `n_digitalTwin` (int): Digital twin ID (0-4)
  - 0: T1DEXI-01-0102
  - 1: T1DEXI-01-0692
  - 2: T1DEXI-01-0794
  - 3: T1DEXI-01-0880
  - 4: T1DEXI-01-1047
- `scale_dx` (float, optional): Time scaling factor (default: 1.0)

**Methods**:

##### `simulate(data)`
Simulate glucose dynamics for the provided data.

**Parameters**:
- `data` (pandas.DataFrame): Input data with required columns

**Required columns**:
- `output_cgm`: CGM readings (mg/dL)
- `input_insulin`: Insulin delivery (U/h)
- `input_meal_carbs`: Carbohydrate intake (g)
- `heart_rate`: Heart rate (BPM)
- `sleep_efficiency`: Sleep quality (0-1)
- `is_train`: Training flag (boolean)
- `feat_hour_of_day_sin`: Hour of day (sine)
- `feat_hour_of_day_cos`: Hour of day (cosine)
- `feat_is_weekend`: Weekend flag (0/1)
- `heart_rate_WRTbaseline`: Heart rate relative to baseline

**Returns**:
- `pandas.DataFrame`: Simulation results with columns:
  - `cgm_Actual`: Original CGM readings
  - `cgm_NNPop`: Population model predictions
  - `cgm_NNDT`: Digital twin predictions
  - All original input columns

**Example**:
```python
from t1dsim_ai.individual_model import DigitalTwin
import pandas as pd

# Initialize digital twin
twin = DigitalTwin(n_digitalTwin=1)

# Load data
data = pd.read_csv("data_example.csv")
data = data[~data.is_train]  # Use test set

# Simulate
results = twin.simulate(data.head(288))  # 24 hours

# Access predictions
print(f"Mean predicted glucose: {results.cgm_NNDT.mean():.1f} mg/dL")
```

---

#### `CGMOHSUSimStateSpaceModel_V2`

**Location**: `src/t1dsim_ai/population_model.py`

**Description**: Population-level neural state-space model.

**Constructor**:
```python
CGMOHSUSimStateSpaceModel_V2(n_feat, lookback_inputs=[None, None], scale_dx=1.0, init_small=True)
```

**Parameters**:
- `n_feat` (dict): Number of neurons per state variable
  - Keys: 'S1', 'S2', 'I', 'Q1', 'Q2', 'CGM'
  - Values: Integer neuron counts
- `lookback_inputs` (list): Historical input window sizes
- `scale_dx` (float): Time scaling factor
- `init_small` (bool): Use small weight initialization

**Example**:
```python
from t1dsim_ai.population_model import CGMOHSUSimStateSpaceModel_V2

# Define network architecture
n_feat = {
    'S1': 32, 'S2': 32, 'I': 32,
    'Q1': 64, 'Q2': 32, 'CGM': 32
}

# Create model
model = CGMOHSUSimStateSpaceModel_V2(
    n_feat=n_feat,
    scale_dx=1.0,
    init_small=True
)
```

---

#### `VoiceFoodLogger`

**Location**: `example/voice_module.py`

**Description**: Voice-enabled food logging system.

**Constructor**:
```python
VoiceFoodLogger()
```

**Methods**:

##### `listen_and_log()`
Listen for voice input and log foods.

**Returns**:
- `list`: List of logged food dictionaries

**Example**:
```python
from example.voice_module import VoiceFoodLogger

logger = VoiceFoodLogger()
foods = logger.listen_and_log()
# Speak: "I ate two apples"

for food in foods:
    print(f"{food['quantity']} {food['name']}: {food['carbs']}g carbs")
```

##### `get_total_carbs()`
Get total carbohydrates from recent logs.

**Returns**:
- `float`: Total carbs in grams

##### `parse_food_from_text(text)`
Parse food items from text.

**Parameters**:
- `text` (str): Natural language food description

**Returns**:
- `list`: Parsed food items

**Example**:
```python
foods = logger.parse_food_from_text("two apples and one banana")
# Returns: [{'name': 'apple', 'quantity': 2, 'carbs': 50}, ...]
```

##### `get_food_nutrition(food_name, quantity=1, unit='serving')`
Get nutrition information for a food.

**Parameters**:
- `food_name` (str): Name of the food
- `quantity` (float): Amount
- `unit` (str): Unit of measurement

**Returns**:
- `dict`: Nutrition data with keys:
  - `carbs`: Carbohydrates (g)
  - `protein`: Protein (g)
  - `fat`: Fat (g)
  - `fiber`: Fiber (g)
  - `calories`: Calories (kcal)

---

### Utility Functions

#### Scenario Creation

**Location**: `src/t1dsim_ai/create_scenarios.py`

##### `create_custom_scenario(initial_glucose, basal_insulin, meal_carbs, meal_time, heart_rate, duration=288)`

Create a custom simulation scenario.

**Parameters**:
- `initial_glucose` (float): Starting glucose (mg/dL)
- `basal_insulin` (float): Basal insulin rate (U/h)
- `meal_carbs` (float): Meal carbohydrate amount (g)
- `meal_time` (int): Time of meal in 5-min intervals
- `heart_rate` (float): Baseline heart rate (BPM)
- `duration` (int): Simulation duration in 5-min intervals (default: 288 = 24h)

**Returns**:
- `pandas.DataFrame`: Scenario data ready for simulation

**Example**:
```python
from t1dsim_ai.create_scenarios import create_custom_scenario

scenario = create_custom_scenario(
    initial_glucose=110,
    basal_insulin=1.0,
    meal_carbs=75,
    meal_time=60,  # 5 hours (60 * 5 min = 5 hours)
    heart_rate=70,
    duration=288   # 24 hours
)
```

---

## 🌐 Web API (Flask)

### Endpoints

#### `GET /`

**Description**: Main dashboard page

**Response**: HTML page with interactive interface

---

#### `POST /simulate`

**Description**: Run a digital twin simulation

**Request Body** (JSON):
```json
{
  "digital_twin_id": 1,
  "scenario": {
    "init_cgm": 110,
    "basal_insulin": 1.0,
    "meal_size": 75,
    "meal_time": 60,
    "heart_rate": 70
  }
}
```

**Response** (JSON):
```json
{
  "time": [0, 1, 2, ...],
  "glucose": [110, 112, 115, ...],
  "insulin": [1.0, 1.0, 1.0, ...],
  "meals": [0, 0, 75, ...],
  "statistics": {
    "mean_glucose": 145.2,
    "time_in_range": 78.5,
    "cv": 32.1
  }
}
```

---

#### `POST /voice_log_food`

**Description**: Log food using voice recognition

**Request Body**: None (uses microphone)

**Response** (JSON):
```json
{
  "success": true,
  "foods": [
    {
      "name": "apple",
      "quantity": 2,
      "unit": "serving",
      "carbs": 50,
      "protein": 1,
      "fat": 0.5
    }
  ],
  "total_carbs": 50,
  "message": "Logged 2 apple(s)"
}
```

---

#### `POST /manual_log_food`

**Description**: Manually log a food item

**Request Body** (JSON):
```json
{
  "food_name": "apple",
  "quantity": 2,
  "unit": "serving"
}
```

**Response** (JSON):
```json
{
  "success": true,
  "food": {
    "name": "apple",
    "quantity": 2,
    "carbs": 50
  },
  "total_carbs": 50
}
```

---

#### `GET /get_food_log`

**Description**: Retrieve food log entries

**Query Parameters**:
- `hours` (optional): Hours to look back (default: 24)

**Response** (JSON):
```json
{
  "entries": [
    {
      "timestamp": "2025-02-01T10:30:00",
      "food": "apple",
      "quantity": 2,
      "carbs": 50
    }
  ],
  "total_carbs_24h": 125.5
}
```

---

#### `POST /clear_food_log`

**Description**: Clear all food log entries

**Response** (JSON):
```json
{
  "success": true,
  "message": "Food log cleared"
}
```

---

#### `GET /animate_scenario`

**Description**: Get animated scenario data

**Query Parameters**:
- `digital_twin_id` (required): Digital twin ID (0-4)
- `scenario_type` (optional): Scenario preset name

**Response** (JSON):
```json
{
  "frames": [
    {
      "time": 0,
      "glucose": 110,
      "insulin": 1.0,
      "meal": 0
    },
    ...
  ],
  "duration": 288
}
```

---

## 📊 Data Structures

### Simulation Results DataFrame

**Columns**:
| Column | Type | Description |
|--------|------|-------------|
| `time` | int | Time index (5-min intervals) |
| `datetime_local` | datetime | Local timestamp |
| `cgm_Actual` | float | Actual CGM reading (mg/dL) |
| `cgm_NNPop` | float | Population model prediction (mg/dL) |
| `cgm_NNDT` | float | Digital twin prediction (mg/dL) |
| `input_insulin` | float | Insulin delivery (U/h) |
| `input_meal_carbs` | float | Carbohydrate intake (g) |
| `heart_rate` | float | Heart rate (BPM) |
| `sleep_efficiency` | float | Sleep quality (0-1) |

### Food Database Schema

**Structure**:
```python
{
  "food_name": {
    "carbs_per_serving": float,    # grams
    "protein_per_serving": float,  # grams
    "fat_per_serving": float,      # grams
    "fiber_per_serving": float,    # grams
    "calories_per_serving": float, # kcal
    "glycemic_index": str,         # "low", "medium", "high"
    "serving_size": str            # e.g., "1 medium apple"
  }
}
```

**Example**:
```python
{
  "apple": {
    "carbs_per_serving": 25,
    "protein_per_serving": 0.5,
    "fat_per_serving": 0.3,
    "fiber_per_serving": 4.4,
    "calories_per_serving": 95,
    "glycemic_index": "low",
    "serving_size": "1 medium apple (182g)"
  }
}
```

---

## 🔐 Configuration Options

### Environment Variables

Set these in your environment or `.env` file:

```bash
# Flask Configuration
FLASK_ENV=development          # 'development' or 'production'
FLASK_DEBUG=true              # true or false
PORT=5000                     # Port number
HOST=0.0.0.0                  # Host address

# Feature Flags
VOICE_ENABLED=true            # Enable voice logging
TTS_ENABLED=false             # Enable text-to-speech
FOOD_LOG_ENABLED=true         # Enable food logging
NUTRITION_ANALYSIS=true       # Enable nutrition analysis

# Model Configuration
DEFAULT_DIGITAL_TWIN=1        # Default digital twin ID (0-4)
SIMULATION_DURATION=288       # Default duration (5-min intervals)
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_code.py

# Run with coverage
python -m pytest --cov=src/t1dsim_ai tests/
```

### Example Test

```python
import pytest
from t1dsim_ai.individual_model import DigitalTwin
import pandas as pd

def test_digital_twin_simulation():
    # Load test data
    data = pd.read_csv("example/data_example/data_example.csv")
    data = data[~data.is_train].head(288)
    
    # Initialize twin
    twin = DigitalTwin(n_digitalTwin=1)
    
    # Run simulation
    results = twin.simulate(data)
    
    # Assertions
    assert len(results) == len(data)
    assert 'cgm_NNDT' in results.columns
    assert results.cgm_NNDT.notna().all()
    assert results.cgm_NNDT.min() >= 0
    assert results.cgm_NNDT.max() <= 500
```

---

## 📚 Additional Resources

### Code Examples
- See `example/` directory for working scripts
- Check `example/T1DSim_AI-main/example/` for advanced examples

### External Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Support
- GitHub Issues: [Report bugs](https://github.com/Xplosion-Team/greensdigitalsimulator/issues)
- Discussions: [Ask questions](https://github.com/Xplosion-Team/greensdigitalsimulator/discussions)

---

<div align="center">

**Complete API reference for Greens Digital Simulator** 🩺

[Back to README](README.md) • [Quick Start](QUICKSTART.md)

</div>
