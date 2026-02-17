# Files Explained - Week 3: Mobile UI Foundation

## Location: `mobile-interface/app/`

### 1. `App.tsx` (Entry Point)
*   **Purpose**: The main controller for the mobile application.
*   **Key Components**:
    *   State Management: Tracks the current glucose reading being displayed.
    *   Refresh Logic: Simulates real-time data flow by cycling through the simulation results.
    *   Navigation: Currently serves as the primary container for the status dashboard.

### 2. `screens/GlucoseStatusScreen.tsx`
*   **Purpose**: The primary dashboard view for the patient.
*   **Key Components**:
    *   Header: Displays the current glucose value and trend arrow.
    *   Status Card: Shows the interpreted state (e.g., "Trending High") using the logic from Week 2.
    *   Recommendation Section: Displays the "Suggested Action" from the Recommendation Engine.

### 3. `components/GlucoseBadge.tsx`
*   **Purpose**: A reusable UI component for visual state feedback.
*   **Key Components**:
    *   Dynamic Styling: Automatically changes color based on the `GlucoseState` (Red for Low, Orange for High, Green for Stable).
    *   Accessibility: Built with proper touch targets and visual contrast.

---

## Logic Integration
This week successfully linked the **Logic Layer** (Weeks 1-2) with the **UI Layer**. The app now consumes the `integrated_data.json` produced by the Digital Twin simulation, making the "Twin" visible on a mobile screen for the first time.
