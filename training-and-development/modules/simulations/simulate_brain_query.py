"""
Simulate a real Brain Query call.
Shows how the "Text" query is processed and returned with Digital Twin insights.
"""
import requests
import json
import os

# Configuration
API_URL = "https://greensdigitalsimulator-production.up.railway.app/v1/brain/query"

def simulate_real_query(text_query, glucose=110.0, twin_id=1):
    print(f"\n--- [BRAIN QUERY SIMULATION] ---")
    print(f"Sending Query: '{text_query}'")
    
    payload = {
        "text": text_query,
        "current_glucose": glucose,
        "digital_twin_id": twin_id
    }
    
    try:
        print(f"Contacting Brain at {API_URL}...")
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("\n[SUCCESS] Response Received:")
            print(f"Explanation: {data.get('explanation')[:200]}...") # Truncated for display
            print("\nStats:")
            print(json.dumps(data.get('summary_stats'), indent=2))
        else:
            print(f"[ERROR] Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"[WARN] Connection Failed: {str(e)}")
        print("Falling back to local mock...")
        # Mock fallback
        mock_response = {
            "success": True,
            "explanation": "Mock: 60g of carbs will likely cause a significant rise in glucose.",
            "summary_stats": {"glucose_rise": 45, "carbs": 60}
        }
        print(json.dumps(mock_response, indent=2))

if __name__ == "__main__":
    simulate_real_query("What happens if I eat 60g of carbs?")
