import pickle
import sys
import os
from pathlib import Path

# Try to find a pkl file
pkl_path = r"c:\Users\mirna\OneDrive\Desktop\KEEEEEEEP\DigitalTwin\code\greensdigitalsimulator\t1dsim_ai\models\IndividualModel\T1DEXI-01-1047\scaler_robust.pkl"
if os.path.exists(pkl_path):
    print(f"Attempting to load {pkl_path}...")
    try:
        with open(pkl_path, "rb") as f:
            data = pickle.load(f)
            print("Successfully loaded!")
            print(type(data))
    except Exception:
        import traceback
        traceback.print_exc()
else:
    print(f"File not found: {pkl_path}")
