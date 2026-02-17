# 🔌 Backend Integration Module

## Overview
This module provides backend integration components for CGM data processing, API endpoints, and data synchronization between the digital twin simulator and various frontends (web, mobile).

## Purpose
- Define API endpoints for CGM data access
- Handle real-time data synchronization
- Process and validate incoming CGM data
- Integrate eating experiments with the digital twin simulation
- Provide secure data storage and retrieval

## Module Structure

```
backend-integration/
├── README.md                    # This file
├── api/
│   ├── cgm_endpoints.py         # CGM data API endpoints
│   ├── experiments_api.py       # Eating experiments API
│   └── auth_middleware.py       # Authentication and security
├── data_sync.py                 # Data synchronization utilities
├── cgm_processor.py             # CGM data processing pipeline
└── database_models.py           # Data models for storage
```

## API Endpoints

### CGM Data Endpoints

#### Get Current Glucose
```
GET /api/cgm/current
Response: {
  "glucose": 120,
  "timestamp": "2026-02-17T10:30:00Z",
  "trend": "stable",
  "trend_arrow": "→"
}
```

#### Get Glucose History
```
GET /api/cgm/history?hours=24
Response: {
  "readings": [
    {"glucose": 115, "timestamp": "2026-02-17T09:00:00Z"},
    {"glucose": 120, "timestamp": "2026-02-17T09:30:00Z"},
    ...
  ],
  "summary": {
    "avg": 125,
    "min": 85,
    "max": 165,
    "time_in_range": 85.5
  }
}
```

#### Post CGM Reading
```
POST /api/cgm/reading
Body: {
  "glucose": 145,
  "timestamp": "2026-02-17T10:45:00Z",
  "source": "cgm_sensor"
}
Response: {
  "success": true,
  "reading_id": "abc123"
}
```

### Experiment Endpoints

#### Get Active Experiments
```
GET /api/experiments/active
Response: {
  "experiments": [
    {
      "id": "exp_001",
      "name": "Oatmeal Breakfast Test",
      "status": "in_progress",
      "next_measurement": "2026-02-17T11:00:00Z"
    }
  ]
}
```

#### Log Meal
```
POST /api/experiments/log-meal
Body: {
  "experiment_id": "exp_001",
  "meal_type": "breakfast",
  "foods": ["oatmeal", "banana"],
  "carbs": 45,
  "protein": 8,
  "fat": 5
}
Response: {
  "success": true,
  "meal_id": "meal_123"
}
```

#### Get Experiment Results
```
GET /api/experiments/{experiment_id}/results
Response: {
  "experiment": {...},
  "analysis": {
    "avg_spike": 48,
    "peak_time": 65,
    "response_category": "Good"
  },
  "recommendations": [...]
}
```

### Digital Twin Integration

#### Run Simulation
```
POST /api/simulation/run
Body: {
  "participant_id": "user_001",
  "meals": [...],
  "insulin": [...],
  "duration_hours": 24
}
Response: {
  "prediction": {
    "glucose_curve": [...],
    "time_in_range": 82.3,
    "estimated_a1c": 6.8
  }
}
```

## Data Synchronization

### Real-time Sync
- WebSocket connections for live CGM data streaming
- Automatic conflict resolution for offline changes
- Delta synchronization to minimize bandwidth
- Background sync for mobile apps

### Sync Architecture
```
Mobile App / Web Client
        ↓
    WebSocket / REST API
        ↓
    Sync Manager
        ↓
    ┌─────────┬─────────┬─────────┐
    │         │         │         │
CGM Data  Meals    Experiments  Digital Twin
    │         │         │         │
    └─────────┴─────────┴─────────┘
              ↓
        Local Database
```

## Security & Authentication

### API Authentication
- JWT tokens for API access
- Refresh token rotation
- Rate limiting per user
- CORS configuration for web clients

### Data Privacy
- End-to-end encryption for sensitive data
- Local-first data storage
- Optional cloud backup with encryption
- HIPAA-compliant data handling

## Integration Points

### 1. CGM Devices
- Dexcom G6/G7 integration
- Libre integration
- Manual entry fallback

### 2. Digital Twin Simulator
- Feed experiment data to train models
- Use predictions for meal planning
- Calibrate models with real data

### 3. Mobile/Web Applications
- Real-time glucose display
- Experiment tracking UI
- Push notifications for alerts

## Data Processing Pipeline

```python
# Example data processing flow
from cgm_processor import CGMProcessor

processor = CGMProcessor()

# 1. Receive raw CGM data
raw_data = {
    "glucose": 145,
    "timestamp": "2026-02-17T10:30:00Z",
    "sensor_id": "sensor_001"
}

# 2. Validate and clean
validated_data = processor.validate(raw_data)

# 3. Detect patterns
patterns = processor.detect_patterns(validated_data)

# 4. Generate alerts if needed
alerts = processor.check_alerts(validated_data)

# 5. Store in database
processor.save(validated_data, patterns, alerts)

# 6. Sync to clients
processor.broadcast_update(validated_data)
```

## Database Schema

### CGM Readings
```sql
CREATE TABLE cgm_readings (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    glucose FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    source VARCHAR(50),
    trend VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Experiments
```sql
CREATE TABLE experiments (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    name VARCHAR(255),
    template_id VARCHAR(50),
    status VARCHAR(20),
    created_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

### Meals
```sql
CREATE TABLE meals (
    id UUID PRIMARY KEY,
    experiment_id UUID,
    user_id UUID NOT NULL,
    meal_type VARCHAR(50),
    foods JSONB,
    carbs FLOAT,
    protein FLOAT,
    fat FLOAT,
    timestamp TIMESTAMP,
    notes TEXT
);
```

## Error Handling

### API Error Responses
```json
{
  "error": {
    "code": "INVALID_GLUCOSE_VALUE",
    "message": "Glucose value must be between 20 and 600 mg/dL",
    "timestamp": "2026-02-17T10:30:00Z"
  }
}
```

### Error Codes
- `INVALID_GLUCOSE_VALUE`: Glucose outside acceptable range
- `MISSING_REQUIRED_FIELD`: Required field not provided
- `EXPERIMENT_NOT_FOUND`: Referenced experiment doesn't exist
- `UNAUTHORIZED`: Authentication failed
- `RATE_LIMIT_EXCEEDED`: Too many requests

## Performance Considerations

- Cache frequently accessed data (last 24h of readings)
- Batch database writes where possible
- Use connection pooling for database
- Implement CDN for static assets
- Compress API responses

## Deployment

### Development
```bash
# Start backend server
python backend-integration/api/cgm_endpoints.py

# Run in debug mode
DEBUG=true python backend-integration/api/cgm_endpoints.py
```

### Production
```bash
# Use production WSGI server (Gunicorn)
gunicorn -w 4 -b 0.0.0.0:8000 api.cgm_endpoints:app

# With SSL
gunicorn -w 4 -b 0.0.0.0:443 \
  --certfile=/path/to/cert.pem \
  --keyfile=/path/to/key.pem \
  api.cgm_endpoints:app
```

## Testing

### Unit Tests
```python
# Test CGM endpoint
def test_post_cgm_reading():
    response = client.post('/api/cgm/reading', json={
        'glucose': 120,
        'timestamp': '2026-02-17T10:00:00Z'
    })
    assert response.status_code == 200
    assert response.json['success'] == True
```

### Integration Tests
- End-to-end API flows
- Database integration
- WebSocket connections
- Authentication flows

---

**Next Steps**:
1. Review API endpoint specifications
2. Set up development database
3. Implement authentication
4. Test with frontend applications

For questions or support, refer to the main [Training & Development](../README.md) guide.
