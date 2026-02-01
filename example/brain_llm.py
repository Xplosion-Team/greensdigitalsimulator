import os
import json

class BrainLLM:
    """
    Interface for LLM-based intelligence.
    Can be configured to use OpenAI API or a mock for local testing.
    """
    def __init__(self, provider="mock", api_key=None):
        self.provider = provider
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
    def parse_intent(self, query):
        """
        Parses user intent and extracts parameters.
        """
        if self.provider == "mock":
            return self._mock_parse_intent(query)
        elif self.provider == "openai":
            return self._openai_parse_intent(query)
        return None

    def generate_explanation(self, context):
        """
        Generates a warm, senior-friendly explanation of simulation results.
        """
        if self.provider == "mock":
            return self._mock_generate_explanation(context)
        elif self.provider == "openai":
            return self._openai_generate_explanation(context)
        return None

    def _mock_parse_intent(self, query):
        import re
        query = query.lower()
        
        # Simple rule-based extraction for the mock
        carbs_match = re.search(r'(\d+)\s*g', query)
        if not carbs_match:
            carbs_match = re.search(r'(\d+)\s*(grams|carbs)', query)
            
        if "eat" in query or carbs_match:
            carbs = int(carbs_match.group(1)) if carbs_match else 40
            return {
                "type": "meal",
                "carbs": carbs,
                "time_offset": 30 # minutes from now
            }
        return None

    def _mock_generate_explanation(self, context):
        # context contains: start_glucose, max_glucose, final_glucose, carbs
        rise = context['max_glucose'] - context['start_glucose']
        
        if context['max_glucose'] > 200:
            tone = "a bit high. You might want to keep an eye on it or talk to your doctor about your insulin."
        elif context['max_glucose'] > 180:
            tone = "slightly above your target. A short walk might help keep things steady."
        else:
            tone = "well within your safe range. Great choice!"
            
        return (f"If you eat {context['carbs']}g of carbs, your glucose (currently {context['start_glucose']:.0f}) "
                f"is predicted to peak at {context['max_glucose']:.0f}. That's {rise:.0f} points higher, which is {tone}")

    def _openai_parse_intent(self, query):
        # Placeholder for actual OpenAI call
        return self._mock_parse_intent(query)

    def _openai_generate_explanation(self, context):
        # Placeholder for actual OpenAI call
        return self._mock_generate_explanation(context)

if __name__ == "__main__":
    llm = BrainLLM()
    print("Test intent parsing: 'I want to eat 50g of carbs'")
    print(llm.parse_intent("I want to eat 50g of carbs"))
    
    print("\nTest explanation generation:")
    print(llm.generate_explanation({
        "start_glucose": 110,
        "max_glucose": 185,
        "carbs": 50
    }))
