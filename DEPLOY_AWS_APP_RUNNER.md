# Deploy to AWS App Runner (Brains API)

This repo includes a small FastAPI service that wraps the digital twin + brains layer.

## What gets deployed
- FastAPI app: `api/main.py`
- Dockerfile at repo root
- Endpoint:
  - `GET /health`
  - `POST /v1/brain/query`

## App Runner setup (container)
1) Push this repo to GitHub.
2) In AWS Console → App Runner → **Create service**.
3) Source: **GitHub** → pick repo/branch.
4) Deployment: **Dockerfile** (default).
5) Service settings:
   - Port: `8080`

## Environment variables
Set these in App Runner → Configuration → Environment variables.

Required for OpenAI:
- `OPENAI_API_KEY` = your key

Recommended:
- `BRAIN_PROVIDER` = `fallback`  (tries OpenAI → Ollama → mock)
- `BRAIN_OPENAI_MODEL` = `gpt-4o-mini`

If you do not have Ollama hosted yet, you can disable it by setting:
- `BRAIN_PROVIDER=openai`

## Test
After deploy, hit:
- `https://<your-service-url>/health`

Example request:
```bash
curl -s https://<your-service-url>/v1/brain/query \
  -H 'content-type: application/json' \
  -d '{"text":"What if I eat 60g carbs?","current_glucose":110,"digital_twin_id":1}'
```
