# 🔌 Module: Server Integration (Brains)

## Goal
Connect your Lovable frontend to your Replit/Backend environment and ensure secure, real-time communication.

## The Connection Bridge
To make the frontend and backend talk, we need two things:
1. **The URL**: The public address of your server (e.g., `https://my-engine.replit.app`).
2. **CORS (Cross-Origin Resource Sharing)**: A security feature that allows your frontend domain to request data from your backend domain.

## Execution Checklist
1. **Initialize Replit**: Spin up a FastAPI server using the "Greens Engine" template.
2. **Setup Environment**: Add your API keys (OpenAI, Anthropic) to the Secret keys in Replit.
3. **Frontend Config**: In your Lovable project, update the `API_URL` constant.
4. **Test the Handshake**: Send a "Hello" pulse from the frontend and verify the backend receives it.

- **CORS Error**: Ensure the frontend URL is listed in the `origins` list of the FastAPI middle-ware.

## The Brain Query Endpoint
To get insights from your digital twin, send a POST request to `/v1/brain/query`.

**Sample Request (Linux/Mac/Bash):**
```bash
curl -X POST https://greensdigitalsimulator-production.up.railway.app/v1/brain/query \
-H "Content-Type: application/json" \
-d '{
  "text": "What happens if I eat 60g of carbs?",
  "current_glucose": 110.0,
  "digital_twin_id": 1
}'
```

**Sample Request (Windows PowerShell):**
On Windows, PowerShell uses an alias for `curl`. Use `curl.exe` to ensure you are using the real version, and use double quotes for the data payload:
```powershell
curl.exe -X POST https://greensdigitalsimulator-production.up.railway.app/v1/brain/query -H "Content-Type: application/json" -d "{\"text\": \"What happens if I eat 60g of carbs?\", \"current_glucose\": 110.0, \"digital_twin_id\": 1}"
```

**Key Parameters:**
- `text`: Your question or meal description.
- `current_glucose`: Your latest CGM reading.
- `digital_twin_id`: The ID of your twin profile.

## Run Simulation 🧪
Test the handshake locally:
`python simulations/simulate_server_handshake.py`

Test a real Brain Query:
`python simulations/simulate_brain_query.py`

---
*Back to [Training Plan](../MIRNA_TRAINING_PLAN.md)*
