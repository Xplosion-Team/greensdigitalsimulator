# Week 1 Quick-Start Checklist
## Digital Twin Fundamentals (Mirna's First Week)

---

## 🎯 This Week's Goal
Understand the glucose digital twin engine and create the state classification logic.

---

## ✅ Day-by-Day Tasks

### **Monday: Environment Setup**

#### Morning (2 hours)
- [ ] Verify Antigravity AI is working
- [ ] Check Python installation: `python --version` (should be 3.10+)
- [ ] Check Node.js installation: `node --version` (should be 18+)
- [ ] Install Expo CLI: `npm install -g expo-cli`

#### Afternoon (2 hours)
- [ ] Navigate to project: `cd /Users/kehlinswain/Documents/GitHub/greensdigitalsimulator`
- [ ] Create Python virtual environment: `python -m venv .venv`
- [ ] Activate it: `source .venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirments.txt`

**Vibe Coding Prompt for Antigravity**:
> "I'm in the greensdigitalsimulator directory. Help me verify that all dependencies are installed correctly and the Python environment is ready."

---

### **Tuesday: Explore the Digital Twin**

#### Morning (2 hours)
- [ ] Read `/src/t1dsim_ai/individual_model.py`

**Vibe Coding Prompt**:
> "Explain what `individual_model.py` does. What are the key inputs and outputs? How does it simulate glucose dynamics?"

- [ ] Read `/example/runDigitalTwin.py`

**Vibe Coding Prompt**:
> "Walk me through `runDigitalTwin.py`. What does it do step-by-step?"

#### Afternoon (2 hours)
- [ ] Run the digital twin: `python example/runDigitalTwin.py`
- [ ] Observe the output

**Vibe Coding Prompt**:
> "I ran the digital twin. Here's the output: [paste output]. Explain what each column means and what patterns I should notice."

---

### **Wednesday: Define Glucose States**

#### Morning (2 hours)
- [ ] Create new directory: `mkdir -p mobile-interface/logic`
- [ ] Create file: `mobile-interface/logic/glucoseStates.ts`

**Vibe Coding Prompt**:
> "Help me create a TypeScript file at `mobile-interface/logic/glucoseStates.ts` that defines glucose states. I need:
> 
> **States**:
> - Stable: 70-140 mg/dL, change < 5 mg/dL per 5 min
> - Trending High: 140-180 mg/dL OR rising > 5 mg/dL per 5 min
> - High Risk: > 180 mg/dL OR rising > 10 mg/dL per 5 min
> - Trending Low: < 70 mg/dL OR falling > 5 mg/dL per 5 min
> - Low Risk: < 55 mg/dL OR falling > 10 mg/dL per 5 min
> 
> **Function signature**:
> ```typescript
> function classifyGlucoseState(
>   currentGlucose: number,
>   previousGlucose: number,
>   timeDeltaMinutes: number
> ): GlucoseState
> ```
> 
> Include TypeScript types and comments explaining the logic."

#### Afternoon (2 hours)
- [ ] Review the generated code
- [ ] Test it with sample values

**Vibe Coding Prompt**:
> "Create a test file `glucoseStates.test.ts` that tests these scenarios:
> 1. Stable: current=100, previous=98, delta=5min → should return 'Stable'
> 2. Trending High: current=150, previous=140, delta=5min → should return 'Trending High'
> 3. High Risk: current=200, previous=180, delta=5min → should return 'High Risk'
> 
> Show me how to run these tests with Node.js."

---

### **Thursday: Mock Data Generation**

#### Morning (2 hours)
- [ ] Create file: `mobile-interface/logic/mockGlucoseData.ts`

