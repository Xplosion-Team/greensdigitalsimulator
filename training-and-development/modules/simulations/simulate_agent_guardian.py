"""
Simulate an Agentic Guardian workflow.
Demonstrates how an AI agent uses data to make decisions 
and trigger external tools (like alerts).
"""
import time

class DigitalTwinGuardian:
    def __init__(self, threshold=200):
        self.threshold = threshold
        self.alert_sent = False

    def evaluate_risk(self, glucose_value):
        print(f"\n[AGENT] Evaluating current glucose: {glucose_value} mg/dL")
        
        if glucose_value > self.threshold:
            print(f"🚨 [DECISION] Emergency! Glucose is above {self.threshold}.")
            self.trigger_tool("SMS_Alert", "Mom, my glucose is dangerous!")
        elif glucose_value > 150:
            print("⚠️ [DECISION] High. Suggesting a walk.")
            self.trigger_tool("Recommendation", "Consider a 10-minute walk.")
        else:
            print("✅ [DECISION] All clear. Keep it up!")

    def trigger_tool(self, tool_name, message):
        print(f"[TOOL] Executing {tool_name}...")
        time.sleep(1)
        print(f"[TOOL OUTPUT] Sent: \"{message}\"")

if __name__ == "__main__":
    guardian = DigitalTwinGuardian()
    
    # Test Scenario 1: Stable
    guardian.evaluate_risk(110)
    
    # Test Scenario 2: Emergency
    guardian.evaluate_risk(245)
