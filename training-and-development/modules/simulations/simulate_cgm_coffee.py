"""
Simulate the "Coffee Experiment" for CGM Baseline Training.
This script demonstrates how different inputs (Black Coffee vs Coffee with Sugar) 
affect glucose levels over time.
"""
import time
import random

def simulate_coffee_spike(with_sugar=False):
    print(f"\n--- Starting Coffee Experiment (Sugar: {with_sugar}) ---")
    glucose = 180  # Baseline mg/dL
    trend = "Stable"
    
    for minute in range(0, 120, 10):
        # Simulate physiological response
        if with_sugar:
            # Sugar causes a faster, higher spike
            spike = random.uniform(5, 15) if minute < 60 else random.uniform(-10, -5)
        else:
            # Black coffee might cause a small elevation for some or stay stable
            spike = random.uniform(0, 3) if minute < 40 else random.uniform(-2, 0)
        
        glucose += spike
        
        # Determine trend
        if spike > 2: trend = "Rising Fast"
        elif spike > 0.5: trend = "Rising"
        elif spike < -2: trend = "Falling Fast"
        elif spike < -0.5: trend = "Falling"
        else: trend = "Stable"
        
        print(f"Time: {minute:3} min | Glucose: {glucose:6.1f} mg/dL | Trend: {trend}")
        time.sleep(0.1)  # Artificial delay for effect

if __name__ == "__main__":
    simulate_coffee_spike(with_sugar=False)
    simulate_coffee_spike(with_sugar=True)
    print("\nExperiment Complete. Observe how sugar intensity changes the curve velocity.")
