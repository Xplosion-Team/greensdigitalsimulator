import os
from typing import Any, Dict, Optional

from fastapi import FastAPI, Form, Response
from pydantic import BaseModel, Field
from twilio.twiml.messaging_response import MessagingResponse

from t1dsim_ai.brains.orchestrator import BrainOrchestrator
from t1dsim_ai.individual_model import DigitalTwin
from t1dsim_ai.create_scenarios import digitalTwin_scenario


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Greens Digital Twin Brain API", version="0.1.0")

# Enable CORS for external frontends (e.g., Lovable)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BrainQueryRequest(BaseModel):
    text: str = Field(..., description="User message")
    current_glucose: float = Field(..., description="Current glucose mg/dL")
    digital_twin_id: int = Field(1, description="Digital twin ID (0-4)")
    provider: Optional[str] = Field(None, description="Override BRAIN_PROVIDER for this request")


class TimelineRequest(BaseModel):
    current_glucose: float = Field(..., description="Current glucose mg/dL")
    carbs: float = Field(50, description="Carbohydrates in grams")
    meal_time_offset: int = Field(30, description="Minutes from sim start until meal")
    digital_twin_id: int = Field(1, description="Digital twin ID (0-4)")


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


@app.post("/v1/predict/timeline")
def predict_timeline(req: TimelineRequest) -> Dict[str, Any]:
    """Return predicted CGM readings every 5 minutes for 2 hours post-meal."""
    try:
        # 1. Build the scenario (2-hour window)
        scenario = digitalTwin_scenario(
            init_cgm=req.current_glucose,
            meal_size_array=[req.carbs],
            meal_time_fromStart_array=[req.meal_time_offset],
            sim_time=2 * 60,  # 120 minutes
        )

        # 2. Run the digital twin simulation
        dt = DigitalTwin(n_digitalTwin=req.digital_twin_id)
        results = dt.simulate(scenario)

        # 3. Build the timeline (every 5-min datapoint)
        timeline = []
        for i, row in results.iterrows():
            timeline.append({
                "minute": int(i * 5),
                "glucose": round(float(row["cgm_NNDT"]), 1),
            })

        # 4. Summary stats
        peak_idx = results["cgm_NNDT"].idxmax()
        summary = {
            "start_glucose": req.current_glucose,
            "peak_glucose": round(float(results["cgm_NNDT"].max()), 1),
            "peak_at_minute": int(peak_idx * 5),
            "final_glucose": round(float(results["cgm_NNDT"].iloc[-1]), 1),
            "carbs": req.carbs,
            "total_points": len(timeline),
        }

        return {"success": True, "timeline": timeline, "summary": summary}

    except Exception as e:
        return {"success": False, "error": str(e)}

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
