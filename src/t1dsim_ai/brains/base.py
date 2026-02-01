from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BrainProvider(ABC):
    """
    Abstract base class for Intelligence Layer providers (e.g. OpenAI, Local Llama).
    """
    
    @abstractmethod
    def parse_intent(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Translates natural language into structured simulation parameters.
        Example return: {"type": "meal", "carbs": 50, "time_offset": 60}
        """
        pass

    @abstractmethod
    def generate_explanation(self, context: Dict[str, Any]) -> str:
        """
        Generates a human-readable explanation from sanitized simulation summary stats.
        """
        pass
