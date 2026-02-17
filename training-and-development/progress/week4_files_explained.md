# Files Explained - Week 4: Voice & Accessibility

## Location: `mobile-interface/app/`

### 1. `App.tsx` (Voice Updates)
*   **Purpose**: Integrated auditory feedback into the main application flow.
*   **Key Changes**:
    *   `expo-speech` Integration: Added logic to automatically speak "Critical" or "High" alerts.
    *   `handleRefresh` Hook: Now triggers a voice alert whenever the system detects a dangerous glucose change.

### 2. `screens/GlucoseStatusScreen.tsx` (Accessibility Updates)
*   **Purpose**: Enhanced the UI for users with visual or physical impairments.
*   **Key Changes**:
    *   `accessibilityLabel`: Added descriptive labels to all buttons and badges.
    *   `accessibilityRole`: Defined roles (e.g., "header", "button") to help screen readers navigate correctly.
    *   `Speak Message` Button: Added a manual trigger to read the current status and recommendation aloud.

---

## Accessibility Achievement
Week 4 ensured that the Greens Digital Twin is inclusive. By moving beyond just visual data, we've made the system usable for people with low vision or those who need hands-free alerts while managing their health.
