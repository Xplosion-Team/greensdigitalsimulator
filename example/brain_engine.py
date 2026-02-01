import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from t1dsim_ai.individual_model import DigitalTwin
from t1dsim_ai.create_scenarios import digitalTwin_scenario
from dexcom_connector import DexcomConnector
from brain_llm import BrainLLM

class BrainEngine:
    """
    The Intelligence Layer ("The Brain") that connects natural language
    with the Digital Twin physics engine.
    """
    def __init__(self, digital_twin_id=4):
        self.digital_twin_id = digital_twin_id
        self.dt = DigitalTwin(n_digitalTwin=digital_twin_id)
        self.dexcom = DexcomConnector()
        self.llm = BrainLLM(provider="mock") # Use mock for prototype
        
    def process_query(self, query):
        """
        Main entry point for user queries.
        1. Fetch latest real-time state
        2. Parse intent and parameters
        3. Run simulation
        4. Explain results
        """
        # 1. Get current state from "Dexcom"
        current_data = self.dexcom.get_latest_glucose()
        start_glucose = current_data["value"]

        # 2. Parse intent
        params = self.llm.parse_intent(query)
        
        if not params:
            return f"Currently, your glucose is {start_glucose} mg/dL and {current_data['trend']}. I couldn't understand that question, but you can ask about food or activities!"
        
        # 3. Run Simulation with starting state
        results = self._run_simulation(params, start_glucose)
        
        # 4. Generate Explanation
        context = {
            "start_glucose": start_glucose,
            "max_glucose": results.cgm_NNDT.max(),
            "final_glucose": results.cgm_NNDT.iloc[-1],
            "carbs": params.get("carbs", 0),
            "type": params.get("type")
        }
        explanation = self.llm.generate_explanation(context)
        
        return explanation

    def _run_simulation(self, params, start_glucose):
        """
        Runs the Digital Twin simulation based on extracted parameters and starting glucose.
        """
        if params["type"] == "meal":
            scenario = digitalTwin_scenario(
                init_cgm=start_glucose,
                meal_size_array=[params["carbs"]],
                meal_time_fromStart_array=[params["time_offset"]],
                sim_time=4 * 60 # 4 hours
            )
            return self.dt.simulate(scenario)
        return None

if __name__ == "__main__":
    brain = BrainEngine()
    print("-------------------------------------------")
    print("Welcome to the Greens Health Brain Prototype!")
    print("-------------------------------------------")
    print("This prototype connects real-time (mocked) Dexcom data")
    print("with the Digital Twin physics engine and an LLM interpreter.")
    print("\nExample queries:")
    print("- 'What happens if I eat 60g of carbs?'")
    print("- 'I want to eat a slice of cake (50g carbs)'")
    
    while True:
        try:
            print("\n" + "="*40)
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Brain: Goodbye! Stay healthy.")
                break
            
            if not user_input.strip():
                continue
                
            response = brain.process_query(user_input)
            print(f"\nBrain: {response}")
        except KeyboardInterrupt:
            print("\nBrain: Goodbye!")
            break
        except Exception as e:
            print(f"\nBrain: I ran into a bit of trouble: {e}")
