# 🏗️ Architecture Documentation

Detailed technical architecture of the Greens Digital Simulator.

---

## 📐 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Greens Digital Simulator                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────┐      ┌──────────────────────────────┐  │
│  │  Web Interface │◄────►│   Flask Application Layer    │  │
│  │   (HTML/JS)    │      │      (app.py / routes)       │  │
│  └────────────────┘      └──────────────────────────────┘  │
│         │                            │                      │
│         │                            ▼                      │
│         │                  ┌────────────────────┐          │
│         │                  │  Voice Module      │          │
│         │                  │  (Speech → Food)   │          │
│         │                  └────────────────────┘          │
│         │                            │                      │
│         └────────────────────────────┼──────────────────┐  │
│                                      │                  │  │
│                                      ▼                  ▼  │
│              ┌─────────────────────────────────────────────┤
│              │         Core Simulation Engine              │
│              ├─────────────────────────────────────────────┤
│              │                                             │
│              │  ┌──────────────────┐  ┌─────────────────┐ │
│              │  │ Population Model │  │  Digital Twins  │ │
│              │  │   (NN State-     │  │  (Individual    │ │
│              │  │    Space Model)  │  │   Calibration)  │ │
│              │  └──────────────────┘  └─────────────────┘ │
│              │           │                     │           │
│              │           └──────────┬──────────┘           │
│              │                      ▼                      │
│              │         ┌────────────────────────┐          │
│              │         │  Forward Euler         │          │
│              │         │  Simulator             │          │
│              │         └────────────────────────┘          │
│              │                      │                      │
│              └──────────────────────┼──────────────────────┘
│                                     │                      │
│                                     ▼                      │
│                         ┌────────────────────┐            │
│                         │  Utility Modules   │            │
│                         │  - Preprocessing   │            │
│                         │  - Metrics         │            │
│                         │  - Scenarios       │            │
│                         └────────────────────┘            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🧠 Neural Network Architecture

### State-Space Model

The core of the simulator is a **physiologically-constrained neural state-space model** that represents glucose-insulin dynamics.

#### State Variables

1. **S1**: Subcutaneous insulin compartment
2. **S2**: Plasma insulin compartment  
3. **I**: Insulin action/effect
4. **Q1**: Glucose mass in accessible compartment
5. **Q2**: Glucose mass in non-accessible compartment

#### Neural Network Components

```python
# NN1: Subcutaneous insulin dynamics
NN1(S1, insulin_input) → dS1/dt

# NN2: Plasma insulin dynamics  
NN2(S1, S2) → dS2/dt

# NN3: Insulin action dynamics
NN3(S2, I) → dI/dt

# NN4: Accessible glucose dynamics (main compartment)
NN4(I, meals, sleep, heart_rate) → dQ1/dt

# NN5: Non-accessible glucose dynamics
NN5(Q1, Q2) → dQ2/dt

# NN6: CGM output (observation model)
NN6(Q1) → CGM_output
```

### Network Structure

Each neural network is a **feed-forward network** with:
- **Input layer**: Relevant state variables and inputs
- **Hidden layer**: ReLU activation
- **Output layer**: Linear activation

**Example (NN1)**:
```
Input: [S1, insulin] (2 neurons)
  ↓
Hidden: 32 neurons (ReLU)
  ↓
Output: dS1/dt (1 neuron)
```

### Architecture Diagram

```
                    ┌─────────────┐
                    │   Inputs    │
                    ├─────────────┤
                    │ • Insulin   │
                    │ • Meals     │
                    │ • HR        │
                    │ • Sleep     │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌───────┐         ┌───────┐         ┌───────┐
    │  NN1  │────────►│  NN2  │────────►│  NN3  │
    │  S1   │         │  S2   │         │   I   │
    └───────┘         └───────┘         └───┬───┘
                                            │
                                            ▼
                                        ┌───────┐
                                        │  NN4  │
                                        │  Q1   │
                                        └───┬───┘
                                            │
                                            ▼
                                        ┌───────┐
                                        │  NN5  │
                                        │  Q2   │
                                        └───┬───┘
                                            │
                                            ▼
                                        ┌───────┐
                                        │  NN6  │
                                        │  CGM  │
                                        └───────┘
                                            │
                                            ▼
                                    ┌───────────────┐
                                    │ Glucose (mg/dL)│
                                    └───────────────┘
```