**Vibe Coding Prompt**:
> "Create a mock glucose data generator that simulates 24 hours of readings (every 5 minutes = 288 readings). Include realistic patterns:
> 
> **Patterns**:
> - Overnight (12am-6am): Stable around 90-110 mg/dL
> - Breakfast spike (7am-9am): Rise to 140-160 mg/dL
> - Morning dip (10am-11am): Drop to 100-120 mg/dL
> - Lunch spike (12pm-2pm): Rise to 150-170 mg/dL
> - Afternoon stable (3pm-5pm): 110-130 mg/dL
> - Dinner spike (6pm-8pm): Rise to 160-180 mg/dL
> - Evening decline (9pm-11pm): Drop to 100-120 mg/dL
> 
> Export as JSON array with format:
> ```json
> [
>   { \"timestamp\": \"2024-01-01T00:00:00Z\", \"glucose\": 95 },
>   { \"timestamp\": \"2024-01-01T00:05:00Z\", \"glucose\": 97 },
>   ...
> ]
> ```"

#### Afternoon (2 hours)
- [ ] Generate the mock data
- [ ] Save to `mobile-interface/data/mockGlucoseData.json`
- [ ] Visualize it (optional)

**Vibe Coding Prompt**:
> "Create a simple script that reads `mockGlucoseData.json` and prints a text-based chart showing glucose over 24 hours. Just use asterisks (*) to show levels."

---

### **Friday: Integration & Review**

#### Morning (2 hours)
- [ ] Create `mobile-interface/logic/stateEngine.ts`

**Vibe Coding Prompt**:
> "Create a 'state engine' that combines everything we built this week:
> 
> 1. Import the mock glucose data
> 2. For each reading, calculate the state using `classifyGlucoseState`
> 3. Return an array of results with format:
> ```typescript
> {
>   timestamp: string,
>   glucose: number,
>   state: GlucoseState,
>   trend: 'rising' | 'falling' | 'stable'
> }
> ```
> 
> Add a function to get the 'current' state (most recent reading)."

#### Afternoon (2 hours)
- [ ] Test the full pipeline
- [ ] Document what you learned

**Vibe Coding Prompt**:
> "Help me create a README.md in `mobile-interface/` that explains:
> 1. What we built this week
> 2. How to run the state engine
> 3. What the output means
> 
> Keep it simple—this is for my own reference."

---

## 🎓 End-of-Week Deliverables

You should have:
- [ ] `mobile-interface/logic/glucoseStates.ts` - State classification logic
- [ ] `mobile-interface/logic/mockGlucoseData.ts` - Data generator
- [ ] `mobile-interface/data/mockGlucoseData.json` - 24 hours of mock data
- [ ] `mobile-interface/logic/stateEngine.ts` - Full pipeline
- [ ] `mobile-interface/README.md` - Documentation

---

## 🤔 Reflection Questions (Friday afternoon)

1. **What was the hardest part this week?**
2. **What did you learn about glucose dynamics?**
3. **What questions do you have about the digital twin model?**
4. **Are you comfortable with TypeScript basics?**

---

## 📊 Success Criteria

By end of Week 1, you should be able to:
- [ ] Explain what a digital twin is
- [ ] Run the Python glucose simulator
- [ ] Classify glucose states from raw readings
- [ ] Generate realistic mock data
- [ ] Use Antigravity to write and debug TypeScript

---

## 🆘 If You Get Stuck

### Common Issues

**"Python command not found"**
- Ask Antigravity: "Help me install Python 3.10 on macOS"

**"TypeScript errors I don't understand"**
- Ask Antigravity: "Explain this TypeScript error: [paste error]"

**"Mock data doesn't look realistic"**
- Ask Antigravity: "Review my glucose data and suggest improvements to make it more realistic"

**"I don't understand the digital twin code"**
- Ask Antigravity: "Explain this function like I'm new to programming: [paste function]"

---

## 🎯 Next Week Preview

Week 2 will focus on:
- Creating plain-language messages for each state
- Building message templates for different audiences
- Preparing for LLM integration

**No mobile UI yet!** We're building the "brain" first. 🧠

---

## 💡 Pro Tips

1. **Save your Antigravity conversations** - You'll want to reference them later
2. **Commit to Git daily** - Even if code isn't perfect
3. **Take breaks** - Digital twin logic is complex!
4. **Ask "why" questions** - Don't just copy code, understand it
5. **Celebrate small wins** - Every function that works is progress! 🎉
