# Files Explained - Week 2: Interpretation Layer

## Location: `mobile-interface/logic/`

### 1. `messageTemplates.ts`
*   **Purpose**: Centralizes all user-facing messaging based on glucose states and user roles.
*   **Key Components**:
    *   `UserRole` (Enum): Distinguishes between Patient, Caregiver, and Clinician.
    *   `MessageTemplate` (Type): Defines the structure of a message (Title, Body, Intensity).
    *   `messages` (Object): A mapping of `GlucoseState` to role-specific message content.
    *   `getMessageForState` (Function): Retrieves the correct message for a given state and role.

### 2. `recommendationEngine.ts`
*   **Purpose**: Provides actionable advice by combining glucose states with situational context.
*   **Key Components**:
    *   `ContextFactors` (Interface): Defines variables like `timeOfDay`, `mealContext`, and `activityContext`.
    *   `getRecommendation` (Function): Analyzes the current glucose state alongside context to provide a specific "Suggested Action".
    *   Contains logic for handling specific scenarios (e.g., "Nighttime Low" vs "Post-Exercise Stability").

### 3. `llmPromptBuilder.ts`
*   **Purpose**: Prepares structured data for Large Language Model (LLM) interpretation.
*   **Key Components**:
    *   `buildInterpretationPrompt` (Function): Converts numerical glucose data and context into a natural language prompt.
    *   Helps the AI "understand" the history and current situation to generate high-level health summaries.

---

## Technical Achievement
Week 2 shifted the project from raw numbers to **meaningful communication**, ensuring that the data provided by the Digital Twin is translated into language that patients and doctors can actually use.
