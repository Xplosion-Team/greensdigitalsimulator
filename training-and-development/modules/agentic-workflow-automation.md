# 🤖 Module: Agentic Workflows (The Guardian)

## Goal
Transform the Digital Twin from a passive display into an active "Guardian" that can take actions based on data.

## What are Agentic Workflows?
An agentic workflow uses AI to decide *which* tool to use and *when* to use it.
- **Data**: Glucose is 240 mg/dL and rising.
- **Decision**: This is an emergency.
- **Action**: Use the "Email Tool" to alert the primary contact.

## The "Guardian" System
The Guardian is a specialized AI agent with access to:
1. **The Clock**: To know when alerts were last sent.
2. **The SMS Tool**: To send urgent notifications.
3. **The Calendar Tool**: To suggest booking a doctor's appointment.

## Prompting for Agency
To build this, we use **System Prompts** that define the AI's personality and rules:
> "You are the Digital Twin Guardian. Your primary rule is safety. If glucose exceeds 200 mg/dL for more than 2 hours, you must use the `notify_caregiver` tool."

## Graduation Project
Build the **"Mom, I'm High" SMS alert system**.
1. Input: Simulated glucose spike.
2. Processing: Agent evaluates the risk.
3. Output: An automated SMS sent via Twilio or Email bridge.

## Run Simulation 🧪
Watch the Guardian protect the curve:
`python simulations/simulate_agent_guardian.py`

---
*Back to [Training Plan](../MIRNA_TRAINING_PLAN.md)*
