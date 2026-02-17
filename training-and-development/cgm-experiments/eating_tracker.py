"""
Eating Tracker Module
Track meals and glucose responses for CGM eating experiments
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class EatingExperiment:
    """
    Track eating experiments including meals and glucose readings
    """
    
    def __init__(self, name: str, participant_id: str, results_dir: str = "results"):
        self.name = name
        self.participant_id = participant_id
        self.created_at = datetime.now().isoformat()
        self.meals = []
        self.glucose_readings = []
        self.notes = []
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
    def log_meal(
        self,
        meal_type: str,
        foods: List[str],
        carbs: float,
        protein: float = 0,
        fat: float = 0,
        time: Optional[str] = None,
        notes: str = ""
    ):
        """
        Log a meal entry
        
        Args:
            meal_type: breakfast, lunch, dinner, snack
            foods: List of food items
            carbs: Carbohydrate content in grams
            protein: Protein content in grams
            fat: Fat content in grams
            time: ISO format timestamp (defaults to now)
            notes: Additional notes about the meal
        """
        meal_entry = {
            "meal_type": meal_type,
            "foods": foods,
            "carbs": carbs,
            "protein": protein,
            "fat": fat,
            "timestamp": time or datetime.now().isoformat(),
            "notes": notes
        }
        self.meals.append(meal_entry)
        return meal_entry
    
    def log_glucose(self, value: float, timestamp: Optional[str] = None, context: str = ""):
        """
        Log a glucose reading
        
        Args:
            value: Glucose value in mg/dL
            timestamp: ISO format timestamp (defaults to now)
            context: Context of reading (pre-meal, post-meal, etc.)
        """
        glucose_entry = {
            "value": value,
            "timestamp": timestamp or datetime.now().isoformat(),
            "context": context
        }
        self.glucose_readings.append(glucose_entry)
        return glucose_entry
    
    def add_note(self, note: str, timestamp: Optional[str] = None):
        """Add a timestamped note to the experiment"""
        note_entry = {
            "note": note,
            "timestamp": timestamp or datetime.now().isoformat()
        }
        self.notes.append(note_entry)
        return note_entry
    
    def get_meal_glucose_pairs(self) -> List[Dict]:
        """
        Match meals with their corresponding glucose readings
        Returns list of meal-glucose pairs for analysis
        """
        pairs = []
        for meal in self.meals:
            meal_time = datetime.fromisoformat(meal["timestamp"])
            
            # Find glucose readings within 3 hours of meal
            related_readings = []
            for reading in self.glucose_readings:
                reading_time = datetime.fromisoformat(reading["timestamp"])
                time_diff = (reading_time - meal_time).total_seconds() / 60  # minutes
                
                if -30 <= time_diff <= 180:  # 30 min before to 3 hours after
                    related_readings.append({
                        **reading,
                        "time_from_meal_minutes": time_diff
                    })
            
            if related_readings:
                pairs.append({
                    "meal": meal,
                    "glucose_readings": sorted(
                        related_readings,
                        key=lambda x: x["time_from_meal_minutes"]
                    )
                })
        
        return pairs
    
    def save(self, filename: Optional[str] = None):
        """Save experiment data to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.participant_id}_{self.name}_{timestamp}.json"
        
        filepath = self.results_dir / filename
        
        data = {
            "experiment_name": self.name,
            "participant_id": self.participant_id,
            "created_at": self.created_at,
            "meals": self.meals,
            "glucose_readings": self.glucose_readings,
            "notes": self.notes,
            "summary": {
                "total_meals": len(self.meals),
                "total_readings": len(self.glucose_readings),
                "duration_hours": self._calculate_duration()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(filepath)
    
    def _calculate_duration(self) -> float:
        """Calculate experiment duration in hours"""
        if not self.glucose_readings and not self.meals:
            return 0
        
        all_times = []
        for reading in self.glucose_readings:
            all_times.append(datetime.fromisoformat(reading["timestamp"]))
        for meal in self.meals:
            all_times.append(datetime.fromisoformat(meal["timestamp"]))
        
        if len(all_times) < 2:
            return 0
        
        duration = max(all_times) - min(all_times)
        return duration.total_seconds() / 3600  # hours
    
    @classmethod
    def load(cls, filepath: str):
        """Load experiment from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        experiment = cls(
            name=data["experiment_name"],
            participant_id=data["participant_id"]
        )
        experiment.created_at = data["created_at"]
        experiment.meals = data["meals"]
        experiment.glucose_readings = data["glucose_readings"]
        experiment.notes = data.get("notes", [])
        
        return experiment


class ExperimentLogger:
    """
    Centralized logging system for multiple experiments
    """
    
    def __init__(self, log_file: str = "results/experiments_log.json"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
        self.experiments = self._load_log()
    
    def _load_log(self) -> List[Dict]:
        """Load existing experiment log"""
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return []
    
    def register_experiment(self, experiment: EatingExperiment, filepath: str):
        """Register a completed experiment in the log"""
        entry = {
            "experiment_name": experiment.name,
            "participant_id": experiment.participant_id,
            "created_at": experiment.created_at,
            "completed_at": datetime.now().isoformat(),
            "file_path": filepath,
            "meal_count": len(experiment.meals),
            "reading_count": len(experiment.glucose_readings)
        }
        self.experiments.append(entry)
        self._save_log()
        return entry
    
    def _save_log(self):
        """Save experiment log to file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.experiments, f, indent=2)
    
    def get_participant_experiments(self, participant_id: str) -> List[Dict]:
        """Get all experiments for a participant"""
        return [
            exp for exp in self.experiments
            if exp["participant_id"] == participant_id
        ]
    
    def get_recent_experiments(self, count: int = 10) -> List[Dict]:
        """Get most recent experiments"""
        sorted_experiments = sorted(
            self.experiments,
            key=lambda x: x["completed_at"],
            reverse=True
        )
        return sorted_experiments[:count]


if __name__ == "__main__":
    # Example usage
    print("CGM Eating Tracker Example")
    print("-" * 50)
    
    # Create a new experiment
    experiment = EatingExperiment(
        name="Breakfast_Oatmeal_Test",
        participant_id="user_001"
    )
    
    # Log a meal
    experiment.log_meal(
        meal_type="breakfast",
        foods=["oatmeal", "banana", "almonds"],
        carbs=45,
        protein=8,
        fat=10,
        notes="Feeling energetic this morning"
    )
    
    # Log glucose readings
    experiment.log_glucose(115, context="pre-meal")
    experiment.log_glucose(145, context="30-min post-meal")
    experiment.log_glucose(165, context="1-hour post-meal")
    experiment.log_glucose(140, context="2-hour post-meal")
    
    # Add notes
    experiment.add_note("Peak occurred at 1 hour, felt good throughout")
    
    # Get meal-glucose pairs
    pairs = experiment.get_meal_glucose_pairs()
    print(f"\nFound {len(pairs)} meal-glucose pairs")
    
    # Save experiment
    saved_path = experiment.save()
    print(f"\nExperiment saved to: {saved_path}")
    
    # Log in central registry
    logger = ExperimentLogger()
    logger.register_experiment(experiment, saved_path)
    print("\nExperiment registered in central log")
