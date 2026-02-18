import os
from typing import Any, Dict, Optional

from fastapi import FastAPI, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from twilio.twiml.messaging_response import MessagingResponse

from t1dsim_ai.brains.orchestrator import BrainOrchestrator


app = FastAPI(title="Greens Digital Twin Brain API", version="0.1.0")

# Enable CORS for frontend development
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/v1/brain/sms")
async def sms_reply(Body: str = Form(...), From: str = Form(...)):
    """Twilio SMS Webhook. Receives text, queries Brain, replies via SMS."""
    # 1. Initialize Brain
    # Note: Currently uses a hardcoded digital_twin_id=1 (Phase 7 prototype).
    # In Phase 3 (Data Integration), we will fetch 'From' user's real-time glucose.
    brain = BrainOrchestrator(
        provider="fallback",
        digital_twin_id=1,
    )

    # 2. Query the Brain
    # Defaulting to 115.0 mg/dL for now.
    result = brain.query(user_query=Body, current_glucose=115.0)

    # 3. Build TwiML Response
    twiml = MessagingResponse()
    if result["success"]:
        twiml.message(result["explanation"])
    else:
        twiml.message(result["message"])

    return Response(content=str(twiml), media_type="application/xml")
