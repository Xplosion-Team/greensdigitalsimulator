import os
from typing import Any, Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from t1dsim_ai.brains.orchestrator import BrainOrchestrator


app = FastAPI(title="Greens Digital Twin Brain API", version="0.1.0")


class BrainQueryRequest(BaseModel):
    text: str = Field(..., description="User message")
    current_glucose: float = Field(..., description="Current glucose mg/dL")
    digital_twin_id: int = Field(1, description="Digital twin ID (0-4)")
    provider: Optional[str] = Field(None, description="Override BRAIN_PROVIDER for this request")


@app.get("/")
def read_root() -> Dict[str, Any]:
    return {"message": "Greens Digital Twin Brain API is running", "status": "ok"}


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True}


@app.post("/v1/brain/query")
def brain_query(req: BrainQueryRequest) -> Dict[str, Any]:
    # Provider defaults to env (BRAIN_PROVIDER) unless overridden.
    provider = req.provider or os.getenv("BRAIN_PROVIDER", "fallback")

    brain = BrainOrchestrator(
        provider=provider,
        digital_twin_id=req.digital_twin_id,
        # OpenAI key/model and Ollama base/models are read from env inside providers.
    )

    result = brain.query(user_query=req.text, current_glucose=req.current_glucose)
    return result
