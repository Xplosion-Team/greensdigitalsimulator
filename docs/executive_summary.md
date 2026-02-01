# Greens Health Digital Twin - Executive Summary & Next Steps

**Date**: January 31, 2026  
**Project**: Glucose Digital Twin Mobile Interface for Seniors  
**Team**: Kehlin Swain (Greens Health), Mirna (Developer), Dr. Clara Mosquera (OHSU)

---

## 🎯 Your Questions Answered

### 1. **Top UI Apps for Seniors - Research Summary**

**Key Principles for Senior-Friendly Design**:

✅ **Large, High-Contrast Text**
- Minimum 18pt font size
- WCAG AAA contrast ratios (7:1)
- Sans-serif fonts (Inter, Roboto)

✅ **Simple Navigation**
- Maximum 3-5 main screens
- Large touch targets (44x44pt minimum)
- No hidden menus or gestures

✅ **Voice-First Interaction**
- Text-to-speech for all content
- Voice commands for primary actions
- Reduces cognitive load

✅ **Minimal Cognitive Load**
- One task per screen
- Plain language (no jargon)
- Visual cues (icons + text labels)

**Best Examples**:
- **Medisafe** (medication reminders) - Simple, colorful, voice-enabled
- **MySugr** (diabetes tracking) - Friendly tone, gamification
- **Livongo** (CGM monitoring) - Coaching + simple visuals

**What to Avoid**:
- ❌ Small text or buttons
- ❌ Complex charts without explanations
- ❌ Multi-step workflows
- ❌ Reliance on numerical literacy

---

### 2. **How to Add AI Model & Physics Engine**

You **already have the physics engine** — it's your Python glucose-insulin model!

**Current Setup**:
- **Physics Engine**: `/src/t1dsim_ai/individual_model.py`
  - Simulates glucose-insulin dynamics
  - Based on physiological equations
  - Predicts future glucose states

**Adding AI/LLM Layer**:

```
┌──────────────────────────────────────────────┐
│  Physics Engine (Python)                     │
│  • Glucose-insulin differential equations    │
│  • Predicts: "Glucose will be 165 in 1 hour" │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│  State Classifier (TypeScript)               │
│  • Converts numbers → states                 │
│  • Output: "Trending High"                   │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│  LLM Interpretation Layer (GPT-4/Claude)     │
│  • Converts states → plain language          │
│  • Personalizes for culture/language         │
│  • Output: "Your glucose is rising slowly.   │
│    A short walk may help."                   │
└──────────────────────────────────────────────┘
```

**Implementation (Week 2)**:
```typescript
// llmPromptBuilder.ts
async function generatePersonalizedMessage(
  state: GlucoseState,
  userProfile: UserProfile
): Promise<string> {
  const prompt = `
    Patient glucose state: ${state}
    Current value: ${glucose} mg/dL
    Trend: ${trend}
    
    User preferences:
    - Language: ${userProfile.language}
    - Cultural background: ${userProfile.culture}
    - Preferred foods: ${userProfile.foods}
    
    Generate a 1-2 sentence explanation and suggestion.
    Tone: warm, encouraging, non-clinical.
  `;
  
  const response = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [{ role: "user", content: prompt }]
  });
  
  return response.choices[0].message.content;
}
```

**Cost**: ~$0.004 per message (very affordable)

---

### 3. **Chat vs. Voice vs. Mobile - Which to Start?**

**Recommendation: Mobile-First with Voice Integration**

**Why Mobile?**
- ✅ Seniors increasingly use smartphones (85% of 65+ own one)
- ✅ Visual + voice = best of both worlds
- ✅ Can add SMS/chat later (same logic layer)
- ✅ Expo gives you iOS, Android, AND web preview

**Architecture (Multichannel Ready)**:

```
┌─────────────────────────────────────────────┐
│  Core Logic Layer (TypeScript)              │
│  • State classification                     │
│  • Message generation                       │
│  • Recommendation engine                    │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴───────┬───────────┬──────────┐
       │               │           │          │
       ▼               ▼           ▼          ▼
┌──────────┐    ┌──────────┐  ┌────────┐  ┌────────┐
│  Mobile  │    │   SMS    │  │  Voice │  │  Chat  │
│   App    │    │ (Twilio) │  │  IVR   │  │  Web   │
└──────────┘    └──────────┘  └────────┘  └────────┘
```