---

## 🔄 Simulation Flow

### Forward Euler Integration

The simulator uses **forward Euler method** for time integration:

```python
# At each time step (5 minutes):
for t in range(simulation_length):
    # 1. Compute state derivatives using NNs
    dS1 = NN1(S1[t], insulin[t])
    dS2 = NN2(S1[t], S2[t])
    dI = NN3(S2[t], I[t])
    dQ1 = NN4(I[t], meals[t], sleep[t], HR[t])
    dQ2 = NN5(Q1[t], Q2[t])
    
    # 2. Update states
    S1[t+1] = S1[t] + dt * dS1
    S2[t+1] = S2[t] + dt * dS2
    I[t+1] = I[t] + dt * dI
    Q1[t+1] = Q1[t] + dt * dQ1
    Q2[t+1] = Q2[t] + dt * dQ2
    
    # 3. Compute CGM output
    CGM[t+1] = NN6(Q1[t+1])
```

### Data Flow

```
Input Data (CSV)
     │
     ▼
┌──────────────┐
│ Preprocessing │
│ - Scaling     │
│ - Validation  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Load Model   │
│ - Weights    │
│ - Scaler     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Simulation  │
│ - State      │
│   Evolution  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Post-process │
│ - Inverse    │
│   Scaling    │
└──────┬───────┘
       │
       ▼
Results DataFrame
```

---

## 📦 Module Structure

### Core Modules

```
src/t1dsim_ai/
├── __init__.py              # Package initialization
├── __about__.py             # Version info
├── options.py               # Configuration parameters
├── population_model.py      # Population-level NN model
├── individual_model.py      # Digital twin (individual) model
├── create_scenarios.py      # Scenario generation utilities
└── utils/
    ├── __init__.py
    ├── preprocess.py        # Data preprocessing & scaling
    └── metrics.py           # Evaluation metrics
```

### Key Classes

#### `CGMOHSUSimStateSpaceModel_V2` (Population Model)

**Responsibilities**:
- Define neural network architecture
- Implement forward propagation
- Compute state derivatives

**Key Methods**:
- `forward(x, u)`: Compute next states
- `init_hidden()`: Initialize hidden states

---

#### `ForwardEulerSimulator` (Individual Model)

**Responsibilities**:
- Load trained model weights
- Run simulations
- Handle data preprocessing

**Key Methods**:
- `simulate(data)`: Run full simulation
- `_predict_step(state, inputs)`: Single time step

---

#### `DigitalTwin` (High-level API)

**Responsibilities**:
- User-friendly interface
- Load pre-trained models
- Handle data formatting

**Key Methods**:
- `simulate(data)`: Run simulation
- `load_model()`: Load trained weights

---

## 🌐 Web Application Architecture

### Flask Application Structure

```
example/
├── app.py                   # Main Flask application
├── app_production.py        # Production-ready version
├── voice_module.py          # Voice recognition module
├── templates/
│   └── index.html           # Web interface
└── static/
    ├── css/                 # Stylesheets
    ├── js/                  # JavaScript
    └── img/                 # Images
```

### Request/Response Flow

```
Browser
   │
   │ HTTP Request
   ▼
Flask Router
   │
   ├─► GET /            → index.html
   ├─► POST /simulate   → run_simulation()
   ├─► POST /voice_log  → voice_logger.listen()
   └─► GET /food_log    → get_food_history()
   │
   ▼
Business Logic
   │
   ├─► DigitalTwin.simulate()
   ├─► VoiceFoodLogger.parse()
   └─► Statistics calculations
   │
   ▼
JSON Response
   │
   ▼
Browser (Update UI)
```

