# Greens Health: Intelligence Layer (The Brain)

The `brain_llm.py` module serves as the cognitive interface for the Greens Health Digital Twin platform. It is designed to bridge the gap between unstructured human language and the rigorous physical simulations of the T1D Physics Engine.

## Core Functions

### 1. `parse_intent(query)`
*   **Purpose**: Translates natural language into structured simulation parameters.
*   **How it works**: It scans user input (e.g., *"I want to eat a 60g carb burger"*) and extracts key variables like `carbs`, `type`, and `time_offset`.
*   **Current State**: Rule-based regex for reliable prototyping.
*   **Future Upgrade**: Semantic extraction using LLMs (GPT-4/Llama 3) to handle complex queries like *"I had a snack an hour ago and I'm planning a big dinner soon."*

### 2. `generate_explanation(context)`
*   **Purpose**: Converts raw data points (mg/dL, trend lines) into empathetic, senior-friendly physiological advice.
*   **How it works**: It takes the Digital Twin's predicted peak glucose and current starting state to build a narrative response.
*   **Senior Literacy Focus**: It avoids clinical jargon (like "hyperglycemia") in favor of plain language (like "a bit high") and actionable suggestions (like "a short walk").

---

## Future Use Cases & Roadmap

### 1. Symptom Attribution (RAG)
**Scenario**: User asks, *"Why do I feel so tired right now?"* 
The Brain will use **Retrieval-Augmented Generation (RAG)** to look at the last 6 hours of simulation data, identify a "glucose roller coaster" (rapid rise and fall), and explain: *"You're likely feeling a 'sugar crash' from the high you had after lunch."*

### 2. Multi-Activity "What-If" Simulations
**Scenario**: User asks, *"Can I eat this cake if I go for a 20-minute walk after?"*
The Brain will orchestrate **compound scenarios**:
1. Run Meal Simulation.
2. Overlay Exercise Simulation.
3. Compare the net result to show the user how activity "offsets" the glucose spike.

### 3. Cultural & Language Personalization
The Brain will adapt its tone and meal suggestions based on the user's cultural background. 
*   **Example**: Providing context for a traditional Sunday dinner vs. a quick weekday breakfast, ensuring the advice feels personal and non-judgmental.

### 4. Vision-to-Simulation Logging
Integrating with a camera, the Brain could analyze a photo of a plate, estimate the carbs, and **automatically trigger a simulation** before the user even takes the first bite, providing a proactive "look-ahead" warning.

---

## Technical Configuration
The module supports multiple providers via the `provider` argument in the constructor:
*   `"mock"`: No API key required. Best for logic testing.
*   `"openai"`: High intelligence, cloud-based (Requires `OPENAI_API_KEY`).
*   `"local_llama"`: Private, offline intelligence for maximum data security.