**Build Order**:
1. **Weeks 1-2**: Core logic (works for ALL channels)
2. **Weeks 3-4**: Mobile app (visual interface)
3. **Week 4**: Add voice to mobile app
4. **Week 6+**: SMS interface (reuses same logic)
5. **Future**: Web chat, IVR phone line

**Key Insight**: Build the "brain" first, then attach interfaces.

---

### 4. **What Should Be the NEXT Task?**

**Immediate Next Task (This Week)**:

> **Build the Glucose State Classification Engine**

**Why This First?**
- ✅ Core IP of your product
- ✅ Required for ALL interfaces (app, SMS, voice)
- ✅ Can be built and tested WITHOUT UI
- ✅ Perfect for Mirna to learn vibe coding

**Deliverable**: A TypeScript function that:
- Takes glucose readings
- Returns human-readable state + message
- Works independently of any UI

**Success Criteria**:
```typescript
// Input
const reading = {
  glucose: 165,
  previousGlucose: 150,
  timeDelta: 5 // minutes
};

// Output
const result = classifyAndExplain(reading);
// {
//   state: "Trending High",
//   message: "Your glucose has been slowly rising...",
//   action: "Consider a short walk or lighter snack",
//   urgency: "low"
// }
```

---

### 5. **Low-Code Programming for Mirna - What Does This Mean?**

**"Low-Code" in this context = Vibe Coding with Antigravity**

**Traditional Coding**:
1. Learn syntax (months)
2. Memorize APIs (weeks)
3. Debug cryptic errors (frustration)
4. Write boilerplate (tedious)

**Vibe Coding**:
1. Describe what you want in plain language
2. Antigravity generates code
3. You review and test
4. Iterate by chatting

**Example Workflow**:

**Mirna says to Antigravity**:
> "Create a function that takes current and previous glucose, calculates the rate of change, and returns 'rising', 'falling', or 'stable'."

**Antigravity generates**:
```typescript
function calculateTrend(
  current: number,
  previous: number,
  timeDelta: number
): 'rising' | 'falling' | 'stable' {
  const rateOfChange = (current - previous) / timeDelta;
  
  if (rateOfChange > 1) return 'rising';
  if (rateOfChange < -1) return 'falling';
  return 'stable';
}
```

**Mirna tests it**:
> "Test this with current=150, previous=140, timeDelta=5"

**Antigravity responds**:
> "Result: 'rising' (rate of change = 2 mg/dL/min)"

**Mirna refines**:
> "Make the threshold configurable"

**Antigravity updates**:
```typescript
function calculateTrend(
  current: number,
  previous: number,
  timeDelta: number,
  threshold: number = 1
): 'rising' | 'falling' | 'stable' {
  // ... updated code
}
```

**Key Benefits**:
- ✅ Mirna learns by doing, not memorizing
- ✅ Focuses on logic, not syntax
- ✅ Faster iteration
- ✅ AI handles TypeScript complexity

---

### 6. **Product Development Roadmap - Priority Order**

Based on your 18-month plan, here's the **critical path**:

#### **Phase 0 (NOW - Feb 15): Foundation**
- [x] Python digital twin working
- [ ] **State classification engine** ← START HERE
- [ ] Message templates
- [ ] Mock data pipeline

#### **Phase 1 (Feb 15 - Mar 31): Mobile Prototype**
- [ ] Expo app with one screen
- [ ] Voice output (TTS)
- [ ] Accessibility compliance
- [ ] Internal demo to stakeholders

#### **Phase 2 (Apr 1 - May 31): Multichannel**
- [ ] SMS interface (Twilio)
- [ ] Voice input (STT)
- [ ] LLM personalization
- [ ] User preference system

#### **Phase 3 (Jun 1 - Aug 31): Real Data**
- [ ] Dexcom CGM integration
- [ ] Python API server
- [ ] Real-time predictions
- [ ] Onboarding workflow

#### **Phase 4 (Sep 1 - Dec 31): Pilot**
- [ ] Beta testing with 10-20 seniors
- [ ] Health navigator integration
- [ ] Clinical validation (Dr. Mosquera)
- [ ] Branding & naming

