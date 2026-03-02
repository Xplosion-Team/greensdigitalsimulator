# 💾 Module: Database Vibe Coding

## Goal
Use natural language (Vibe Coding) to design and implement a persistent database for storing health metrics.

## What is Vibe Coding?
Vibe Coding is the practice of describing a system's behavior and data needs to an AI, allowing it to generate the schema, migrations, and CRUD (Create, Read, Update, Delete) logic.

## The Objective
We need to store every glucose reading from the Digital Twin so we can perform historical analysis.

### Step 1: The Prompt
*Prompting Antigravity:*
> "I need a database schema for `GlucoseReading`. It needs a timestamp, the value (mg/dL), a source (Simulation vs Dexcom), and a user ID. Please use SQLModel or SQLAlchemy."

### Step 2: Verification
Once the code is generated, run a script to:
1. Create the tables.
2. Insert a "dummy" reading.
3. Query it back to ensure it saved correctly.

## Essential Models
- `User`: Profile settings and targets.
- `GlucoseReading`: The core time-series data.
- `MealLog`: Context for glucose spikes.

## Run Simulation 🧪
Experience Vibe Coding with this SQLite demo:
`python simulations/simulate_db_vibe.py`

---
*Back to [Training Plan](../MIRNA_TRAINING_PLAN.md)*
