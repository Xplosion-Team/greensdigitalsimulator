"""
Simulate a Server Handshake and CORS check.
Demonstrates how the frontend verifies the backend 'pulse' and security settings.
"""
import time

def simulate_handshake(frontend_origin):
    allowed_origins = ["https://lovable.dev", "http://localhost:3000"]
    
    print(f"\nChecking handshake from: {frontend_origin}")
    time.sleep(0.5)
    
    if frontend_origin in allowed_origins:
        print("[PASS] [CORS] Permission Granted.")
        print("[INFO] [PULSE] Backend is alive and talking to frontend.")
    else:
        print("[FAIL] [CORS] Permission Denied: Origin not recognized.")
        print("[WARN] [DEBUG] Please add this URL to your FastAPI origins list.")

if __name__ == "__main__":
    simulate_handshake("https://lovable.dev")
    simulate_handshake("https://malicious-site.com")
