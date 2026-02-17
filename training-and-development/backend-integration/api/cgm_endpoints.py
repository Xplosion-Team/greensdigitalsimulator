"""
CGM API Endpoints
FastAPI endpoints for CGM data access and management
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import statistics

app = FastAPI(
    title="CGM Data API",
    description="API for accessing and managing CGM data",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data Models
class CGMReading(BaseModel):
    """CGM glucose reading"""
    glucose: float = Field(..., ge=20, le=600, description="Glucose value in mg/dL")
    timestamp: str = Field(..., description="ISO format timestamp")
    source: Optional[str] = Field("manual", description="Data source (cgm_sensor, manual)")
    trend: Optional[str] = Field(None, description="Trend direction")
    
    @validator('glucose')
    def validate_glucose(cls, v):
        if v < 20 or v > 600:
            raise ValueError('Glucose must be between 20 and 600 mg/dL')
        return v


class CGMHistory(BaseModel):
    """Historical CGM data"""
    readings: List[Dict]
    summary: Dict


class GlucoseSummary(BaseModel):
    """Summary statistics for glucose data"""
    avg: float
    min: float
    max: float
    std_dev: float
    time_in_range: float
    time_below_range: float
    time_above_range: float
    coefficient_of_variation: float


# In-memory storage (replace with database in production)
cgm_data_store = {}


# Helper Functions
def calculate_trend(recent_readings: List[float]) -> str:
    """Calculate glucose trend from recent readings"""
    if len(recent_readings) < 3:
        return "stable"
    
    first = recent_readings[0]
    last = recent_readings[-1]
    change = last - first
    rate = change / len(recent_readings)
    
    if rate > 2:
        return "rapidly_rising"
    elif rate > 0.5:
        return "rising"
    elif rate < -2:
        return "rapidly_falling"
    elif rate < -0.5:
        return "falling"
    else:
        return "stable"


def calculate_summary(readings: List[Dict], target_range=(70, 180)) -> GlucoseSummary:
    """Calculate summary statistics for glucose readings"""
    if not readings:
        return GlucoseSummary(
            avg=0, min=0, max=0, std_dev=0,
            time_in_range=0, time_below_range=0, time_above_range=0,
            coefficient_of_variation=0
        )
    
    values = [r["glucose"] for r in readings]
    
    in_range = sum(1 for v in values if target_range[0] <= v <= target_range[1])
    below_range = sum(1 for v in values if v < target_range[0])
    above_range = sum(1 for v in values if v > target_range[1])
    total = len(values)
    
    avg = statistics.mean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0
    cv = (std / avg * 100) if avg > 0 else 0
    
    return GlucoseSummary(
        avg=round(avg, 1),
        min=min(values),
        max=max(values),
        std_dev=round(std, 1),
        time_in_range=round((in_range / total) * 100, 1),
        time_below_range=round((below_range / total) * 100, 1),
        time_above_range=round((above_range / total) * 100, 1),
        coefficient_of_variation=round(cv, 1)
    )


# API Endpoints

@app.get("/")
def root():
    """API root endpoint"""
    return {
        "message": "CGM Data API",
        "version": "1.0.0",
        "endpoints": {
            "current": "/api/cgm/current",
            "history": "/api/cgm/history",
            "post_reading": "/api/cgm/reading",
            "stats": "/api/cgm/stats"
        }
    }


@app.get("/api/cgm/current")
def get_current_glucose(user_id: str = "default"):
    """Get the most recent glucose reading"""
    if user_id not in cgm_data_store or not cgm_data_store[user_id]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No glucose readings found for user"
        )
    
    readings = cgm_data_store[user_id]
    latest = readings[-1]
    
    # Calculate trend from recent readings
    recent_values = [r["glucose"] for r in readings[-5:]]
    trend = calculate_trend(recent_values)
    
    # Trend arrows
    trend_arrows = {
        "rapidly_rising": "↑↑",
        "rising": "↑",
        "stable": "→",
        "falling": "↓",
        "rapidly_falling": "↓↓"
    }
    
    return {
        "glucose": latest["glucose"],
        "timestamp": latest["timestamp"],
        "trend": trend,
        "trend_arrow": trend_arrows.get(trend, "→"),
        "source": latest.get("source", "unknown")
    }


@app.get("/api/cgm/history")
def get_glucose_history(
    user_id: str = "default",
    hours: int = 24,
    include_summary: bool = True
):
    """Get glucose reading history"""
    if user_id not in cgm_data_store:
        return {
            "readings": [],
            "summary": None,
            "message": "No data found for user"
        }
    
    all_readings = cgm_data_store[user_id]
    
    # Filter by time
    cutoff_time = datetime.now() - timedelta(hours=hours)
    filtered_readings = [
        r for r in all_readings
        if datetime.fromisoformat(r["timestamp"]) >= cutoff_time
    ]
    
    response = {"readings": filtered_readings}
    
    if include_summary:
        summary = calculate_summary(filtered_readings)
        response["summary"] = summary.dict()
    
    return response


@app.post("/api/cgm/reading")
def post_cgm_reading(reading: CGMReading, user_id: str = "default"):
    """Post a new CGM reading"""
    if user_id not in cgm_data_store:
        cgm_data_store[user_id] = []
    
    reading_dict = reading.dict()
    reading_dict["created_at"] = datetime.now().isoformat()
    
    cgm_data_store[user_id].append(reading_dict)
    
    # Keep only last 1000 readings per user
    if len(cgm_data_store[user_id]) > 1000:
        cgm_data_store[user_id] = cgm_data_store[user_id][-1000:]
    
    return {
        "success": True,
        "reading_id": f"{user_id}_{len(cgm_data_store[user_id])}",
        "message": "Reading stored successfully"
    }


@app.get("/api/cgm/stats")
def get_glucose_stats(user_id: str = "default", days: int = 7):
    """Get glucose statistics over specified period"""
    if user_id not in cgm_data_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data found for user"
        )
    
    cutoff_time = datetime.now() - timedelta(days=days)
    readings = [
        r for r in cgm_data_store[user_id]
        if datetime.fromisoformat(r["timestamp"]) >= cutoff_time
    ]
    
    if not readings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No readings found in the last {days} days"
        )
    
    summary = calculate_summary(readings)
    
    # Calculate GMI (Glucose Management Indicator)
    gmi = 3.31 + 0.02392 * summary.avg
    
    return {
        "period_days": days,
        "total_readings": len(readings),
        "statistics": summary.dict(),
        "gmi": round(gmi, 1),
        "estimated_a1c": round(gmi, 1)
    }


@app.delete("/api/cgm/data")
def delete_user_data(user_id: str = "default"):
    """Delete all CGM data for a user"""
    if user_id in cgm_data_store:
        del cgm_data_store[user_id]
        return {"success": True, "message": f"Data deleted for user {user_id}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User data not found"
        )


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_users": len(cgm_data_store)
    }


if __name__ == "__main__":
    import uvicorn
    
    print("Starting CGM Data API Server...")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative Docs: http://localhost:8000/redoc")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