### Voice Module Architecture

```
┌─────────────────────────────────────────────┐
│          Voice Food Logger                   │
├─────────────────────────────────────────────┤
│                                              │
│  ┌────────────┐      ┌──────────────────┐  │
│  │ Microphone │─────►│ Speech Recognition│  │
│  │            │      │ (Google API)      │  │
│  └────────────┘      └─────────┬─────────┘  │
│                                │              │
│                                ▼              │
│                      ┌──────────────────┐    │
│                      │ Text Processing  │    │
│                      │ - Extract foods  │    │
│                      │ - Parse quantity │    │
│                      └─────────┬────────┘    │
│                                │              │
│                                ▼              │
│                      ┌──────────────────┐    │
│                      │  Food Database   │    │
│                      │  Lookup          │    │
│                      └─────────┬────────┘    │
│                                │              │
│                                ▼              │
│                      ┌──────────────────┐    │
│                      │ Nutrition Calc   │    │
│                      │ - Carbs          │    │
│                      │ - Protein, Fat   │    │
│                      └─────────┬────────┘    │
│                                │              │
│                                ▼              │
│                      ┌──────────────────┐    │
│                      │   Food Log       │    │
│                      │   (JSON file)    │    │
│                      └──────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## 💾 Data Processing Pipeline

### Input Data Processing

```python
# 1. Load raw data
raw_data = pd.read_csv("data.csv")

# 2. Feature engineering
data = add_time_features(raw_data)
# - Hour of day (sin/cos encoding)
# - Weekend flag
# - Heart rate relative to baseline

# 3. Scaling
from t1dsim_ai.utils.preprocess import scaler
scaled_data = scaler.transform(data)

# 4. Validation
validate_data_format(scaled_data)
# - Check required columns
# - Check value ranges
# - Handle missing data

# 5. Segmentation (for training)
segments = create_overlapping_segments(
    scaled_data,
    window_size=288,  # 24 hours
    overlap=0.5
)
```

### Output Post-Processing

```python
# 1. Inverse scaling
predictions_scaled = model.forward(inputs)
predictions = scaler_inverse(predictions_scaled)

# 2. Add metadata
results = pd.DataFrame({
    'time': time_vector,
    'cgm_NNDT': predictions,
    'cgm_NNPop': population_predictions,
    'cgm_Actual': actual_cgm
})

# 3. Calculate metrics
metrics = {
    'rmse': calculate_rmse(results),
    'time_in_range': calculate_tir(results),
    'mean_glucose': results.cgm_NNDT.mean()
}
```

---

## 🔧 Configuration System

### Parameter Hierarchy

```
1. Default Parameters (options.py)
   ↓
2. Model-Specific Parameters (saved with model)
   ↓
3. Scenario Parameters (passed at runtime)
   ↓
4. User Input (web interface or API)
```

### Key Parameters

**Model Architecture** (`options.py`):
```python
n_neurons_pop = {
    'S1': 32,
    'S2': 32,
    'I': 32,
    'Q1': 64,
    'Q2': 32,
    'CGM': 32
}

