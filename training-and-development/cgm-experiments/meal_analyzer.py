"""
Meal Analyzer Module
Analyze glucose responses to meals and identify patterns
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
import statistics


class MealAnalyzer:
    """
    Analyze meal and glucose data to understand glycemic responses
    """
    
    TARGET_RANGE = (70, 180)  # mg/dL
    SPIKE_THRESHOLD = 50  # mg/dL rise from baseline
    
    def __init__(self):
        self.analysis_results = []
    
    def analyze_meal_response(self, experiment_data: Dict) -> Dict:
        """
        Analyze glucose response to a meal
        
        Args:
            experiment_data: Dictionary with 'meal' and 'glucose_readings' keys
            
        Returns:
            Dictionary with analysis metrics
        """
        meal = experiment_data["meal"]
        readings = experiment_data["glucose_readings"]
        
        if not readings:
            return {"error": "No glucose readings found"}
        
        # Extract glucose values and times
        pre_meal = None
        peak_value = 0
        peak_time = 0
        values_1hr = []
        values_2hr = []
        
        for reading in readings:
            time_from_meal = reading.get("time_from_meal_minutes", 0)
            glucose = reading["value"]
            
            # Pre-meal baseline
            if -30 <= time_from_meal <= 0:
                if pre_meal is None or time_from_meal > -5:
                    pre_meal = glucose
            
            # Track peak
            if glucose > peak_value and time_from_meal > 0:
                peak_value = glucose
                peak_time = time_from_meal
            
            # 1-hour readings
            if 45 <= time_from_meal <= 75:
                values_1hr.append(glucose)
            
            # 2-hour readings
            if 105 <= time_from_meal <= 135:
                values_2hr.append(glucose)
        
        # Calculate metrics
        analysis = {
            "meal": {
                "type": meal["meal_type"],
                "foods": meal["foods"],
                "carbs": meal["carbs"],
                "protein": meal.get("protein", 0),
                "fat": meal.get("fat", 0)
            },
            "glucose_response": {
                "baseline": pre_meal,
                "peak_value": peak_value,
                "peak_time_minutes": peak_time,
                "rise_from_baseline": peak_value - pre_meal if pre_meal else None,
                "avg_1hr": statistics.mean(values_1hr) if values_1hr else None,
                "avg_2hr": statistics.mean(values_2hr) if values_2hr else None
            },
            "metrics": {},
            "recommendations": []
        }
        
        # Calculate derived metrics
        if pre_meal:
            rise = peak_value - pre_meal
            analysis["metrics"]["spike_magnitude"] = rise
            analysis["metrics"]["glycemic_impact"] = rise / meal["carbs"] if meal["carbs"] > 0 else 0
            
            # Classify response
            if rise < 30:
                analysis["metrics"]["response_category"] = "Excellent"
            elif rise < 50:
                analysis["metrics"]["response_category"] = "Good"
            elif rise < 80:
                analysis["metrics"]["response_category"] = "Moderate"
            else:
                analysis["metrics"]["response_category"] = "High"
        
        # Time to peak analysis
        if peak_time > 0:
            if peak_time < 45:
                analysis["metrics"]["peak_timing"] = "Fast"
                analysis["recommendations"].append(
                    "Fast peak suggests high glycemic index foods. Consider adding protein/fat."
                )
            elif peak_time <= 90:
                analysis["metrics"]["peak_timing"] = "Normal"
            else:
                analysis["metrics"]["peak_timing"] = "Delayed"
                analysis["recommendations"].append(
                    "Delayed peak may indicate high fat content slowing digestion."
                )
        
        # Generate recommendations
        if pre_meal and peak_value - pre_meal > self.SPIKE_THRESHOLD:
            analysis["recommendations"].append(
                "Significant spike detected. Consider reducing carb portion or adding more protein."
            )
        
        if values_2hr and statistics.mean(values_2hr) > self.TARGET_RANGE[1]:
            analysis["recommendations"].append(
                "2-hour glucose still elevated. May need additional insulin or reduced carbs."
            )
        
        self.analysis_results.append(analysis)
        return analysis
    
    def compare_meals(self, analyses: List[Dict]) -> Dict:
        """
        Compare multiple meal analyses to identify patterns
        """
        if not analyses:
            return {"error": "No analyses to compare"}
        
        # Group by meal type
        by_meal_type = {}
        for analysis in analyses:
            meal_type = analysis["meal"]["type"]
            if meal_type not in by_meal_type:
                by_meal_type[meal_type] = []
            by_meal_type[meal_type].append(analysis)
        
        comparison = {
            "total_meals": len(analyses),
            "by_meal_type": {}
        }
        
        # Analyze each meal type
        for meal_type, meals in by_meal_type.items():
            spikes = [
                m["glucose_response"]["rise_from_baseline"]
                for m in meals
                if m["glucose_response"]["rise_from_baseline"] is not None
            ]
            
            if spikes:
                comparison["by_meal_type"][meal_type] = {
                    "count": len(meals),
                    "avg_spike": statistics.mean(spikes),
                    "min_spike": min(spikes),
                    "max_spike": max(spikes),
                    "consistency": statistics.stdev(spikes) if len(spikes) > 1 else 0
                }
        
        return comparison
    
    def identify_problem_foods(self, analyses: List[Dict], threshold: float = 60) -> List[Dict]:
        """
        Identify foods that consistently cause high glucose spikes
        """
        food_impacts = {}
        
        for analysis in analyses:
            rise = analysis["glucose_response"].get("rise_from_baseline")
            if rise is None:
                continue
            
            foods = analysis["meal"]["foods"]
            for food in foods:
                if food not in food_impacts:
                    food_impacts[food] = []
                food_impacts[food].append(rise)
        
        problem_foods = []
        for food, rises in food_impacts.items():
            avg_rise = statistics.mean(rises)
            if avg_rise > threshold:
                problem_foods.append({
                    "food": food,
                    "avg_spike": avg_rise,
                    "occurrences": len(rises),
                    "consistency": statistics.stdev(rises) if len(rises) > 1 else 0
                })
        
        return sorted(problem_foods, key=lambda x: x["avg_spike"], reverse=True)
    
    def calculate_glycemic_index_estimate(self, food_analyses: List[Dict]) -> float:
        """
        Estimate personal glycemic index for a food based on multiple tests
        """
        if not food_analyses:
            return 0
        
        # Calculate average rise per gram of carbs
        impacts = []
        for analysis in food_analyses:
            rise = analysis["glucose_response"].get("rise_from_baseline")
            carbs = analysis["meal"]["carbs"]
            if rise and carbs > 0:
                impacts.append(rise / carbs)
        
        return statistics.mean(impacts) if impacts else 0
    
    def generate_meal_report(self, analysis: Dict) -> str:
        """
        Generate a human-readable report for a meal analysis
        """
        report_lines = [
            "=" * 60,
            "MEAL ANALYSIS REPORT",
            "=" * 60,
            "",
            f"Meal Type: {analysis['meal']['type'].title()}",
            f"Foods: {', '.join(analysis['meal']['foods'])}",
            f"Macros: {analysis['meal']['carbs']}g carbs, "
            f"{analysis['meal']['protein']}g protein, "
            f"{analysis['meal']['fat']}g fat",
            "",
            "GLUCOSE RESPONSE:",
            f"  Baseline: {analysis['glucose_response']['baseline']} mg/dL",
            f"  Peak: {analysis['glucose_response']['peak_value']} mg/dL "
            f"(at {analysis['glucose_response']['peak_time_minutes']} min)",
            f"  Rise: {analysis['glucose_response']['rise_from_baseline']} mg/dL",
            "",
        ]
        
        if "response_category" in analysis["metrics"]:
            report_lines.append(
                f"Response Category: {analysis['metrics']['response_category']}"
            )
        
        if analysis.get("recommendations"):
            report_lines.append("")
            report_lines.append("RECOMMENDATIONS:")
            for i, rec in enumerate(analysis["recommendations"], 1):
                report_lines.append(f"  {i}. {rec}")
        
        report_lines.append("")
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)


class GlucoseMetrics:
    """
    Calculate standard glucose control metrics
    """
    
    @staticmethod
    def time_in_range(readings: List[float], target_range: tuple = (70, 180)) -> float:
        """
        Calculate percentage of time in target range
        """
        if not readings:
            return 0
        
        in_range = sum(1 for r in readings if target_range[0] <= r <= target_range[1])
        return (in_range / len(readings)) * 100
    
    @staticmethod
    def coefficient_of_variation(readings: List[float]) -> float:
        """
        Calculate CV% - measure of glucose variability
        """
        if not readings or len(readings) < 2:
            return 0
        
        mean = statistics.mean(readings)
        std = statistics.stdev(readings)
        return (std / mean) * 100 if mean > 0 else 0
    
    @staticmethod
    def glucose_management_indicator(readings: List[float]) -> float:
        """
        Estimate GMI (equivalent to HbA1c)
        GMI = 3.31 + 0.02392 * mean_glucose
        """
        if not readings:
            return 0
        
        mean_glucose = statistics.mean(readings)
        return 3.31 + 0.02392 * mean_glucose


if __name__ == "__main__":
    # Example usage
    print("Meal Analyzer Example")
    print("-" * 60)
    
    # Sample meal data
    meal_data = {
        "meal": {
            "meal_type": "breakfast",
            "foods": ["oatmeal", "banana"],
            "carbs": 45,
            "protein": 8,
            "fat": 5
        },
        "glucose_readings": [
            {"value": 110, "time_from_meal_minutes": -5, "context": "pre-meal"},
            {"value": 135, "time_from_meal_minutes": 30, "context": "30-min"},
            {"value": 165, "time_from_meal_minutes": 60, "context": "1-hour"},
            {"value": 145, "time_from_meal_minutes": 120, "context": "2-hour"}
        ]
    }
    
    # Analyze the meal
    analyzer = MealAnalyzer()
    result = analyzer.analyze_meal_response(meal_data)
    
    # Print report
    report = analyzer.generate_meal_report(result)
    print(report)
    
    # Calculate glucose metrics
    glucose_values = [r["value"] for r in meal_data["glucose_readings"]]
    tir = GlucoseMetrics.time_in_range(glucose_values)
    cv = GlucoseMetrics.coefficient_of_variation(glucose_values)
    
    print(f"\nTime in Range: {tir:.1f}%")
    print(f"Coefficient of Variation: {cv:.1f}%")
