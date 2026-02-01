from typing import Optional, Dict, Any
from ..individual_model import DigitalTwin
from ..create_scenarios import digitalTwin_scenario
from .base import BrainProvider
from .providers import MockBrainProvider, OpenAIProvider
from .sanitizer import BrainSanitizer

class BrainOrchestrator:
    """
    Main orchestrator for the Intelligence Layer.
    Bridges User -> LLM -> Simulation -> Explanation.
    """
    def __init__(self, provider: str = "mock", api_key: Optional[str] = None, digital_twin_id: int = 1):
        self.digital_twin_id = digital_twin_id
        self.dt = DigitalTwin(n_digitalTwin=digital_twin_id)
        
        if provider == "openai":
            self.provider = OpenAIProvider(api_key=api_key)
        else:
            self.provider = MockBrainProvider()

    def query(self, user_query: str, current_glucose: float) -> Dict[str, Any]:
        """
        Executes the full intelligence loop.
        """
        # 1. Parse Intent
        params = self.provider.parse_intent(user_query)
        if not params:
            return {
                "success": False,
                "error": "intent_not_found",
                "message": f"I'm sorry, I couldn't understand that. You can ask about food like 'What if I eat 50g of carbs?'"
            }
            
        # 2. Run Physical Simulation
        try:
            scenario = digitalTwin_scenario(
                init_cgm=current_glucose,
                meal_size_array=[params.get("carbs", 0)],
                meal_time_fromStart_array=[params.get("time_offset", 30)],
                sim_time=4 * 60
            )
            results = self.dt.simulate(scenario)
        except Exception as e:
            return {"success": False, "error": "simulation_failed", "message": f"Simulation hitch: {e}"}

        # 3. Sanitize Data (Privacy Protection)
        sanitized_summary = BrainSanitizer.summarize_simulation(results, params, current_glucose)
        
        # 4. Generate Explanation (LLM)
        explanation = self.provider.generate_explanation(sanitized_summary)
        
        return {
            "success": True,
            "explanation": explanation,
            "summary_stats": sanitized_summary
        }
