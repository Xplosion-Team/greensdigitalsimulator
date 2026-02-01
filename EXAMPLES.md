# 💡 Examples and Tutorials

Step-by-step examples for using Greens Digital Simulator.

---

## 📚 Table of Contents

1. [Basic Simulation](#basic-simulation)
2. [Voice Food Logging](#voice-food-logging)
3. [Custom Scenarios](#custom-scenarios)
4. [Comparing Digital Twins](#comparing-digital-twins)
5. [Training a Custom Digital Twin](#training-a-custom-digital-twin)
6. [Web Interface Usage](#web-interface-usage)
7. [Advanced Analysis](#advanced-analysis)
8. [Research Applications](#research-applications)

---

## 1️⃣ Basic Simulation

### Example 1A: Run Your First Simulation

**Goal**: Simulate 24 hours of glucose dynamics using a pre-trained digital twin.

```python
import pandas as pd
from t1dsim_ai.individual_model import DigitalTwin
import matplotlib.pyplot as plt

# Load example data
data = pd.read_csv("example/data_example/data_example.csv")

# Filter to test data only
test_data = data[~data.is_train]

# Select 24 hours (288 data points at 5-min intervals)
simulation_data = test_data.iloc[0:288]

# Initialize digital twin #1
twin = DigitalTwin(n_digitalTwin=1)

# Run simulation
results = twin.simulate(simulation_data)

# Print summary statistics
print(f"Mean glucose (actual): {results.cgm_Actual.mean():.1f} mg/dL")
print(f"Mean glucose (predicted): {results.cgm_NNDT.mean():.1f} mg/dL")
print(f"RMSE: {((results.cgm_NNDT - results.cgm_Actual)**2).mean()**0.5:.1f} mg/dL")

# Calculate time in range (70-180 mg/dL)
tir_actual = ((results.cgm_Actual >= 70) & (results.cgm_Actual <= 180)).mean() * 100
tir_predicted = ((results.cgm_NNDT >= 70) & (results.cgm_NNDT <= 180)).mean() * 100

print(f"Time in range (actual): {tir_actual:.1f}%")
print(f"Time in range (predicted): {tir_predicted:.1f}%")
```

**Expected Output**:
```
Mean glucose (actual): 145.3 mg/dL
Mean glucose (predicted): 142.8 mg/dL
RMSE: 18.2 mg/dL
Time in range (actual): 72.5%
Time in range (predicted): 75.3%
```

---

### Example 1B: Visualize Results

**Goal**: Create a publication-quality plot of simulation results.

```python
import matplotlib.pyplot as plt
import numpy as np

# Create figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7), sharex=True)

# Time vector (in hours)
time_hours = np.arange(len(results)) / 12  # 12 data points per hour

# Plot 1: Glucose levels
ax1.plot(time_hours, results.cgm_Actual, 'k-', linewidth=2, label='Actual CGM')
ax1.plot(time_hours, results.cgm_NNDT, 'b--', linewidth=2, label='Digital Twin Prediction')
ax1.axhspan(70, 180, alpha=0.2, color='green', label='Target Range')
ax1.axhline(70, color='red', linestyle=':', alpha=0.5)
ax1.axhline(180, color='red', linestyle=':', alpha=0.5)

ax1.set_ylabel('Glucose (mg/dL)', fontsize=12)
ax1.set_ylim(40, 300)
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_title('Digital Twin Glucose Prediction', fontsize=14, fontweight='bold')

# Plot 2: Inputs (insulin and meals)
ax2_insulin = ax2
ax2_insulin.plot(time_hours, results.input_insulin, 'b-', linewidth=2, label='Insulin (U/h)')
ax2_insulin.set_ylabel('Insulin (U/h)', color='b', fontsize=12)
ax2_insulin.tick_params(axis='y', labelcolor='b')

# Overlay meals on secondary y-axis
ax2_meals = ax2.twinx()
meal_times = results[results.input_meal_carbs > 0]
meal_hours = meal_times.index / 12
ax2_meals.stem(meal_hours, meal_times.input_meal_carbs, 'r', markerfmt='ro', 
               label='Meals (g carbs)', basefmt=' ')
ax2_meals.set_ylabel('Carbohydrates (g)', color='r', fontsize=12)
ax2_meals.tick_params(axis='y', labelcolor='r')

ax2_insulin.set_xlabel('Time (hours)', fontsize=12)
ax2_insulin.set_xlim(0, 24)
ax2_insulin.grid(True, alpha=0.3)

# Combine legends
lines1, labels1 = ax2_insulin.get_legend_handles_labels()
lines2, labels2 = ax2_meals.get_legend_handles_labels()
ax2_insulin.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)

plt.tight_layout()
plt.savefig('simulation_results.png', dpi=300, bbox_inches='tight')
plt.show()

print("Plot saved as 'simulation_results.png'")
```

---

## 2️⃣ Voice Food Logging

### Example 2A: Basic Voice Logging

**Goal**: Log food using voice commands and calculate nutrition.

```python
from example.voice_module import VoiceFoodLogger

# Initialize voice logger
logger = VoiceFoodLogger()

print("Voice Food Logger Ready!")
print("Say something like: 'I ate two apples and one banana'")
print("Listening...")

# Listen for food input
foods = logger.listen_and_log()

# Display results
if foods:
    print("\n=== Foods Logged ===")
    total_carbs = 0
    
    for food in foods:
        print(f"  • {food['quantity']:.1f} {food['unit']} of {food['name']}")
        print(f"    - Carbs: {food['carbs']:.1f}g")
        print(f"    - Protein: {food.get('protein', 0):.1f}g")
        print(f"    - Calories: {food.get('calories', 0):.0f} kcal")
        total_carbs += food['carbs']
    
    print(f"\n=== Total ===")
    print(f"Total Carbohydrates: {total_carbs:.1f}g")
else:
    print("No foods detected. Please try again.")
```

**Example Interaction**:
```
Voice Food Logger Ready!
Say something like: 'I ate two apples and one banana'
Listening...

[You speak: "I ate two apples and a slice of bread"]

=== Foods Logged ===
  • 2.0 serving of apple
    - Carbs: 50.0g
    - Protein: 1.0g
    - Calories: 190 kcal
  • 1.0 slice of bread
    - Carbs: 15.0g
    - Protein: 3.0g
    - Calories: 80 kcal

=== Total ===
Total Carbohydrates: 65.0g
```

---

### Example 2B: Manual Food Entry (Fallback)

**Goal**: Log food manually when voice is unavailable.

```python
from example.voice_module import VoiceFoodLogger

logger = VoiceFoodLogger()

# Manual food entry
food_entries = [
    {"food": "apple", "quantity": 2, "unit": "serving"},
    {"food": "rice", "quantity": 1.5, "unit": "cup"},
    {"food": "chicken", "quantity": 6, "unit": "oz"}
]

print("=== Manual Food Log ===\n")
total_carbs = 0
total_protein = 0

for entry in food_entries:
    nutrition = logger.get_food_nutrition(
        entry["food"], 
        entry["quantity"], 
        entry["unit"]
    )
    
    print(f"{entry['quantity']} {entry['unit']} of {entry['food']}")
    print(f"  Carbs: {nutrition['carbs']:.1f}g | Protein: {nutrition['protein']:.1f}g")
    print(f"  Fat: {nutrition['fat']:.1f}g | Fiber: {nutrition['fiber']:.1f}g")
    print(f"  Calories: {nutrition['calories']:.0f} kcal\n")
    
    total_carbs += nutrition['carbs']
    total_protein += nutrition['protein']

print(f"=== Totals ===")
print(f"Carbs: {total_carbs:.1f}g | Protein: {total_protein:.1f}g")
```

---

## 3️⃣ Custom Scenarios

### Example 3A: Create a Meal Response Scenario

**Goal**: Simulate glucose response to a specific meal.

```python
import pandas as pd
import numpy as np
from t1dsim_ai.individual_model import DigitalTwin

# Scenario parameters
duration = 288  # 24 hours
dt = 5  # 5-minute intervals

# Initialize DataFrame
scenario = pd.DataFrame({
    'time': range(duration),
    'output_cgm': 110,  # Start at 110 mg/dL
    'input_insulin': 1.0,  # Basal rate 1.0 U/h
    'input_meal_carbs': 0,
    'heart_rate': 70,
    'sleep_efficiency': 0,
    'is_train': False,
    'feat_hour_of_day_sin': 0,
    'feat_hour_of_day_cos': 1,
    'feat_is_weekend': 0,
    'heart_rate_WRTbaseline': 0
})

# Add breakfast (75g carbs) at hour 1 (time index 12)
breakfast_time = 12  # 1 hour * 12 intervals/hour
scenario.loc[breakfast_time, 'input_meal_carbs'] = 75

# Add lunch (60g carbs) at hour 6 (time index 72)
lunch_time = 72
scenario.loc[lunch_time, 'input_meal_carbs'] = 60

# Add dinner (80g carbs) at hour 12 (time index 144)
dinner_time = 144
scenario.loc[dinner_time, 'input_meal_carbs'] = 80

# Simulate with digital twin
twin = DigitalTwin(n_digitalTwin=1)
results = twin.simulate(scenario)

# Analyze meal responses
meals = [
    ("Breakfast", breakfast_time, 75),
    ("Lunch", lunch_time, 60),
    ("Dinner", dinner_time, 80)
]

for meal_name, meal_time, carbs in meals:
    # Extract 4-hour window after meal
    start_idx = meal_time
    end_idx = min(meal_time + 48, len(results))  # 48 = 4 hours
    
    window = results.iloc[start_idx:end_idx]
    
    baseline = results.iloc[meal_time].cgm_NNDT
    peak = window.cgm_NNDT.max()
    time_to_peak = (window.cgm_NNDT.idxmax() - meal_time) * 5  # minutes
    
    print(f"\n{meal_name} Response ({carbs}g carbs):")
    print(f"  Baseline glucose: {baseline:.1f} mg/dL")
    print(f"  Peak glucose: {peak:.1f} mg/dL")
    print(f"  Glucose rise: {peak - baseline:.1f} mg/dL")
    print(f"  Time to peak: {time_to_peak:.0f} minutes")
```

**Expected Output**:
```
Breakfast Response (75g carbs):
  Baseline glucose: 110.0 mg/dL
  Peak glucose: 187.3 mg/dL
  Glucose rise: 77.3 mg/dL
  Time to peak: 90 minutes

Lunch Response (60g carbs):
  Baseline glucose: 125.4 mg/dL
  Peak glucose: 192.1 mg/dL
  Glucose rise: 66.7 mg/dL
  Time to peak: 75 minutes

Dinner Response (80g carbs):
  Baseline glucose: 118.2 mg/dL
  Peak glucose: 201.5 mg/dL
  Glucose rise: 83.3 mg/dL
  Time to peak: 95 minutes
```

---

### Example 3B: Test Different Insulin Doses

**Goal**: Find optimal insulin dose for a 75g carb meal.

```python
import pandas as pd
import numpy as np
from t1dsim_ai.individual_model import DigitalTwin
import matplotlib.pyplot as plt

# Test insulin doses from 4 to 10 units
insulin_doses = [4, 5, 6, 7, 8, 9, 10]
twin = DigitalTwin(n_digitalTwin=1)

results_by_dose = {}

for dose in insulin_doses:
    # Create scenario
    scenario = pd.DataFrame({
        'time': range(144),  # 12 hours
        'output_cgm': 120,
        'input_insulin': 1.0,  # Basal
        'input_meal_carbs': 0,
        'heart_rate': 70,
        'sleep_efficiency': 0,
        'is_train': False,
        'feat_hour_of_day_sin': 0,
        'feat_hour_of_day_cos': 1,
        'feat_is_weekend': 0,
        'heart_rate_WRTbaseline': 0
    })
    
    # Add meal at time 0
    scenario.loc[0, 'input_meal_carbs'] = 75
    
    # Add bolus insulin
    # Spread dose over 30 minutes (6 intervals)
    for i in range(6):
        scenario.loc[i, 'input_insulin'] = 1.0 + (dose / 0.5)  # U/h
    
    # Simulate
    result = twin.simulate(scenario)
    results_by_dose[dose] = result
    
    # Calculate metrics
    peak = result.cgm_NNDT.max()
    nadir = result.cgm_NNDT.min()
    tir = ((result.cgm_NNDT >= 70) & (result.cgm_NNDT <= 180)).mean() * 100
    
    print(f"Dose: {dose}U | Peak: {peak:.1f} | Nadir: {nadir:.1f} | TIR: {tir:.1f}%")

# Plot comparison
plt.figure(figsize=(12, 6))
for dose, result in results_by_dose.items():
    time_hours = np.arange(len(result)) / 12
    plt.plot(time_hours, result.cgm_NNDT, label=f'{dose}U bolus')

plt.axhspan(70, 180, alpha=0.2, color='green', label='Target Range')
plt.xlabel('Time (hours)')
plt.ylabel('Glucose (mg/dL)')
plt.title('Glucose Response to Different Insulin Doses (75g meal)')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('insulin_dose_comparison.png', dpi=300)
plt.show()
```

---

## 4️⃣ Comparing Digital Twins

### Example 4A: Population Variability Analysis

**Goal**: Compare glucose responses across different digital twins.

```python
from t1dsim_ai.individual_model import DigitalTwin
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load test data
data = pd.read_csv("example/data_example/data_example.csv")
test_data = data[~data.is_train].iloc[0:288]  # 24 hours

# Simulate with all 5 digital twins
twins_results = {}

for twin_id in range(5):
    print(f"Simulating Digital Twin #{twin_id}...")
    twin = DigitalTwin(n_digitalTwin=twin_id)
    result = twin.simulate(test_data)
    twins_results[twin_id] = result
    
    # Calculate metrics
    mean_glucose = result.cgm_NNDT.mean()
    std_glucose = result.cgm_NNDT.std()
    cv = (std_glucose / mean_glucose) * 100
    tir = ((result.cgm_NNDT >= 70) & (result.cgm_NNDT <= 180)).mean() * 100
    
    print(f"  Mean: {mean_glucose:.1f} mg/dL | CV: {cv:.1f}% | TIR: {tir:.1f}%\n")

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Glucose trajectories
time_hours = np.arange(288) / 12
for twin_id, result in twins_results.items():
    ax1.plot(time_hours, result.cgm_NNDT, label=f'Twin #{twin_id}', alpha=0.7)

ax1.axhspan(70, 180, alpha=0.2, color='green')
ax1.set_xlabel('Time (hours)', fontsize=12)
ax1.set_ylabel('Glucose (mg/dL)', fontsize=12)
ax1.set_title('Inter-individual Variability', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Statistics comparison
twin_ids = list(twins_results.keys())
means = [twins_results[tid].cgm_NNDT.mean() for tid in twin_ids]
stds = [twins_results[tid].cgm_NNDT.std() for tid in twin_ids]

x = np.arange(len(twin_ids))
width = 0.35

ax2.bar(x - width/2, means, width, label='Mean Glucose', alpha=0.8)
ax2.bar(x + width/2, stds, width, label='Std Dev', alpha=0.8)

ax2.set_xlabel('Digital Twin ID', fontsize=12)
ax2.set_ylabel('Glucose (mg/dL)', fontsize=12)
ax2.set_title('Statistical Comparison', fontsize=14, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels([f'Twin {i}' for i in twin_ids])
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('twin_comparison.png', dpi=300)
plt.show()
```

---

## 5️⃣ Training a Custom Digital Twin

### Example 5A: Prepare Your Data

**Goal**: Format your CGM data for training a digital twin.

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Example: Convert your raw CGM data
raw_data = pd.read_csv("my_cgm_data.csv")

# Required columns transformation
formatted_data = pd.DataFrame()

# 1. Time (5-minute intervals)
formatted_data['time'] = pd.date_range(
    start='2024-01-01', 
    periods=len(raw_data), 
    freq='5min'
)
formatted_data['datetime_local'] = formatted_data['time']

# 2. CGM readings
formatted_data['output_cgm'] = raw_data['glucose_mg_dl']

# 3. Insulin (if you have pump data)
formatted_data['input_insulin'] = raw_data['insulin_rate_u_hr']

# 4. Meals (carbohydrate intake)
formatted_data['input_meal_carbs'] = raw_data['carbs_grams'].fillna(0)

# 5. Heart rate (if available, otherwise use average)
if 'heart_rate' in raw_data.columns:
    formatted_data['heart_rate'] = raw_data['heart_rate']
else:
    formatted_data['heart_rate'] = 70  # Default

# 6. Sleep efficiency (0-1 scale)
# You can derive this from activity or sleep tracker data
formatted_data['sleep_efficiency'] = 0  # Simplified

# 7. Feature engineering
hour_of_day = formatted_data['time'].dt.hour + formatted_data['time'].dt.minute / 60
formatted_data['feat_hour_of_day_sin'] = np.sin(2 * np.pi * hour_of_day / 24)
formatted_data['feat_hour_of_day_cos'] = np.cos(2 * np.pi * hour_of_day / 24)
formatted_data['feat_is_weekend'] = formatted_data['time'].dt.dayofweek.isin([5, 6]).astype(int)

# 8. Heart rate baseline
hr_baseline = formatted_data['heart_rate'].median()
formatted_data['heart_rate_WRTbaseline'] = (formatted_data['heart_rate'] - hr_baseline) / hr_baseline

# 9. Train/test split (80/20)
split_idx = int(len(formatted_data) * 0.8)
formatted_data['is_train'] = True
formatted_data.loc[split_idx:, 'is_train'] = False

# Save formatted data
formatted_data.to_csv('formatted_training_data.csv', index=False)

print(f"Formatted {len(formatted_data)} data points")
print(f"Training samples: {formatted_data['is_train'].sum()}")
print(f"Test samples: {(~formatted_data['is_train']).sum()}")
print("\nData ready for training!")
```

---

### Example 5B: Train the Model (Conceptual)

**Note**: Full training requires the complete training pipeline from the original T1DSim_AI framework.

```python
# This is a conceptual example - actual training requires
# the full training infrastructure

from t1dsim_ai.individual_model import train_digital_twin

# Load your prepared data
training_data = pd.read_csv('formatted_training_data.csv')

# Training configuration
config = {
    'n_epochs': 100,
    'learning_rate': 0.001,
    'batch_size': 32,
    'n_neurons': {
        'S1': 32, 'S2': 32, 'I': 32,
        'Q1': 64, 'Q2': 32, 'CGM': 32
    },
    'overlap': 0.5,  # Data window overlap
    'window_size': 288  # 24-hour windows
}

# Train model
model, scaler, history = train_digital_twin(
    data=training_data,
    config=config,
    save_path='my_digital_twin/'
)

# Evaluate on test set
test_data = training_data[~training_data.is_train]
test_results = model.simulate(test_data)

# Calculate performance
rmse = np.sqrt(((test_results.cgm_NNDT - test_results.cgm_Actual)**2).mean())
print(f"Test RMSE: {rmse:.2f} mg/dL")
```

---

## 6️⃣ Web Interface Usage

### Example 6A: Launch and Navigate

**Step 1**: Start the web application

```bash
cd example
python app.py
```

**Step 2**: Open browser to `http://localhost:5000`

**Step 3**: Interface tour:

1. **Top Panel**: Digital twin selector (0-4)
2. **Left Sidebar**: Scenario parameters
   - Initial glucose
   - Basal insulin rate
   - Meal size and timing
   - Heart rate
3. **Center**: Interactive glucose chart
4. **Right Sidebar**: Voice/manual food logging
5. **Bottom**: Statistics dashboard

---

### Example 6B: Create Interactive Scenario

**Steps**:

1. Select **Digital Twin #2** from dropdown
2. Set parameters:
   - Initial Glucose: **120 mg/dL**
   - Basal Insulin: **1.2 U/h**
   - Meal Size: **60 grams**
   - Meal Time: **1 hour**
   - Heart Rate: **75 BPM**
3. Click **"Run Simulation"**
4. Observe:
   - Glucose trajectory prediction
   - Time-in-range percentage
   - Peak glucose and timing
5. Adjust parameters and re-run to compare

---

## 7️⃣ Advanced Analysis

### Example 7A: Glycemic Variability Assessment

**Goal**: Analyze glucose variability metrics.

```python
import pandas as pd
import numpy as np
from t1dsim_ai.individual_model import DigitalTwin

# Load data and simulate
data = pd.read_csv("example/data_example/data_example.csv")
test_data = data[~data.is_train].iloc[0:864]  # 3 days

twin = DigitalTwin(n_digitalTwin=1)
results = twin.simulate(test_data)

# Glycemic Variability Metrics
glucose = results.cgm_NNDT

# 1. Standard Deviation (SD)
sd = glucose.std()

# 2. Coefficient of Variation (CV)
cv = (sd / glucose.mean()) * 100

# 3. Mean Amplitude of Glycemic Excursions (MAGE)
# Simplified calculation
peaks = glucose[(glucose.shift(1) < glucose) & (glucose.shift(-1) < glucose)]
troughs = glucose[(glucose.shift(1) > glucose) & (glucose.shift(-1) > glucose)]
excursions = []
for i in range(min(len(peaks), len(troughs))):
    excursion = abs(peaks.iloc[i] - troughs.iloc[i])
    if excursion > sd:  # Only count significant excursions
        excursions.append(excursion)
mage = np.mean(excursions) if excursions else 0

# 4. J-Index
j_index = 0.001 * (glucose.mean() + sd) ** 2

# 5. Low Blood Glucose Index (LBGI)
def calculate_lbgi(glucose_values):
    risk_values = []
    for g in glucose_values:
        if g < 112.5:
            f = 1.509 * (np.log(g)**1.084 - 5.381)
            rl = 10 * f**2
            risk_values.append(rl)
    return np.mean(risk_values) if risk_values else 0

lbgi = calculate_lbgi(glucose)

# 6. High Blood Glucose Index (HBGI)
def calculate_hbgi(glucose_values):
    risk_values = []
    for g in glucose_values:
        if g > 112.5:
            f = 1.509 * (np.log(g)**1.084 - 5.381)
            rh = 10 * f**2
            risk_values.append(rh)
    return np.mean(risk_values) if risk_values else 0

hbgi = calculate_hbgi(glucose)

# 7. Time in Ranges
tir = ((glucose >= 70) & (glucose <= 180)).mean() * 100
time_below = (glucose < 70).mean() * 100
time_above = (glucose > 180).mean() * 100
time_very_high = (glucose > 250).mean() * 100

# Print report
print("=" * 50)
print("GLYCEMIC VARIABILITY ANALYSIS")
print("=" * 50)
print(f"\nBasic Statistics:")
print(f"  Mean Glucose: {glucose.mean():.1f} mg/dL")
print(f"  Median Glucose: {glucose.median():.1f} mg/dL")
print(f"  Min Glucose: {glucose.min():.1f} mg/dL")
print(f"  Max Glucose: {glucose.max():.1f} mg/dL")

print(f"\nVariability Metrics:")
print(f"  Standard Deviation: {sd:.1f} mg/dL")
print(f"  Coefficient of Variation: {cv:.1f}%")
print(f"  MAGE: {mage:.1f} mg/dL")
print(f"  J-Index: {j_index:.2f}")

print(f"\nRisk Indices:")
print(f"  LBGI (Low Risk): {lbgi:.2f}")
print(f"  HBGI (High Risk): {hbgi:.2f}")

print(f"\nTime in Ranges:")
print(f"  Time in Range (70-180): {tir:.1f}%")
print(f"  Time Below Range (<70): {time_below:.1f}%")
print(f"  Time Above Range (>180): {time_above:.1f}%")
print(f"  Time Very High (>250): {time_very_high:.1f}%")

print("\n" + "=" * 50)
```

---

## 8️⃣ Research Applications

### Example 8A: Virtual Clinical Trial

**Goal**: Test a treatment intervention across a population.

```python
from t1dsim_ai.individual_model import DigitalTwin
import pandas as pd
import numpy as np

# Load baseline data
data = pd.read_csv("example/data_example/data_example.csv")
test_data = data[~data.is_train].iloc[0:288]

# Define two interventions
interventions = {
    'Standard': {'basal_multiplier': 1.0},
    'Intensive': {'basal_multiplier': 1.2}  # 20% increase
}

# Run virtual trial across all digital twins
results_table = []

for twin_id in range(5):
    twin = DigitalTwin(n_digitalTwin=twin_id)
    
    for intervention_name, params in interventions.items():
        # Modify scenario
        scenario = test_data.copy()
        scenario['input_insulin'] *= params['basal_multiplier']
        
        # Simulate
        result = twin.simulate(scenario)
        
        # Calculate outcomes
        mean_glucose = result.cgm_NNDT.mean()
        tir = ((result.cgm_NNDT >= 70) & (result.cgm_NNDT <= 180)).mean() * 100
        hypo_events = (result.cgm_NNDT < 70).sum()
        
        results_table.append({
            'Twin_ID': twin_id,
            'Intervention': intervention_name,
            'Mean_Glucose': mean_glucose,
            'TIR': tir,
            'Hypo_Events': hypo_events
        })

# Convert to DataFrame
results_df = pd.DataFrame(results_table)

# Statistical analysis
print("VIRTUAL CLINICAL TRIAL RESULTS")
print("=" * 60)

for intervention in ['Standard', 'Intensive']:
    subset = results_df[results_df.Intervention == intervention]
    print(f"\n{intervention} Therapy:")
    print(f"  Mean Glucose: {subset.Mean_Glucose.mean():.1f} ± {subset.Mean_Glucose.std():.1f} mg/dL")
    print(f"  Time in Range: {subset.TIR.mean():.1f} ± {subset.TIR.std():.1f}%")
    print(f"  Avg Hypo Events: {subset.Hypo_Events.mean():.1f}")

# Statistical test (simplified)
from scipy import stats

standard_tir = results_df[results_df.Intervention == 'Standard']['TIR']
intensive_tir = results_df[results_df.Intervention == 'Intensive']['TIR']

t_stat, p_value = stats.ttest_ind(standard_tir, intensive_tir)

print(f"\n\nStatistical Comparison:")
print(f"  t-statistic: {t_stat:.3f}")
print(f"  p-value: {p_value:.4f}")
print(f"  Significant: {'Yes' if p_value < 0.05 else 'No'} (α=0.05)")
```

---

<div align="center">

**Complete examples and tutorials for Greens Digital Simulator** 💡

[Back to README](README.md) • [API Reference](API.md) • [Quick Start](QUICKSTART.md)

</div>
