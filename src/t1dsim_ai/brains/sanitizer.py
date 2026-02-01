import pandas as pd
from typing import Dict, Any

class BrainSanitizer:
    """
    Enforces privacy by extracting only anonymous summary statistics from 
    raw simulation data. Ensures no PHI or time-series data leaves the environment.
    """
    
    @staticmethod
    def summarize_simulation(results: pd.DataFrame, params: Dict[str, Any], start_glucose: float) -> Dict[str, Any]:
        """
        Extracts key metrics for LLM interpretation without sharing raw data points.
        """
        # We only pass scalars and relative terms to the LLM
        summary = {
            "start_glucose": float(start_glucose),
            "max_glucose": float(results.cgm_NNDT.max()),
            "min_glucose": float(results.cgm_NNDT.min()),
            "final_glucose": float(results.cgm_NNDT.iloc[-1]),
            "glucose_rise": float(results.cgm_NNDT.max() - start_glucose),
            "time_to_peak_mins": int(results.cgm_NNDT.idxmax() * 5), # 5 min intervals
        }
        
        # Merge with non-identifiable intent params (e.g. carbs)
        for key in ["carbs", "type", "exercise_intensity"]:
            if key in params:
                summary[key] = params[key]
                
        return summary
