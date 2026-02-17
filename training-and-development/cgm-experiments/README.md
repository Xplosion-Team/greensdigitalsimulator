# 🍽️ CGM Eating Experiments Module

## Overview
This module provides tools and frameworks for conducting CGM (Continuous Glucose Monitoring) eating experiments to understand glucose responses to different meals and eating patterns.

## Purpose
- Track and analyze glucose responses to various foods
- Identify patterns in meal timing and glucose spikes
- Experiment with different meal compositions
- Build personalized glucose prediction models

## Module Structure

```
cgm-experiments/
├── README.md                        # This file
├── eating_tracker.py                # Meal and glucose tracking
├── meal_analyzer.py                 # Meal composition and glucose response analysis
├── glucose_patterns.py              # Pattern recognition in CGM data
├── experiment_templates.json        # Pre-defined experiment protocols
└── results/                         # Experiment results and data
    ├── experiments_log.json
    └── analysis_reports/
```

## Key Components

### 1. Eating Tracker (`eating_tracker.py`)
- Log meals with timestamp, composition, and portion sizes
- Track pre-meal and post-meal glucose readings
- Record eating context (time of day, activity level, stress)
- Export data for analysis

### 2. Meal Analyzer (`meal_analyzer.py`)
- Calculate glycemic impact of meals
- Analyze glucose spike patterns
- Identify optimal meal timing
- Compare similar meals for consistency

### 3. Glucose Patterns (`glucose_patterns.py`)
- Detect glucose response patterns
- Identify rapid rises and delayed peaks
- Analyze post-meal trends
- Generate visual reports

## Experiment Types

### Basic Experiments
1. **Single Food Testing**: Test individual foods to understand their glycemic impact
2. **Meal Timing**: Compare glucose responses at different times of day
3. **Portion Control**: Test different portion sizes of the same meal
4. **Food Combinations**: Analyze how food pairings affect glucose

### Advanced Experiments
1. **Pre-bolus Timing**: Optimize insulin timing relative to meals
2. **Exercise Effects**: Understand post-meal activity impact
3. **Stress Response**: Track glucose during different stress levels
4. **Sleep Patterns**: Correlate sleep quality with glucose control

## Getting Started

### Running Your First Experiment

```python
from eating_tracker import EatingExperiment
from meal_analyzer import MealAnalyzer

# Create a new experiment
experiment = EatingExperiment(
    name="Morning Oatmeal Test",
    participant_id="user_001"
)

# Log a meal
experiment.log_meal(
    meal_type="breakfast",
    foods=["oatmeal", "banana", "almonds"],
    carbs=45,
    protein=8,
    fat=10,
    time="2026-02-17T08:00:00"
)

# Track glucose readings
experiment.log_glucose(120, timestamp="2026-02-17T08:00:00")  # Pre-meal
experiment.log_glucose(145, timestamp="2026-02-17T08:30:00")  # 30 min post
experiment.log_glucose(165, timestamp="2026-02-17T09:00:00")  # 1 hr post
experiment.log_glucose(140, timestamp="2026-02-17T10:00:00")  # 2 hr post

# Analyze results
analyzer = MealAnalyzer()
results = analyzer.analyze_meal_response(experiment)
print(results)
```

## Best Practices

1. **Consistency**: Test meals at similar times and contexts
2. **Documentation**: Record all relevant details (stress, sleep, activity)
3. **Repetition**: Test meals multiple times to confirm patterns
4. **Control Variables**: Change one variable at a time
5. **Pre-meal Readings**: Always start with stable baseline glucose

## Integration with Digital Twin

The CGM eating experiments data can be used to:
- Calibrate personal glucose prediction models
- Improve meal response accuracy
- Validate digital twin predictions
- Train AI models on individual patterns

## Safety Notes

- Always follow your healthcare provider's guidance
- Monitor for unexpected glucose patterns
- Have fast-acting carbs available for lows
- Don't experiment during critical times (driving, working, etc.)

## Data Privacy

All experiment data is stored locally and never transmitted without explicit consent. Personal health information is protected and encrypted.

---

**Next Steps**: 
1. Review the experiment templates
2. Run your first simple food test
3. Build your personal food database
4. Share findings with your healthcare team

For questions or support, refer to the main [Training & Development](../README.md) guide.
