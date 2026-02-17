from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from t1dsim_ai.individual_model import DigitalTwin
import numpy as np
import json

app = FastAPI()

# Enable CORS for mobile app access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize simulation data
try:
    df_base = pd.read_csv("example/data_example/data_example.csv")
    df_base = df_base[~df_base.is_train]
    myDigitalTwin = DigitalTwin(n_digitalTwin=4)
except Exception as e:
    print(f"Error initializing data: {e}")
    df_base = None

@app.get("/")
def read_root():
    return {"message": "Greens Digital Twin API is running"}

@app.get("/status")
def get_status():
    return {"status": "online", "model": "DigitalTwin-4"}

@app.get("/simulate/{day}")
def simulate_day(day: int):
    if df_base is None:
        raise HTTPException(status_code=500, detail="Simulation data not loaded")
    
    if day < 0 or day > 2:
        raise HTTPException(status_code=400, detail="Day must be between 0 and 2")

    try:
        # Simulate a specific day window (12 readings per hour * 24 hours = 288 readings)
        start_idx = day * 12 * 24
        end_idx = (day + 1) * 12 * 24
        
        df_window = df_base.iloc[start_idx:end_idx].copy()
        df_result = myDigitalTwin.simulate(df_window)
        
        # Calculate trend and state
        # readings are every 5 minutes
        df_result['trend'] = df_result['cgm_NNDT'].diff() / 5.0
        df_result['trend'] = df_result['trend'].fillna(0)
        
        def classify(row):
            glucose = row['cgm_NNDT']
            trend = row['trend']
            
            if glucose < 70: return "Low"
            if glucose > 180: return "High"
            
            if trend > 2: return "Rapid Rise"
            if trend > 1: return "Trending High"
            if trend < -2: return "Rapid Fall"
            if trend < -1: return "Trending Low"
            
            return "Stable"

        df_result['state'] = df_result.apply(classify, axis=1)
        
        # Convert to list of dicts for JSON response
        records = df_result.reset_index().to_dict(orient='records')
        
        # Clean up NaN values for JSON compatibility
        cleaned_records = []
        for r in records:
            cleaned_r = {k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in r.items()}
            cleaned_records.append(cleaned_r)
            
        return cleaned_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
