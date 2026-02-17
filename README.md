# Greens Digital Simulator

A comprehensive Digital Twin simulation framework for Type 1 Diabetes (T1D) management, featuring predictive modeling, a web-based dashboard, and mobile interface logic.

## 🌟 Overview
Greens Digital Simulator allows users to simulate glucose dynamics using personalized "Digital Twins". It integrates AI-driven predictions with real-time data to help visualize the impact of meals, insulin, and activity on blood glucose levels.

## 🚀 Key Features
- **Digital Twin Simulation**: High-fidelity glucose forecasting using Neural Networks.
- **Web Dashboard**: Interactive interface for running simulations and visualizing results.
- **Voice Food Logging**: Integrated nutrition parsing via voice commands.
- **Mobile Engine**: TypeScript-based logic for glucose state classification and urgency analysis (Low/High/Trending).
- **REST API**: FastAPI backend to serve simulation data to mobile or web clients.

## 📁 Project Structure
- `t1dsim_ai/`: Core Digital Twin modeling and simulation engine.
- `example/`: Python entry points for the simulation (`runDigitalTwin.py`) and Web App (`app.py`).
- `mobile-interface/`: TypeScript engine (`stateEngine.ts`) and mock data generation.
- `api_server.py`: FastAPI server providing endpoints for simulation data.
- `src/`: Core Python source code.

## 🛠️ Setup & Installation

### Python Environment (Simulation & Backend)
1.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```
2.  **Install dependencies**:
    ```bash
    pip install -e .
    pip install -r requirements.txt
    ```

### Node.js Environment (Mobile Logic)
1.  **Install dependencies**:
    ```bash
    npm install
    ```

## 🏃 Running the Project

### 1. Digital Twin CLI Simulation
Run a baseline simulation showing glucose predictions vs actual data:
```bash
cd example
python runDigitalTwin.py
```

### 2. Web Interface
Start the interactive dashboard:
```bash
cd example
python app.py
```
*Access at: http://localhost:5000*

### 3. API Server
Run the FastAPI backend for mobile data integration:
```bash
python api_server.py
```
*Access at: http://localhost:8000*

### 4. Mobile Logic (Mock Data Generation)
Generate simulated glucose data for the mobile state engine:
```bash
npx ts-node mobile-interface/logic/generateData.ts
```

## 🧪 Testing

- **Python Tests**: `pytest`
- **Mobile Logic Tests**: `npm test`

## 📚 Further Documentation
- [Quick Start Guide](QUICKSTART.md)
- [API Documentation](API.md)
- [Architecture Overview](ARCHITECTURE.md)
- [FAQ](FAQ.md)

---
*Maintained by the Greens Health Team.*
