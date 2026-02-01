import re
from typing import Optional, Dict, Any
from .base import BrainProvider

class MockBrainProvider(BrainProvider):
    """
    Rule-based provider for testing logic without external API calls.
    """
    def parse_intent(self, query: str) -> Optional[Dict[str, Any]]:
        query = query.lower()
        carbs_match = re.search(r'(\d+)\s*g', query)
        if not carbs_match:
            carbs_match = re.search(r'(\d+)\s*(grams|carbs)', query)
            
        if "eat" in query or carbs_match:
            carbs = int(carbs_match.group(1)) if carbs_match else 40
            return {
                "type": "meal",
                "carbs": carbs,
                "time_offset": 30
            }
        return None

    def generate_explanation(self, context: Dict[str, Any]) -> str:
        rise = context['max_glucose'] - context['start_glucose']
        if context['max_glucose'] > 200:
            status = "a bit high"
        elif context['max_glucose'] > 180:
            status = "slightly elevated"
        else:
            status = "well within your safe range"
            
        return (f"If you eat {context.get('carbs', 0)}g of carbs, your glucose "
                f"is predicted to rise by {rise:.0f} points, peaking at {context['max_glucose']:.0f}. "
                f"This is {status}. Keep it up!")

class OpenAIProvider(BrainProvider):
    """
    Provider using OpenAI's API. Note: Should only receive sanitized summaries.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        # Lazy import to avoid dependency issues if not used
        self.client = None

    def _ensure_client(self):
        if not self.client and self.api_key:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)

    def parse_intent(self, query: str) -> Optional[Dict[str, Any]]:
        # Plan: In Phase 4, implement structured JSON output parsing here.
        # Fallback to mock for now
        return MockBrainProvider().parse_intent(query)

    def generate_explanation(self, context: Dict[str, Any]) -> str:
        # Plan: In Phase 4, implement warm senior-friendly prompting.
        return MockBrainProvider().generate_explanation(context)