**Critical Dependencies**:
1. **State engine MUST be done first** (everything depends on it)
2. **Mobile UI before SMS** (easier to debug visually)
3. **Mock data before real CGM** (test logic safely)

---

## 🎓 Mirna's Learning Path (Low-Code Approach)

### **Week 1: Logic, No UI**
- Understand digital twin output
- Build state classifier
- Generate mock data
- **Tools**: TypeScript, Node.js, Antigravity

### **Week 2: Messages, No UI**
- Create message templates
- Build LLM prompts
- Test with different scenarios
- **Tools**: TypeScript, OpenAI API (optional)

### **Week 3: First Screen**
- Initialize Expo app
- Build one simple screen
- Display state + message
- **Tools**: Expo, React Native, Antigravity

### **Week 4: Voice & Accessibility**
- Add text-to-speech
- Test with VoiceOver
- Improve contrast/fonts
- **Tools**: expo-speech, accessibility inspector

### **Week 5-6: Integration**
- Create Python API
- Connect to digital twin
- Real predictions
- **Tools**: Flask, API testing

**Key Principle**: Mirna doesn't need to be a React expert or TypeScript wizard. Antigravity handles the complexity. She focuses on:
- **What** the app should do
- **How** users will experience it
- **Why** each feature matters for seniors

---

## 📋 Immediate Action Items (This Week)

### **For Mirna**:
1. [ ] Read `mirna_training_program.md`
2. [ ] Follow `week1_quickstart.md` checklist
3. [ ] Set up development environment
4. [ ] Run existing Python digital twin
5. [ ] Create `glucoseStates.ts` with Antigravity's help

### **For Kehlin**:
1. [ ] Review training materials
2. [ ] Schedule weekly check-in with Mirna (Fridays?)
3. [ ] Connect with Dr. Mosquera about state definitions
4. [ ] Define glucose thresholds for each state
5. [ ] Gather example messages for different scenarios

### **For Team**:
1. [ ] Decide: iOS-first or iOS + Android simultaneously?
2. [ ] Confirm LLM provider (OpenAI vs. Anthropic)
3. [ ] Set up GitHub repo structure
4. [ ] Create project board (Trello/Jira/GitHub Projects)

---

## 🚀 Success Metrics (End of Month 1)

By **February 28, 2026**, you should have:

- [ ] **Working state engine** (TypeScript)
- [ ] **Mock data pipeline** (24hr glucose simulation)
- [ ] **Message templates** (3 audiences: patient, caregiver, clinician)
- [ ] **Basic mobile screen** (shows state + message)
- [ ] **Voice output** (reads messages aloud)
- [ ] **Demo video** (for stakeholders)

**This proves the concept** and sets foundation for CGM integration.

---

## 💡 Key Insights

### **1. You Already Have the Hard Part**
The glucose-insulin model is the complex physics. Everything else is "just" interface design.

### **2. Build the Brain First**
State classification + message generation works the same for app, SMS, voice. Build it once, use everywhere.

### **3. Vibe Coding Lowers the Bar**
Mirna doesn't need years of coding experience. With Antigravity, she can build production-quality code by describing what she wants.

### **4. Seniors Need Simple, Not Simplistic**
Large fonts and voice aren't enough. The **language** and **guidance** must be warm, clear, and actionable.

### **5. Multichannel is the Future**
Not everyone has a smartphone. SMS + voice + app ensures equity.

---

## 📞 Next Steps

**This Week**:
- Mirna starts Week 1 training
- Kehlin defines glucose state thresholds
- Team reviews project structure

**Next Week**:
- Mirna builds message templates
- Team reviews first deliverables
- Plan LLM integration

**By End of Month**:
- Working prototype demo
- Stakeholder presentation
- Plan Phase 2 (multichannel)

---

## 🎯 The Bottom Line

**Next Task**: Build the glucose state classification engine (Week 1)  
**Best Approach**: Mobile-first with voice, expandable to SMS/chat  
**Mirna's Path**: Vibe coding with Antigravity (low-code, high-impact)  
**Timeline**: 4-6 weeks to working prototype  

**You're not building a glucose tracker. You're building an AI health companion for seniors.** 🚀

---

**Questions? Start with Antigravity:**
> "I'm ready to start Week 1. Help me set up my development environment and create the first TypeScript file."
