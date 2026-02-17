# Files Explained

## Location: `mobile-interface/logic/`

### 1. `glucoseStates.ts`
*   **Purpose**: Defines the fundamental types and logic for classifying glucose levels.
*   **Key Components**:
    *   `GlucoseState` (Enum): Lists all possible states (e.g., Stable, High, Low, Trending High).
    *   `classifyGlucoseState` (Function): Takes a glucose value and a trend rate, and returns the corresponding `GlucoseState`.
    *   `CLASSIFICATION_THRESHOLDS` (Constant): Stores the threshold values (e.g., 70 mg/dL for Low, 180 mg/dL for High).

### 2. `glucoseStates.test.ts`
*   **Purpose**: Automated tests to verify the correctness of the glucose classification logic.
*   **Key Components**:
    *   Uses **Jest** as the testing framework.
    *   Contains test cases for various scenarios (e.g., normal stable glucose, rapid rise, hypoglycemia) to ensure `classifyGlucoseState` returns the expected enum value.

### 3. `stateEngine.ts`
*   **Purpose**: The "brain" that integrates the raw data with the classification logic.
*   **Key Components**:
    *   `processGlucoseData` (Function): Takes an array of raw glucose readings, calculates the trend (rate of change) between points, and applies the `classifyGlucoseState` function to each point.
    *   Returns an enhanced dataset where every point has an associated state (e.g., "120 mg/dL" -> "Stable").

### 4. `loadSimulationData.ts`
*   **Purpose**: The specialized loader for the Digital Twin simulation output.
*   **Key Components**:
    *   `loadSimulationData` (Function): Parses the `simulation_results_final.csv` file. 
    *   It is specifically tuned to handle the complex 35-column schema, extracting the correct Digital Twin prediction (`cgm_NNDT`) from **Index 34**.

### 5. `runIntegration.ts`
*   **Purpose**: The main entry point for the Digital Twin to Mobile Interface integration.
*   **Usage**: Run via `npx ts-node mobile-interface/logic/runIntegration.ts`.
*   **Action**: Orchestrates the loading of simulation CSV data, processing it through the `stateEngine`, and saving the results.

### 6. `integrated_data.json`
*   **Purpose**: The final processed output file.
*   **Usage**: Contains the simulation results mapped to glucose states, ready for the mobile UI to consume. This replaces the old mock data with actual Digital Twin predictions.

### 7. `loadRealData.ts`
*   **Purpose**: Reads and parses real patient glucose data from generic CSV files (separate from the simulation).
*   **Key Components**:
    *   `loadRealData` (Function): Reads a CSV, skips headers, and converts rows into `GlucoseDataPoint` objects compatible with our engine.

---

## Location: `example/`

### 8. `runDigitalTwin.py`
*   **Purpose**: The main simulation script for the Digital Twin.
*   **Key Changes**: Updated to run in headless mode (saves plots instead of showing them) and outputs a clean `simulation_results_final.csv` for integration.
*   **Execution**: Requires the `.venv_fix` virtual environment to resolve `matplotlib` visualization errors.

### 9. `simulation_results_final.csv`
*   **Purpose**: The comprehensive output of the Digital Twin simulation.
*   **Content**: Contains actual readings, population models, and the Digital Twin's personalized predictions.

### 10. `img/example_digitaltwin4.png`
*   **Purpose**: The visual proof of the simulation.
*   **Content**: Shows a 24-hour window of simulated glucose, insulin, and carb data.
