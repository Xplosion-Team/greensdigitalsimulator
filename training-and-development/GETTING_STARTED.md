# 🚀 Getting Started with New Development Modules

## Quick Start Guide

This guide helps you get started with the new CGM eating experiments, backend integration, frontend design, and base time modules.

## Installation

### 1. Install Python Dependencies

```bash
cd training-and-development
pip install -r requirements.txt
```

### 2. Verify Installation

Test each module to ensure everything is working:

```bash
# Test CGM Experiments
cd cgm-experiments
python eating_tracker.py
python meal_analyzer.py
python glucose_patterns.py

# Test Data Sync
cd ../backend-integration
python data_sync.py

# Test Time Manager
cd ../base-time/utils
python time_manager.py
```

## Module Overview

### 1. CGM Eating Experiments

**Purpose**: Conduct and analyze eating experiments to understand glucose responses.

**Quick Example**:
```python
from cgm_experiments.eating_tracker import EatingExperiment

# Create experiment
experiment = EatingExperiment("Oatmeal Test", "user_001")

# Log meal
experiment.log_meal(
    meal_type="breakfast",
    foods=["oatmeal", "banana"],
    carbs=45
)

# Log glucose readings
experiment.log_glucose(120, context="pre-meal")
experiment.log_glucose(165, context="1hr post-meal")

# Save experiment
experiment.save()
```

**Learn More**: [CGM Experiments README](cgm-experiments/README.md)

### 2. Backend Integration

**Purpose**: Build APIs for CGM data management and synchronization.

**Quick Example**:
```python
# Start the API server
cd backend-integration/api
python cgm_endpoints.py

# Access API at http://localhost:8000
# View docs at http://localhost:8000/docs
```

**API Endpoints**:
- `GET /api/cgm/current` - Get current glucose
- `GET /api/cgm/history` - Get glucose history
- `POST /api/cgm/reading` - Post new reading

**Learn More**: [Backend Integration README](backend-integration/README.md)

### 3. Frontend Design

**Purpose**: Design system for building accessible CGM interfaces.

**What's Included**:
- UI component specifications
- Color system and typography
- Accessibility guidelines
- User interaction flows

**Key Components**:
- Glucose display widgets
- Trend indicators
- Timeline visualizations
- Meal logging interfaces

**Learn More**: [Frontend Design README](frontend-design/README.md)

### 4. Base Time Utilities

**Purpose**: Time management utilities for CGM applications.

**Quick Example**:
```python
from base_time.utils.time_manager import TimeManager

# Create time manager
time_mgr = TimeManager()

# Get current time
now = time_mgr.now()

# Format for display
display_time = time_mgr.format_display_time(now, 'short')
print(f"Current time: {display_time}")

# Calculate time ago
time_ago = time_mgr.time_ago(now)
print(f"Last reading: {time_ago}")
```

**Learn More**: [Base Time README](base-time/README.md)

## Common Workflows

### Workflow 1: Run an Eating Experiment

1. **Plan Experiment**
   - Choose experiment template from `cgm-experiments/experiment_templates.json`
   - Review protocol and measurements

2. **Conduct Experiment**
   ```python
   from eating_tracker import EatingExperiment
   
   exp = EatingExperiment("Test Name", "user_id")
   exp.log_meal(...)
   exp.log_glucose(...)
   exp.save()
   ```

3. **Analyze Results**
   ```python
   from meal_analyzer import MealAnalyzer
   
   analyzer = MealAnalyzer()
   results = analyzer.analyze_meal_response(exp_data)
   print(analyzer.generate_meal_report(results))
   ```

### Workflow 2: Set Up Backend API

1. **Start API Server**
   ```bash
   cd backend-integration/api
   python cgm_endpoints.py
   ```

2. **Test Endpoints**
   - Open http://localhost:8000/docs
   - Try out different endpoints
   - Post test data

3. **Integrate with Frontend**
   - Use API endpoints in your UI
   - Handle responses
   - Display data

### Workflow 3: Design UI Component

1. **Review Design System**
   - Read `frontend-design/README.md`
   - Check component specifications
   - Review color system

2. **Implement Component**
   - Follow accessibility guidelines
   - Use design tokens
   - Test with keyboard navigation

3. **Test Component**
   - Verify color contrast
   - Test screen reader support
   - Validate touch targets

## Testing

### Run All Tests

```bash
# Test CGM modules
cd cgm-experiments
python eating_tracker.py
python meal_analyzer.py
python glucose_patterns.py

# Test backend
cd ../backend-integration
python data_sync.py

# Test time utilities
cd ../base-time/utils
python time_manager.py
```

### Unit Tests (coming soon)

```bash
pytest tests/
```

## Integration with Existing Code

### With Digital Twin Simulator

```python
# Use eating experiment data to train digital twin
from t1dsim_ai.individual_model import DigitalTwin
from cgm_experiments.eating_tracker import EatingExperiment

# Load experiment
exp = EatingExperiment.load("path/to/experiment.json")

# Extract data for training
meal_data = exp.get_meal_glucose_pairs()

# Feed to digital twin for calibration
twin = DigitalTwin()
# ... calibration logic
```

### With Mobile Interface

```python
# Sync data between mobile and backend
from backend_integration.data_sync import DataSyncManager

sync_mgr = DataSyncManager()
sync_mgr.add_to_sync_queue("cgm_reading", reading_data)
sync_mgr.sync_now(backend_api_client)
```

## Troubleshooting

### Import Errors

If you get import errors, make sure you're in the correct directory:

```bash
# From training-and-development directory
cd cgm-experiments
python -c "from eating_tracker import EatingExperiment; print('Success!')"
```

### FastAPI Not Found

Install FastAPI and dependencies:

```bash
pip install fastapi uvicorn pydantic
```

### Timezone Issues

Make sure pytz is installed:

```bash
pip install pytz
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Test each module
3. 📝 Review documentation for each module
4. 🧪 Run your first eating experiment
5. 🔌 Set up the backend API
6. 🎨 Explore the design system
7. ⏰ Integrate time utilities

## Support

- **Documentation**: Each module has a detailed README
- **Examples**: Check the example code in each module
- **Questions**: Refer to main [Training & Development README](README.md)

---

**Ready to build?** Start with the module that interests you most! 🚀
