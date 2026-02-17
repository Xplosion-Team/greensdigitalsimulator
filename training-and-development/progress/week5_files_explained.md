# Files Explained - Week 5: Python-to-Mobile Bridge

## Location: Root Directory

### 1. `api_server.py`
*   **Purpose**: The FastAPI server that bridges the Python Digital Twin simulation with the mobile app.
*   **Key Components**:
    *   `FastAPI`: The web framework used to create high-performance endpoints.
    *   `CORSMiddleware`: Configured to allow the mobile app (even on different devices) to securely request data.
    *   `DigitalTwin` Wrapper: Instances the simulation and provides it as a service.
    *   State Logic: Re-implements the classification logic on the server to ensure consistency.

## Location: `mobile-interface/app/`

### 2. `App.tsx` (API Connectivity)
*   **Purpose**: Transitioned from loading static files to fetching dynamic predictions.
*   **Key Components**:
    *   `fetchSimulation` (Function): Uses the standard `fetch` API to call the FastAPI server.
    *   Dynamic IP Support: Smartly detects if the app is running on Web (`localhost`) or a physical Phone (`Local IP`) to ensure connectivity.

---

## Technical Achievement
Week 5 moved the project from a "Simulation in a Box" to a **Real-Time System**. The mobile app now acts as a live monitor for a running Digital Twin, proving that the Python modeling and the TypeScript UI can work together seamlessly over a network.
