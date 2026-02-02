import json
import os
import re
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List, Tuple

from .base import BrainProvider


class MockBrainProvider(BrainProvider):
    """Rule-based provider for testing logic without external API calls."""

    def parse_intent(self, query: str) -> Optional[Dict[str, Any]]:
        query = query.lower()
        # Look for carb amounts (e.g., "50g", "40 grams")
        carbs_match = re.search(r"(\d+)\s*g", query)
        if not carbs_match:
            carbs_match = re.search(r"(\d+)\s*(grams|carbs)", query)

        # Meal Intent: Look for "eat", "ate", "eating", "snack", "meal", "pizza", etc.
        meal_keywords = ["eat", "ate", "eating", "snack", "meal", "pizza", "carbs", "food"]
        if any(kw in query for kw in meal_keywords) or carbs_match:
            carbs = int(carbs_match.group(1)) if carbs_match else 45
            return {"type": "meal", "carbs": carbs, "time_offset": 30}

        # Exercise Intent: Look for "walk", "exercise", "run", "gym", "workout"
        exercise_keywords = ["walk", "exercise", "run", "gym", "workout", "active"]
        if any(kw in query for kw in exercise_keywords):
            return {"type": "exercise", "intensity": "moderate", "duration": 30}

        return None

    def generate_explanation(self, context: Dict[str, Any]) -> str:
        rise = context["max_glucose"] - context["start_glucose"]
        if context["max_glucose"] > 200:
            status = "a bit high"
        elif context["max_glucose"] > 180:
            status = "slightly elevated"
        else:
            status = "well within your safe range"

        return (
            f"If you eat {context.get('carbs', 0)}g of carbs, your glucose "
            f"is predicted to rise by {rise:.0f} points, peaking at {context['max_glucose']:.0f}. "
            f"This is {status}."
        )


class OpenAIProvider(BrainProvider):
    """OpenAI provider (safe: only sanitized summaries should be passed in)."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        # NOTE: this repo currently pins openai>=0.27.0 in optional deps, so we use
        # the legacy openai.ChatCompletion.create API for compatibility.
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("BRAIN_OPENAI_MODEL", "gpt-4o-mini")

    def parse_intent(self, query: str) -> Optional[Dict[str, Any]]:
        # Keep parsing local & deterministic for now.
        return MockBrainProvider().parse_intent(query)

    def generate_explanation(self, context: Dict[str, Any]) -> str:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

        import openai

        openai.api_key = self.api_key
        openai.api_base = "https://api.openai.com/v1"

        prompt = (
            "You are Greens Health's assistant. Write a short, calm, senior-friendly explanation. "
            "Avoid medical diagnosis. Do not mention HIPAA. Use simple words.\n\n"
            f"Sanitized simulation summary (no PHI): {json.dumps(context)}\n\n"
            "Reply in 2-4 sentences."
        )

        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful diabetes education assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )
        return resp["choices"][0]["message"]["content"].strip()


class GroqProvider(BrainProvider):
    """Groq provider (OpenAI-compatible)."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("groq") or os.getenv("GROQ")
        self.model = model or os.getenv("BRAIN_GROQ_MODEL", "llama-3.3-70b-versatile")

    def parse_intent(self, query: str) -> Optional[Dict[str, Any]]:
        return MockBrainProvider().parse_intent(query)

    def generate_explanation(self, context: Dict[str, Any]) -> str:
        if not self.api_key:
            raise RuntimeError("GROQ environment variable not set")

        import openai

        openai.api_key = self.api_key
        openai.api_base = "https://api.groq.com/openai/v1"

        prompt = (
            "You are Greens Health's assistant. Write a short, calm, senior-friendly explanation. "
            "Avoid medical diagnosis. Use simple words.\n\n"
            f"Sanitized simulation summary: {json.dumps(context)}\n\n"
            "Reply in 2-4 sentences."
        )

        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful diabetes education assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )
        return resp["choices"][0]["message"]["content"].strip()


class OllamaProvider(BrainProvider):
    """Local Ollama provider via its HTTP API (no API key required).

    Uses /api/generate to avoid extra client deps.
    """

    def __init__(self, model: str = "phi3:latest", base_url: Optional[str] = None):
        self.model = model
        self.base_url = base_url or os.getenv("OLLAMA_API_BASE", "http://127.0.0.1:11434")

    def parse_intent(self, query: str) -> Optional[Dict[str, Any]]:
        # Keep parsing local & deterministic for now.
        return MockBrainProvider().parse_intent(query)

    def generate_explanation(self, context: Dict[str, Any]) -> str:
        url = f"{self.base_url}/api/generate"
        prompt = (
            "Write a short, calm, senior-friendly explanation of the simulation summary. "
            "Avoid clinical jargon and do not diagnose.\n\n"
            f"Summary: {json.dumps(context)}\n\n"
            "Reply in 2-4 sentences."
        )

        payload = {"model": self.model, "prompt": prompt, "stream": False}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read().decode("utf-8")
                out = json.loads(body)
                return (out.get("response") or "").strip() or MockBrainProvider().generate_explanation(context)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            raise RuntimeError(f"ollama_request_failed: {e}")


class FallbackBrainProvider(BrainProvider):
    """Tries a list of providers in order until one succeeds.

    This is how we survive token exhaustion / outages.
    """

    def __init__(self, providers: List[Tuple[str, BrainProvider]]):
        self.providers = providers

    def parse_intent(self, query: str) -> Optional[Dict[str, Any]]:
        # Intent parsing should be local; just call the first provider.
        # (All providers currently delegate to mock anyway.)
        name, p = self.providers[0]
        return p.parse_intent(query)

    def generate_explanation(self, context: Dict[str, Any]) -> str:
        last_err: Optional[Exception] = None
        for name, p in self.providers:
            try:
                return p.generate_explanation(context)
            except Exception as e:
                last_err = e
                continue
        # Absolute last-resort: mock message.
        if last_err:
            return MockBrainProvider().generate_explanation(context)
        return MockBrainProvider().generate_explanation(context)


def build_provider_chain(
    *,
    openai_first: bool = True,
    groq_enabled: bool = True,
    ollama_models: Optional[List[str]] = None,
) -> FallbackBrainProvider:
    """Default chain: OpenAI → Groq → Ollama → Mock."""

    ollama_models = ollama_models or ["phi3:latest", "qwen2.5-coder:7b"]
    chain: List[Tuple[str, BrainProvider]] = []

    if openai_first:
        chain.append(("openai", OpenAIProvider()))

    if groq_enabled:
        chain.append(("groq", GroqProvider()))

    for m in ollama_models:
        chain.append((f"ollama:{m}", OllamaProvider(model=m)))

    chain.append(("mock", MockBrainProvider()))

    return FallbackBrainProvider(chain)