hidden_compartments = ['S1', 'S2', 'I', 'Q1', 'Q2']
states = ['S1', 'S2', 'I', 'Q1', 'Q2', 'CGM']
inputs = ['insulin', 'meals', 'sleep', 'HR']
```

**Simulation Parameters**:
```python
dt = 5 / 60  # Time step: 5 minutes
scale_dx = 1.0  # Time scaling factor
simulation_horizon = 288  # 24 hours in 5-min intervals
```

---

## 🚀 Deployment Architecture

### Local Development

```
┌─────────────────┐
│  Developer      │
│  Machine        │
├─────────────────┤
│                 │
│  Flask (Debug)  │
│  Port: 5000     │
│                 │
│  SQLite/JSON    │
│  (Food logs)    │
└─────────────────┘
```

### Production Deployment (Render)

```
┌─────────────────────────────────────┐
│         Render Platform              │
├─────────────────────────────────────┤
│                                      │
│  ┌──────────────────────────────┐  │
│  │   Gunicorn                    │  │
│  │   (WSGI Server)               │  │
│  │   Port: 8080                  │  │
│  └──────────────────────────────┘  │
│               │                     │
│               ▼                     │
│  ┌──────────────────────────────┐  │
│  │   Flask Application          │  │
│  │   (app_production.py)        │  │
│  └──────────────────────────────┘  │
│               │                     │
│               ▼                     │
│  ┌──────────────────────────────┐  │
│  │   Static Files               │  │
│  │   (Served by Render)         │  │
│  └──────────────────────────────┘  │
│                                      │
└─────────────────────────────────────┘
```

---

## 📊 Performance Considerations

### Computational Complexity

**Single Simulation (24h)**:
- Time steps: 288 (5-min intervals)
- NN forward passes: ~6 per step × 288 = 1,728
- Typical runtime: **< 100ms** on CPU

**Memory Usage**:
- Model weights: ~2-5 MB per digital twin
- Runtime memory: ~50-100 MB
- Food database: < 1 MB

### Optimization Strategies

1. **Model Optimization**:
   - Small network architecture (32-64 neurons)
   - ReLU activation (fast computation)
   - No recurrent connections (parallel processing)

2. **Data Processing**:
   - Pre-scaled data caching
   - Batch processing for multiple simulations
   - Lazy loading of models

3. **Web Application**:
   - Client-side rendering with Plotly
   - AJAX for asynchronous updates
   - Caching of static resources

---

## 🔐 Security Considerations

### Data Privacy
- No patient data stored on server (stateless simulations)
- Food logs stored locally (JSON files)
- No external data transmission (except voice API)

### Input Validation
- Glucose range checks (0-500 mg/dL)
- Insulin limits (0-50 U/h)
- Carb limits (0-200g)

### Web Security
- CORS protection
- Input sanitization
- Rate limiting (production)

---

## 🧪 Testing Architecture

### Test Levels

```
┌─────────────────────────────────────────┐
│  Unit Tests                              │
│  - Individual functions                  │
│  - Model components                      │
│  - Utility functions                     │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  Integration Tests                       │
│  - Full simulation pipeline              │
│  - Data preprocessing + model            │
│  - Web routes + business logic           │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  End-to-End Tests                        │
│  - Complete user workflows               │
│  - Web interface interactions            │
│  - Voice logging integration             │
└─────────────────────────────────────────┘
```

---

## 📚 Design Patterns

### Patterns Used

1. **Facade Pattern**: `DigitalTwin` class provides simple interface to complex simulation
2. **Strategy Pattern**: Different neural networks for different state variables
3. **Factory Pattern**: Scenario creation utilities
4. **Observer Pattern**: Flask routes notify UI updates
5. **Singleton Pattern**: Scaler objects shared across simulations

---

## 🔄 Future Architecture Enhancements

### Planned Improvements

1. **Microservices**: Separate simulation engine from web interface
2. **Caching Layer**: Redis for simulation results
3. **Message Queue**: Async job processing for long simulations
4. **Database**: PostgreSQL for user data and logs
5. **API Gateway**: RESTful API with versioning

### Scalability Roadmap

```
Current (v1.0)
  │
  ├─► Monolithic Flask app
  ├─► Local file storage
  └─► Synchronous processing
      │
      ▼
Future (v2.0)
  │
  ├─► Microservices architecture
  ├─► Cloud storage (S3)
  ├─► Async task queue (Celery)
  ├─► Load balancing
  └─► Horizontal scaling
```

---

<div align="center">

**Architecture documentation for Greens Digital Simulator** 🏗️

[Back to README](README.md) • [API Reference](API.md)

</div>
