import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DexcomConnector:
    """
    Mock connector for Dexcom API real-time glucose streaming.
    In the future, this will connect to https://sandbox-api.dexcom.com/v2/
    """
    def __init__(self, patient_id="MOCK_USER_123"):
        self.patient_id = patient_id
        
    def get_latest_glucose(self):
        """
        Simulates fetching the most recent CGM value.
        """
        return {
            "value": 110 + np.random.randint(-10, 10),
            "unit": "mg/dL",
            "timestamp": datetime.now().isoformat(),
            "trend": "falling" if np.random.rand() > 0.5 else "rising"
        }

    def get_glucose_history(self, hours=24):
        """
        Simulates fetching glucose history for the last N hours.
        Used to initialize the Digital Twin state.
        """
        n_points = (hours * 60) // 5
        now = datetime.now()
        
        times = [now - timedelta(minutes=5*i) for i in range(n_points)]
        # Generate a semi-realistic wandering walk
        values = 120 + np.cumsum(np.random.normal(0, 5, n_points))
        # Clip to physiological ranges
        values = np.clip(values, 40, 400)
        
        history = pd.DataFrame({
            "timestamp": times,
            "glucose": values
        })
        return history.sort_values("timestamp")

if __name__ == "__main__":
    dexcom = DexcomConnector()
    print("Fetching latest Dexcom data...")
    print(dexcom.get_latest_glucose())
    
    print(f"\nFetching 24-hour history ({len(dexcom.get_glucose_history())} points)...")
    print(dexcom.get_glucose_history().head())
