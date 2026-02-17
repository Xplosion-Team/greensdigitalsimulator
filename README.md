# Greens Digital Simulator

This project contains the Digital Twin simulation and the mobile interface logic.

## Setup

1.  **Python Environment**:
    *   Create a virtual environment: `python -m venv .venv`
    *   Install dependencies: `pip install -r requirments.txt` && `pip install -e .`

2.  **Node.js Environment**:
    *   Install dependencies: `npm install`
    *   Run tests: `npm test`

## Digital Twin

The digital twin simulation is located in `example/runDigitalTwin.py`.
Run it with: `python example/runDigitalTwin.py`

## Mobile Interface Logic

The logic for the mobile app is in `mobile-interface/logic`.

*   `glucoseStates.ts`: Glucose state classification logic.
*   `mockGlucoseData.ts`: Generates mock glucose data.
*   `stateEngine.ts`: Integrates data and classification.

### Generating Mock Data

Run: `npx ts-node mobile-interface/logic/generateData.ts`

### Testing Logic

Run: `npx jest`

