# MIRNA Training Program
## Digital Twin Glucose Dynamics → Mobile Interface (Vibe Coding with Antigravity)

![Digital Twin Architecture](/Users/kehlinswain/.gemini/antigravity/brain/ae64b08f-7bfe-4b72-9167-77a7385804d6/uploaded_media_1769908229141.png)

---

## 🎯 Program Overview

**Duration**: 4-6 weeks  
**Approach**: Digital Twin First → Vibe Coding → Mobile UI  
**Tools**: Antigravity AI, Expo (React Native), TypeScript, Python Digital Twin Engine  
**Goal**: Build an interpretable glucose monitoring interface for seniors

---

## 🧠 What is "Vibe Coding" with Antigravity?

**Vibe Coding** = Conversational, AI-assisted development where you:
- Describe what you want in plain language
- Antigravity generates code, suggests architecture, and debugs
- You iterate by chatting, not memorizing syntax
- Focus on **logic and user experience**, not boilerplate

**Why this works for Mirna**:
- Lower barrier to entry (less syntax memorization)
- Faster prototyping
- AI handles TypeScript/React Native complexity
- You focus on glucose dynamics and user needs

---

## 📋 Prerequisites & Setup

### Required Tools
- [ ] **Antigravity AI** (already using!)
- [ ] **Node.js** (v18+) and npm
- [ ] **Expo CLI** (`npm install -g expo-cli`)
- [ ] **Python 3.10+** (for digital twin engine)
- [ ] **VS Code** or preferred editor
- [ ] **iOS Simulator** (Xcode) or **Android Emulator**
- [ ] **Git** for version control

### Required Knowledge (Learn as You Go)
- Basic programming concepts (variables, functions, if/else)
- JSON data format
- How to use terminal/command line
- **NOT required**: Deep React/TypeScript knowledge (Antigravity helps!)

---

## 🗓 Week-by-Week Training Plan

---

## **WEEK 1: Understanding the Digital Twin Engine**

### Goal
Understand how the existing Python glucose simulator works and what data it produces.

### Key Concepts
- **Digital Twin**: A computational model that mirrors real-world glucose dynamics
- **Inputs**: Glucose readings, meals, activity, insulin
- **Outputs**: Predicted glucose states, trends, risk levels
- **State Machine**: Converting continuous data → discrete states (Stable, Trending High, At Risk)

### Tasks

#### 1.1 Explore the Existing Python Simulator (Day 1-2)

**With Antigravity, ask:**
> "Show me how the glucose simulator in `/src/t1dsim_ai/` works. What are the main components?"

**Files to understand**:
- `individual_model.py` - Core glucose dynamics model
- `create_scenarios.py` - Scenario generation
- `population_model.py` - Multi-patient modeling

**Action**: Run an example simulation
```bash
cd /Users/kehlinswain/Documents/GitHub/greensdigitalsimulator
python example/runDigitalTwin.py
```

**Vibe Coding Prompt for Antigravity**:
> "Run the digital twin simulator and explain the output. What does each column mean?"

#### 1.2 Define Glucose States (Day 3-4)

**Create**: `/mobile-interface/logic/glucoseStates.ts`

**Vibe Coding Prompt**:
> "Help me create a TypeScript file that defines glucose states:
> - Stable (70-140 mg/dL, not changing rapidly)
> - Trending High (140-180 mg/dL, rising)
> - High Risk (>180 mg/dL or rapidly rising)
> - Trending Low (<70 mg/dL or rapidly falling)
> 
> Include a function that takes current glucose, previous glucose, and time delta, then returns the state."

**Expected Output**: A state classification function

#### 1.3 Mock Data Generation (Day 5)

**Vibe Coding Prompt**:
> "Create a mock data generator that simulates glucose readings every 5 minutes for 24 hours. Include realistic patterns like:
> - Morning spike after breakfast
> - Post-lunch rise
> - Overnight stability
> 
> Export as JSON format."

**Deliverable**: `mockGlucoseData.json`

---

## **WEEK 2: Building the Interpretation Layer**

### Goal
Translate glucose states into plain-language explanations suitable for seniors.

### Key Concepts
- **Explainability**: Making AI/model outputs human-readable
- **Audience Adaptation**: Different messages for patients, caregivers, clinicians
- **Cultural Sensitivity**: Language and food references that resonate

### Tasks

#### 2.1 Create Message Templates (Day 1-2)

**Create**: `/mobile-interface/logic/messageTemplates.ts`

