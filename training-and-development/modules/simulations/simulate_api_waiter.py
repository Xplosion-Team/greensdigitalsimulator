"""
Simulate the "Waiter" API Analogy.
Demonstrates the Request/Response cycle between a Frontend guest 
and a Backend kitchen via the API waiter.
"""
import time
import json

def api_waiter_call(request_payload):
    print(f"\n[CLIENT] Guest orders: {request_payload['user_message']}")
    print("[API] Waiter takes the order to the kitchen...")
    time.sleep(1)
    
    # Simulate Backend Logic (The Kitchen)
    glucose = request_payload['current_state']['glucose']
    if "prediction" in request_payload['user_message'].lower():
        prediction = glucose + random.randint(-5, 5)
        response = {
            "response": f"The kitchen predicts your glucose will be around {prediction} mg/dL soon.",
            "urgency": "low"
        }
    else:
        response = {
            "response": "The kitchen says 'Hello! Your current state is received.'",
            "urgency": "info"
        }
    
    print("[BACKEND] Kitchen finishes cooking the data.")
    print(f"[API] Waiter brings the response back: {json.dumps(response, indent=2)}")
    return response

if __name__ == "__main__":
    import random
    mock_request = {
        "user_message": "What is my glucose prediction?",
        "current_state": {"glucose": 115, "trend": "Stable"}
    }
    api_waiter_call(mock_request)
