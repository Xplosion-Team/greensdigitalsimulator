"""
Glucose Patterns Module
Detect and analyze patterns in CGM data
"""

from typing import List, Dict, Tuple, Optional
import statistics
from datetime import datetime, timedelta


class GlucosePatternDetector:
    """
    Detect patterns and trends in continuous glucose data
    """
    
    def __init__(self):
        self.patterns = []
    
    def detect_spike(
        self,
        readings: List[Dict],
        threshold: float = 50,
        time_window_minutes: int = 60
    ) -> List[Dict]:
        """
        Detect glucose spikes in a series of readings
        
        Args:
            readings: List of glucose readings with 'value' and 'timestamp'
            threshold: Minimum rise to be considered a spike (mg/dL)
            time_window_minutes: Time window to evaluate spike
            
        Returns:
            List of detected spikes with details
        """
        spikes = []
        
        for i in range(len(readings) - 1):
            current = readings[i]
            
            # Look ahead for peak
            future_window = []
            for j in range(i + 1, len(readings)):
                time_diff = self._time_diff_minutes(
                    current["timestamp"],
                    readings[j]["timestamp"]
                )
                if time_diff <= time_window_minutes:
                    future_window.append(readings[j])
                else:
                    break
            
            if future_window:
                peak_reading = max(future_window, key=lambda x: x["value"])
                rise = peak_reading["value"] - current["value"]
                
                if rise >= threshold:
                    spikes.append({
                        "start_time": current["timestamp"],
                        "start_value": current["value"],
                        "peak_time": peak_reading["timestamp"],
                        "peak_value": peak_reading["value"],
                        "rise": rise,
                        "duration_minutes": self._time_diff_minutes(
                            current["timestamp"],
                            peak_reading["timestamp"]
                        )
                    })
        
        return spikes
    
    def detect_trend(
        self,
        readings: List[Dict],
        window_size: int = 3
    ) -> str:
        """
        Detect overall trend (rising, falling, stable)
        
        Args:
            readings: List of glucose readings
            window_size: Number of readings to analyze
            
        Returns:
            Trend description: 'rising', 'falling', 'stable', 'rapidly_rising', 'rapidly_falling'
        """
        if len(readings) < window_size:
            return "insufficient_data"
        
        recent = readings[-window_size:]
        values = [r["value"] for r in recent]
        
        # Calculate rate of change
        first_value = values[0]
        last_value = values[-1]
        change = last_value - first_value
        
        time_span = self._time_diff_minutes(
            recent[0]["timestamp"],
            recent[-1]["timestamp"]
        )
        
        if time_span > 0:
            rate = change / time_span  # mg/dL per minute
        else:
            rate = 0
        
        # Classify trend
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
    
    def detect_variability(
        self,
        readings: List[Dict],
        time_window_hours: int = 24
    ) -> Dict:
        """
        Analyze glucose variability over a time window
        """
        if not readings:
            return {"error": "No readings provided"}
        
        values = [r["value"] for r in readings]
        
        return {
            "mean": statistics.mean(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
            "coefficient_of_variation": (
                (statistics.stdev(values) / statistics.mean(values)) * 100
                if len(values) > 1 and statistics.mean(values) > 0
                else 0
            ),
            "range": max(values) - min(values),
            "min": min(values),
            "max": max(values)
        }
    
    def detect_hypoglycemia_risk(
        self,
        readings: List[Dict],
        threshold: float = 70,
        trend_threshold: float = -1.5  # mg/dL per minute
    ) -> Dict:
        """
        Detect potential hypoglycemia risk based on current value and trend
        """
        if not readings:
            return {"risk": "unknown"}
        
        current = readings[-1]
        current_value = current["value"]
        trend = self.detect_trend(readings, window_size=min(3, len(readings)))
        
        risk_level = "low"
        warnings = []
        
        # Check current value
        if current_value < threshold:
            risk_level = "high"
            warnings.append(f"Current glucose {current_value} is below {threshold} mg/dL")
        elif current_value < threshold + 10:
            risk_level = "moderate"
            warnings.append(f"Glucose {current_value} is approaching low threshold")
        
        # Check trend
        if trend in ["rapidly_falling", "falling"] and current_value < 100:
            if risk_level == "low":
                risk_level = "moderate"
            warnings.append("Falling trend detected with borderline glucose")
        
        return {
            "risk_level": risk_level,
            "current_glucose": current_value,
            "trend": trend,
            "warnings": warnings,
            "recommendations": self._get_hypo_recommendations(risk_level, trend)
        }
    
    def detect_dawn_phenomenon(
        self,
        readings: List[Dict],
        target_hours: Tuple[int, int] = (4, 8)
    ) -> Optional[Dict]:
        """
        Detect dawn phenomenon (early morning glucose rise)
        """
        # Filter readings to early morning hours
        morning_readings = []
        for reading in readings:
            timestamp = datetime.fromisoformat(reading["timestamp"])
            hour = timestamp.hour
            if target_hours[0] <= hour < target_hours[1]:
                morning_readings.append(reading)
        
        if len(morning_readings) < 3:
            return None
        
        # Calculate rise during dawn hours
        first_value = morning_readings[0]["value"]
        last_value = morning_readings[-1]["value"]
        rise = last_value - first_value
        
        duration = self._time_diff_minutes(
            morning_readings[0]["timestamp"],
            morning_readings[-1]["timestamp"]
        ) / 60  # hours
        
        if rise > 20 and duration > 1:
            return {
                "detected": True,
                "start_glucose": first_value,
                "end_glucose": last_value,
                "rise": rise,
                "duration_hours": duration,
                "severity": "significant" if rise > 40 else "moderate"
            }
        
        return {"detected": False}
    
    def analyze_post_meal_pattern(
        self,
        readings: List[Dict],
        meal_time: str
    ) -> Dict:
        """
        Analyze glucose pattern after a meal
        """
        meal_dt = datetime.fromisoformat(meal_time)
        
        # Find baseline (30 min before meal)
        baseline = None
        for reading in readings:
            reading_dt = datetime.fromisoformat(reading["timestamp"])
            diff = (reading_dt - meal_dt).total_seconds() / 60
            if -30 <= diff <= 0:
                baseline = reading["value"]
                break
        
        # Track post-meal progression
        progression = []
        for reading in readings:
            reading_dt = datetime.fromisoformat(reading["timestamp"])
            diff = (reading_dt - meal_dt).total_seconds() / 60
            if 0 <= diff <= 180:  # 3 hours post-meal
                progression.append({
                    "time_from_meal": diff,
                    "glucose": reading["value"]
                })
        
        if not progression:
            return {"error": "No post-meal data found"}
        
        # Find peak
        peak = max(progression, key=lambda x: x["glucose"])
        
        # Analyze pattern
        pattern = {
            "baseline": baseline,
            "peak_glucose": peak["glucose"],
            "peak_time_minutes": peak["time_from_meal"],
            "rise_from_baseline": peak["glucose"] - baseline if baseline else None,
            "progression": progression
        }
        
        # Classify response shape
        if peak["time_from_meal"] < 45:
            pattern["response_shape"] = "rapid_peak"
        elif peak["time_from_meal"] <= 90:
            pattern["response_shape"] = "normal_peak"
        else:
            pattern["response_shape"] = "delayed_peak"
        
        return pattern
    
    def _time_diff_minutes(self, time1: str, time2: str) -> float:
        """Calculate time difference in minutes"""
        dt1 = datetime.fromisoformat(time1)
        dt2 = datetime.fromisoformat(time2)
        return abs((dt2 - dt1).total_seconds() / 60)
    
    def _get_hypo_recommendations(self, risk_level: str, trend: str) -> List[str]:
        """Get recommendations based on hypoglycemia risk"""
        if risk_level == "high":
            return [
                "Treat immediately with 15g fast-acting carbs",
                "Recheck glucose in 15 minutes",
                "Contact healthcare provider if needed"
            ]
        elif risk_level == "moderate":
            if trend in ["rapidly_falling", "falling"]:
                return [
                    "Consider having a small snack with carbs",
                    "Monitor glucose closely",
                    "Avoid strenuous activity"
                ]
            return ["Monitor glucose closely", "Have fast-acting carbs available"]
        else:
            return ["Continue normal monitoring"]


class PatternVisualizer:
    """
    Generate text-based visualizations of glucose patterns
    """
    
    @staticmethod
    def glucose_chart(readings: List[Dict], width: int = 60) -> str:
        """
        Create a simple ASCII chart of glucose readings
        """
        if not readings:
            return "No data to visualize"
        
        values = [r["value"] for r in readings]
        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val if max_val > min_val else 1
        
        lines = [
            "Glucose Pattern Chart",
            "-" * width,
            f"High: {max_val:.0f} mg/dL",
            ""
        ]
        
        # Create chart
        for reading in readings:
            value = reading["value"]
            normalized = (value - min_val) / range_val
            bar_length = int(normalized * (width - 15))
            bar = "█" * bar_length
            
            timestamp = datetime.fromisoformat(reading["timestamp"])
            time_str = timestamp.strftime("%H:%M")
            
            lines.append(f"{time_str} {bar} {value:.0f}")
        
        lines.extend([
            "",
            f"Low:  {min_val:.0f} mg/dL",
            "-" * width
        ])
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    print("Glucose Pattern Detector Example")
    print("-" * 60)
    
    # Sample glucose readings
    base_time = datetime.now()
    readings = [
        {"value": 110, "timestamp": (base_time - timedelta(minutes=60)).isoformat()},
        {"value": 115, "timestamp": (base_time - timedelta(minutes=45)).isoformat()},
        {"value": 140, "timestamp": (base_time - timedelta(minutes=30)).isoformat()},
        {"value": 170, "timestamp": (base_time - timedelta(minutes=15)).isoformat()},
        {"value": 165, "timestamp": base_time.isoformat()},
    ]
    
    # Detect patterns
    detector = GlucosePatternDetector()
    
    spikes = detector.detect_spike(readings, threshold=40)
    print(f"\nDetected {len(spikes)} spike(s)")
    
    trend = detector.detect_trend(readings)
    print(f"Current trend: {trend}")
    
    variability = detector.detect_variability(readings)
    print(f"Variability: CV = {variability['coefficient_of_variation']:.1f}%")
    
    hypo_risk = detector.detect_hypoglycemia_risk(readings)
    print(f"Hypoglycemia risk: {hypo_risk['risk_level']}")
    
    # Visualize
    visualizer = PatternVisualizer()
    chart = visualizer.glucose_chart(readings)
    print(f"\n{chart}")