**Vibe Coding Prompt**:
> "Create a message template system for glucose states. For each state (Stable, Trending High, High Risk, Trending Low), provide:
> 
> 1. **Patient message** (warm, simple, actionable)
> 2. **Caregiver message** (informative, reassuring)
> 3. **Clinician message** (technical, precise)
> 
> Example for 'Trending High':
> - Patient: 'Your glucose has been slowly rising this afternoon. A short walk or lighter snack may help.'
> - Caregiver: 'Their glucose is trending upward. Encourage light activity or check if they had a large meal.'
> - Clinician: 'BG trending +15 mg/dL/hr. Current: 165 mg/dL. Consider bolus adjustment.'"

#### 2.2 Add Contextual Recommendations (Day 3-4)

**Vibe Coding Prompt**:
> "Extend the message system to include context-aware recommendations:
> - Time of day (morning, afternoon, evening, overnight)
> - Recent meals (if data available)
> - Activity level
> 
> For example, 'Trending High' at 2 PM after lunch should suggest a walk, but 'Trending High' at 10 PM should suggest checking insulin and preparing for bed."

#### 2.3 LLM Integration Prep (Day 5)

**Vibe Coding Prompt**:
> "Create a function that formats glucose data and state into a prompt for an LLM (like GPT-4 or Claude). The LLM should:
> - Personalize the message based on user preferences (language, cultural food references)
> - Adjust tone (encouraging vs. urgent)
> - Keep it under 2 sentences
> 
> Don't integrate the API yet—just prepare the prompt structure."

**Deliverable**: `llmPromptBuilder.ts`

---

## **WEEK 3: Mobile Interface Foundation (Expo + React Native)**

### Goal
Build a simple mobile app that displays glucose states and messages.

### Key Concepts
- **Expo**: Framework for building React Native apps quickly
- **React Native**: JavaScript framework for iOS/Android apps
- **Component-Based UI**: Reusable building blocks (buttons, cards, text)

### Tasks

#### 3.1 Initialize Expo Project (Day 1)

**Vibe Coding Prompt**:
> "Help me create a new Expo project called 'greens-glucose-twin' in `/Users/kehlinswain/Documents/GitHub/greensdigitalsimulator/mobile-interface/`. Use TypeScript. Set it up so I can run it on iOS simulator."

**Commands** (Antigravity will guide):
```bash
npx create-expo-app greens-glucose-twin --template expo-template-blank-typescript
cd greens-glucose-twin
npm start
```

#### 3.2 Build the State Display Screen (Day 2-3)

**Vibe Coding Prompt**:
> "Create a single screen called 'GlucoseStatusScreen' that shows:
> 
> 1. **State Badge**: Large, color-coded badge (green=Stable, yellow=Trending, red=Risk)
> 2. **Current Glucose**: Big number (e.g., '142 mg/dL')
> 3. **Trend Arrow**: ↑ ↗ → ↘ ↓
> 4. **Plain-Language Message**: The explanation from our message templates
> 5. **Suggested Action**: One simple next step
> 
> Use large fonts and high contrast for seniors. No charts yet."

**Design Requirements**:
- Font size: 18pt minimum
- High contrast (WCAG AAA)
- Touch targets: 44x44pt minimum
- Simple, uncluttered layout

#### 3.3 Connect Mock Data (Day 4-5)

**Vibe Coding Prompt**:
> "Import the mock glucose data we created in Week 1. When the app loads:
> 1. Read the latest glucose value
> 2. Calculate the state using our `glucoseStates.ts` logic
> 3. Display the appropriate message
> 
> Add a 'Refresh' button that simulates getting a new reading."

**Deliverable**: Working app showing glucose state on simulator

---

## **WEEK 4: Voice Interface & Accessibility**

### Goal
Add voice output for visually impaired users and voice input for hands-free interaction.

### Key Concepts
- **Text-to-Speech (TTS)**: App reads messages aloud
- **Speech-to-Text (STT)**: User asks questions via voice
- **Accessibility**: Making tech usable for all abilities

### Tasks

#### 4.1 Add Text-to-Speech (Day 1-2)

**Vibe Coding Prompt**:
> "Add text-to-speech to the app using Expo's `expo-speech` library. When the glucose state updates:
> 1. Automatically read the message aloud
> 2. Add a 'Read Aloud' button for manual playback
> 3. Use a warm, calm voice
> 
> Make sure it works on iOS simulator."

#### 4.2 Voice Commands (Day 3-4)

**Vibe Coding Prompt**:
> "Add voice input using `expo-speech-recognition` (or similar). Allow users to ask:
> - 'What's my glucose?'
> - 'Am I okay?'
> - 'What should I do?'
> 
> Respond with the appropriate message via TTS."

