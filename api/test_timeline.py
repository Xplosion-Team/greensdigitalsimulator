from fastapi.testclient import TestClient
import sys
import os

# Add the root directory to sys.path to find api and t1dsim_ai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.main import app

client = TestClient(app)

def test_predict_timeline():
    test_cases = [
        {"name": "Valid Case", "payload": {"current_glucose": 115.0, "carbs": 75.0, "meal_time_offset": 30, "digital_twin_id": 1}},
        {"name": "High Glucose Case (>400)", "payload": {"current_glucose": 450.0, "carbs": 75.0, "meal_time_offset": 30, "digital_twin_id": 1}},
        {"name": "Large Offset Case (>120)", "payload": {"current_glucose": 115.0, "carbs": 75.0, "meal_time_offset": 150, "digital_twin_id": 1}},
    ]
    
    for case in test_cases:
        print(f"\nScenario: {case['name']}")
        response = client.post("/v1/predict/timeline", json=case['payload'])
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("SUCCESS: Timeline generated.")
            else:
                print(f"FAILURE: API returned success=False. Error: {data.get('error')}")
        else:
            print(f"FAILURE: Status code {response.status_code}")

if __name__ == "__main__":
    test_predict_timeline()
