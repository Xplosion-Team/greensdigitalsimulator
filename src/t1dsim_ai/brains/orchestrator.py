import os
from typing import Optional, Dict, Any

from ..individual_model import DigitalTwin
from ..create_scenarios import digitalTwin_scenario
from .providers import (
    MockBrainProvider,
    OpenAIProvider,
    OllamaProvider,
    FallbackBrainProvider,
    build_provider_chain,
)
from .sanitizer import BrainSanitizer


class BrainOrchestrator:
    """Main orchestrator for the Intelligence Layer.

    Bridges User -> Provider (LLM or local logic) -> Simulation -> Explanation.

    Providers:
      - mock
      - openai
      - ollama
      - fallback (OpenAI → Ollama(phi3) → Ollama(qwen) → Mock)
    """

    def __init__(
        self,
        provider: str = "fallback",
        api_key: Optional[str] = None,
        digital_twin_id: int = 1,
        ollama_base: Optional[str] = None,
        ollama_model: Optional[str] = None,
    ):
        self.digital_twin_id = digital_twin_id
        self.dt = DigitalTwin(n_digitalTwin=digital_twin_id)

        provider = (provider or os.getenv("BRAIN_PROVIDER", "fallback")).lower()

        if provider == "openai":
            self.provider = OpenAIProvider(api_key=api_key)
        elif provider == "ollama":
            self.provider = OllamaProvider(model=ollama_model or "phi3:latest", base_url=ollama_base)
        elif provider == "fallback":
            # Use OpenAI first, then Ollama models, then mock.
            # You can override Ollama model list via BRAIN_OLLAMA_MODELS="phi3:latest,qwen2.5-coder:7b"
            models_env = os.getenv("BRAIN_OLLAMA_MODELS")
            models = [m.strip() for m in models_env.split(",")] if models_env else None
            self.provider = build_provider_chain(openai_first=True, ollama_models=models)
        else:
            self.provider = MockBrainProvider()

    def query(self, user_query: str, current_glucose: float) -> Dict[str, Any]:
        """Executes the full intelligence loop."""
        # 1) Parse intent (local/deterministic)
        params = self.provider.parse_intent(user_query)
        if not params:
            return {
                "success": False,
                "error": "intent_not_found",
                "message": "I'm sorry, I couldn't understand that. Try: 'What if I eat 50g of carbs?'",
            }

        # 2) Run simulation
        try:
            scenario = digitalTwin_scenario(
                init_cgm=current_glucose,
                meal_size_array=[params.get("carbs", 0)],
                meal_time_fromStart_array=[params.get("time_offset", 30)],
                sim_time=4 * 60,
            )
            results = self.dt.simulate(scenario)
        except Exception as e:
            return {"success": False, "error": "simulation_failed", "message": f"Simulation hitch: {e}"}

        # 3) Sanitize (privacy)
        sanitized_summary = BrainSanitizer.summarize_simulation(results, params, current_glucose)

        # 4) Explain (provider chain)
        explanation = self.provider.generate_explanation(sanitized_summary)

        return {"success": True, "explanation": explanation, "summary_stats": sanitized_summary}