#### 4.3 Accessibility Audit (Day 5)

**Vibe Coding Prompt**:
> "Review the app for accessibility:
> - Screen reader compatibility (VoiceOver on iOS)
> - Color contrast ratios
> - Touch target sizes
> - Keyboard navigation (if applicable)
> 
> Suggest improvements."

**Deliverable**: Voice-enabled app with accessibility report

---

## **WEEK 5-6: Integration & Advanced Features**

### Goal
Connect to real data sources and add predictive features.

### Tasks

#### 5.1 Python-to-Mobile Bridge (Week 5, Day 1-3)

**Vibe Coding Prompt**:
> "Create a simple API endpoint using Flask or FastAPI that:
> 1. Runs the Python digital twin model
> 2. Returns glucose predictions for the next 2 hours
> 3. Can be called from the mobile app
> 
> Start with local testing (both on same machine)."

#### 5.2 Real-Time Predictions (Week 5, Day 4-5)

**Vibe Coding Prompt**:
> "Update the mobile app to:
> 1. Call the Python API every 5 minutes
> 2. Display predicted glucose trend
> 3. Show 'What if' scenarios (e.g., 'If you eat now, glucose may rise to X')
> 
> Keep the UI simple—just add a 'Prediction' section below current state."

#### 5.3 CGM Integration Prep (Week 6)

**Vibe Coding Prompt**:
> "Research how to integrate Dexcom CGM data:
> 1. What APIs are available?
> 2. What authentication is needed?
> 3. Create a mock CGM data stream for testing
> 
> Don't implement yet—just document the approach."

**Deliverable**: Integration plan document

---

## 🛠 Vibe Coding Best Practices with Antigravity

### How to Ask Effective Questions

#### ✅ Good Prompts
- "Create a function that takes glucose and time, returns a state object"
- "Show me how to add a button that reads text aloud using Expo"
- "Explain why this error is happening: [paste error]"
- "Refactor this code to be more readable for seniors"

#### ❌ Avoid
- "Make it work" (too vague)
- "Build the whole app" (too broad)
- Asking without providing context (share relevant code)

### Iterative Development Pattern

1. **Describe** what you want in plain language
2. **Review** the code Antigravity generates
3. **Test** it in your app
4. **Refine** by asking follow-up questions
5. **Repeat** until it works

### When You Get Stuck

**Ask Antigravity**:
- "Why isn't this working?"
- "What does this error mean?"
- "Show me a simpler way to do this"
- "Explain this code like I'm new to programming"

---

## 📊 Success Metrics

By the end of 6 weeks, Mirna should have:

- [ ] **Working mobile app** (iOS simulator)
- [ ] **Glucose state classification** (logic working)
- [ ] **Plain-language explanations** (readable by seniors)
- [ ] **Voice output** (TTS working)
- [ ] **Mock data integration** (simulated glucose readings)
- [ ] **Python API connection** (digital twin predictions)
- [ ] **Accessibility compliance** (basic WCAG standards)

---

## 🎓 Learning Resources

### Expo & React Native
- [Expo Documentation](https://docs.expo.dev/)
- [React Native Basics](https://reactnative.dev/docs/getting-started)

### TypeScript
- [TypeScript in 5 Minutes](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html)

### Digital Twins
- Review existing code in `/src/t1dsim_ai/`
- Ask Antigravity to explain specific functions

### Accessibility
- [iOS Accessibility Guidelines](https://developer.apple.com/accessibility/ios/)
- [WCAG Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)

---

## 🚀 Next Steps After Training

1. **User Testing**: Test with 2-3 seniors, gather feedback
2. **Real CGM Integration**: Connect to Dexcom API
3. **SMS Interface**: Build text message version (Phase 2)
4. **LLM Personalization**: Integrate GPT-4 for cultural adaptation
5. **Clinical Validation**: Work with Dr. Mosquera on model accuracy

---

## 📝 Weekly Check-Ins

**Every Friday**, Mirna should:
1. Demo what was built that week
2. Share one challenge and how it was solved
3. Ask one question for next week

**Kehlin's Role**:
- Review code weekly
- Provide glucose domain expertise
- Connect with Dr. Mosquera for model questions

---

## 🎯 Key Takeaway

**You don't need to be a coding expert to build this.**

With Antigravity and vibe coding:
- Focus on **what** you want, not **how** to code it
- Iterate quickly with AI assistance
- Learn by doing, not by memorizing syntax

**The digital twin is the hard part—you already have it.**  
Now we're just making it accessible to seniors. 🚀
