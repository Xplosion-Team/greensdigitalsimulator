from brain_engine import BrainEngine
import sys

def test_brain():
    print("Testing Brain Engine Integration...")
    brain = BrainEngine()
    
    test_queries = [
        "What happens if I eat 50g of carbs?",
        "I want to have a 75g carb meal",
        "How is my glucose doing?"
    ]
    
    for query in test_queries:
        print(f"\nQUERY: {query}")
        try:
            response = brain.process_query(query)
            print(f"RESPONSE: {response}")
            if "Currently" in response or "predicted" in response:
                print("SUCCESS: Response generated correctly.")
            else:
                print("FAILURE: Response format unexpected.")
        except Exception as e:
            print(f"ERROR during test: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    test_brain()
