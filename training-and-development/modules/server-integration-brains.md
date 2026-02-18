# 🔌 Module: Server Integration (The Brains API)

## A Comprehensive Training Guide: Python Logic + Lovable UI

**Objective**: Master the "Headless Architecture" by connecting a powerful Python backend (The Brain) to a beautiful React frontend (The Face).

---

### 🏛️ Unit 1: The Concept Corner (Architecture 101)

#### Why split the "Brain" from the "Face"?

In modern AI development, we use the best tool for each job:

1. **The Brain (Backend)**: Written in **Python**. It handles complex logic, data simulation (like our glucose engine), and heavy AI processing. It lives on a server (Replit/Railway).
2. **The Face (Frontend)**: Written in **React/TypeScript**. It provides a snappy, beautiful user interface. It lives in the browser (Lovable/Vite).

#### The Bridge: REST API & CORS

To let The Face talk to The Brain, we use a **REST API**.

* **Request**: "Here is my current glucose." (Frontend -> Backend)
* **Response**: "Here is your prediction." (Backend -> Frontend)
* **CORS (Cross-Origin Resource Sharing)**: The security guard. We *must* explicitly tell the Python server, "It's okay to accept messages from `lovable.dev`."

---

### 🛠️ Unit 2: The Replit DevOps Drill

*Step-by-step prompts to make your Python server production-ready using the Replit Agent.*

#### Phase A: The Diagnosis

*Goal: Ensure the code actually runs before we expose it.*
> **Agent Prompt**: "Scan the `api/main.py` file. Are all imports installed in `pyproject.toml`? Run the server locally and verify the `/health` endpoint returns 200 OK."

#### Phase B: The Gateway (CORS)

*Goal: Open the doors for Lovable.*
> **Agent Prompt**: "Update `api/main.py` to enable CORS. Allow origins: `['*']` for development, or specifically `['https://lovable.dev', 'http://localhost:5173']`. Ensure `CORSMiddleware` is added *before* any routes."

#### Phase C: The Contract (OpenAPI)

*Goal: Give Lovable a map of our capabilities.*
> **Agent Prompt**: "Generate a `openapi.json` file based on the FastAPI app. Save it to the root directory so I can copy it."

#### Phase D: The Launch

*Goal: Keep it running 24/7.*
> **Agent Prompt**: "Configure the `.replit` file to run `uvicorn api.main:app --host 0.0.0.0 --port 80`. Set up an 'Always On' deployment so the public URL never sleeps."

---

### 🎨 Unit 3: The Lovable Blueprint

*How to build the UI and connect it to your new API.*

#### Step 1: The Connection

1. **Copy the Spec**: Open your `openapi.json` from Unit 2. Copy the entire content.
2. **Lovable Chat**: "I have a backend API. Here is the OpenAPI specification: [PASTE JSON]."
3. **Verify**: Lovable should say, "I see the `POST /v1/brain/query` endpoint."

#### Step 2: Building the "Brain Interface"
>
> **Lovable Prompt**: "Create a clean dashboard widget titled 'Digital Twin Query'. It should have:
>
> 1. A number input for 'Current Glucose'.
> 2. A text input for 'Question' (e.g., 'What should I eat?').
> 3. A 'Ask Brain' button that triggers the `POST /v1/brain/query` endpoint.
> 4. A display area for the AI's 'explanation' and a simple line chart for the 'simulation_data'."

#### Step 3: GitHub Sync

*Crucial for version control.*

1. Click the **GitHub Icon** in the Lovable header.
2. Select this repository (`greensdigitalsimulator`).
3. Choose the route: **Sync to `frontend/` folder**.

---

### � Unit 4: Brain Surgery (Configuration)

*Configuring the `BrainOrchestrator` to switch between modes.*

Your server supports multiple "Brains" via the `BRAIN_PROVIDER` environment variable.

| Provider | Value | Description | Cost |
|----------|-------|-------------|------|
| **Fallback** | `fallback` | Returns hardcoded mock data. Great for UI testing. | **Free** |
| **OpenAI** | `openai` | Uses GPT-4o for real reasoning. Requires API Key. | **$$$** |
| **Groq** | `groq` | Ultra-fast inference (Llama 3). Requires API Key. | **$** |

#### Changing Modes (Replit Secrets)

1. Go to **Tools > Secrets** in Replit.
2. Add `BRAIN_PROVIDER` = `openai`.
3. Add `OPENAI_API_KEY` = `sk-...`.
4. **Restart the Server** (Stop/Start) for changes to take effect.

---

### 🔧 Unit 5: Troubleshooting Guide

*What to do when the wires get crossed.*

#### 🛑 Error: "Network Error" or "Failed to fetch" on Frontend

* **Cause**: The API server is down, OR the URL is wrong, OR CORS is blocking it.
* **Fix**:
    1. Check the API URL in your browser (e.g., `https://my-repl.co/health`). If it spins, the server is down.
    2. Check the Browser Console (F12). Looking for "CORS policy: No 'Access-Control-Allow-Origin' header". -> **Redo Phase B**.

#### 🛑 Error: "500 Internal Server Error"

* **Cause**: The Python code crashed (bug).
* **Fix**: Check the **Console/Shell logs** in Replit. It will show the Python traceback. Did you forget an Environment Variable?

#### 🛑 Error: "422 Unprocessable Entity"

* **Cause**: You sent the wrong data format.
* **Fix**: Check the `POST` body. Did you send "glucose" as a string instead of a float? Lovable might be hallucinating the schema. **Redo Step 1** in Unit 3.
