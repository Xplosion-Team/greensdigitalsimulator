# Greens Health Digital Twin - Project Structure

This document outlines the recommended folder structure for the glucose digital twin mobile interface project.

---

## 📁 Current Structure

```
/Users/kehlinswain/Documents/GitHub/greensdigitalsimulator/
├── src/                          # Python digital twin engine (existing)
│   └── t1dsim_ai/
│       ├── individual_model.py   # Core glucose-insulin model
│       ├── population_model.py   # Multi-patient modeling
│       ├── create_scenarios.py   # Scenario generation
│       └── options.py            # Configuration
│
├── example/                      # Python examples & demos (existing)
│   ├── runDigitalTwin.py
│   ├── interactiveDigitalTwin.py
│   ├── voice_module.py
│   └── ...
│
├── mobile-interface/             # NEW: Mobile app (TypeScript/React Native)
│   ├── logic/                    # Business logic (no UI)
│   │   ├── glucoseStates.ts      # State classification
│   │   ├── messageTemplates.ts   # Plain-language messages
│   │   ├── stateEngine.ts        # Full processing pipeline
│   │   ├── mockGlucoseData.ts    # Data generator
│   │   └── llmPromptBuilder.ts   # LLM integration prep
│   │
│   ├── data/                     # Mock & test data
│   │   └── mockGlucoseData.json  # 24hr glucose readings
│   │
│   ├── greens-glucose-twin/      # Expo React Native app
│   │   ├── App.tsx               # Main app entry
│   │   ├── app.json              # Expo config
│   │   ├── package.json          # Dependencies
│   │   │
│   │   ├── screens/              # UI screens
│   │   │   ├── GlucoseStatusScreen.tsx
│   │   │   ├── HistoryScreen.tsx
│   │   │   └── SettingsScreen.tsx
│   │   │
│   │   ├── components/           # Reusable UI components
│   │   │   ├── StateBadge.tsx
│   │   │   ├── TrendArrow.tsx
│   │   │   ├── MessageCard.tsx
│   │   │   └── VoiceButton.tsx
│   │   │
│   │   ├── services/             # API & data services
│   │   │   ├── glucoseService.ts
│   │   │   ├── voiceService.ts
│   │   │   └── apiClient.ts
│   │   │
│   │   └── assets/               # Images, fonts, etc.
│   │
│   └── README.md                 # Mobile interface docs
│
├── api/                          # NEW: Python API (Flask/FastAPI)
│   ├── main.py                   # API server
│   ├── routes/
│   │   ├── predict.py            # Glucose prediction endpoint
│   │   └── scenarios.py          # What-if scenarios
│   └── requirements.txt
│
├── docs/                         # Project documentation
│   ├── architecture.md
│   ├── api-spec.md
│   └── deployment.md
│
├── .venv/                        # Python virtual environment
├── pyproject.toml
├── requirments.txt
└── README.md
```

---

## 🗂 Directory Descriptions

### `/src/t1dsim_ai/` - Digital Twin Engine (Python)
**Purpose**: Core glucose-insulin simulation model  
**Tech**: Python, NumPy, SciPy  
**Owner**: Kehlin + Dr. Mosquera  
**Status**: ✅ Existing

**Key Files**:
- `individual_model.py` - Patient-specific glucose dynamics
- `population_model.py` - Multi-patient cohort modeling
- `create_scenarios.py` - Meal/activity scenario generation

---

### `/mobile-interface/logic/` - Business Logic (TypeScript)
**Purpose**: State classification, message generation, data processing  
**Tech**: TypeScript (Node.js)  
**Owner**: Mirna  
**Status**: 🚧 Week 1-2 deliverable

**Key Files**:
- `glucoseStates.ts` - State machine (Stable, Trending High, etc.)
- `messageTemplates.ts` - Plain-language explanations
- `stateEngine.ts` - Full pipeline (data → state → message)
- `llmPromptBuilder.ts` - LLM integration prep

**Why separate from UI?**
- Logic can be tested independently
- Same logic used for app, SMS, voice
- Easier to maintain and debug

---

### `/mobile-interface/greens-glucose-twin/` - Mobile App (React Native)
**Purpose**: User-facing mobile interface  
**Tech**: Expo, React Native, TypeScript  
**Owner**: Mirna  
**Status**: 🚧 Week 3-4 deliverable

**Key Directories**:
- `screens/` - Full-page views (Status, History, Settings)
- `components/` - Reusable UI pieces (badges, buttons, cards)
- `services/` - API calls, voice, data fetching
- `assets/` - Images, icons, fonts

**Design Principles**:
- Large fonts (18pt+)
- High contrast (WCAG AAA)
- Simple navigation
- Voice-first accessibility

---

### `/api/` - Python API Server
**Purpose**: Bridge between Python digital twin and mobile app  
**Tech**: Flask or FastAPI  
**Owner**: Mirna (Week 5)  
**Status**: 📅 Future

**Endpoints** (planned):
- `POST /predict` - Get glucose predictions
- `POST /scenarios` - Run what-if scenarios
- `GET /state` - Current glucose state

**Why needed?**
- Mobile app (JavaScript) can't run Python code directly
- API allows real-time predictions
- Enables future web interface

---

## 🔄 Data Flow

```
┌─────────────────┐
│  CGM Device     │  (Future: Dexcom API)
│  (Glucose Data) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Mobile App     │  ← User sees this
│  (React Native) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  State Engine   │  ← Classifies glucose state
│  (TypeScript)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Message Layer  │  ← Generates plain language
│  (Templates)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Python API     │  ← Runs predictions (optional)
│  (Flask)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Digital Twin   │  ← Glucose-insulin model
│  (Python)       │
└─────────────────┘
```

---

## 📦 Technology Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Digital Twin** | Python, NumPy | Glucose-insulin simulation |
| **Business Logic** | TypeScript (Node) | State classification, messages |
| **Mobile UI** | Expo, React Native | iOS/Android interface |
| **API Server** | Flask/FastAPI | Python ↔ Mobile bridge |
| **Voice** | expo-speech | Text-to-speech, voice input |
| **LLM** | OpenAI/Anthropic API | Personalized messages |
| **Data** | JSON, SQLite (future) | Mock data, user preferences |

---

## 🎯 Week-by-Week Build Order

### Week 1: `/mobile-interface/logic/`
- State classification
- Mock data generation
- No UI yet

### Week 2: `/mobile-interface/logic/`
- Message templates
- LLM prompt builder
- Still no UI

### Week 3-4: `/mobile-interface/greens-glucose-twin/`
- Expo app setup
- Basic screens
- Voice integration

### Week 5-6: `/api/`
- Python API server
- Connect to digital twin
- Real predictions

---

## 🚀 Getting Started (For Mirna)

### Week 1 Setup
```bash
# Navigate to project
cd /Users/kehlinswain/Documents/GitHub/greensdigitalsimulator

# Create mobile interface directory
mkdir -p mobile-interface/logic
mkdir -p mobile-interface/data

# Initialize TypeScript (if needed)
cd mobile-interface
npm init -y
npm install typescript @types/node --save-dev
npx tsc --init
```

### Week 3 Setup (Expo)
```bash
# Inside mobile-interface/
npx create-expo-app greens-glucose-twin --template expo-template-blank-typescript
cd greens-glucose-twin
npm start
```

---

## 📝 File Naming Conventions

- **TypeScript**: camelCase for files (`glucoseStates.ts`)
- **React Components**: PascalCase (`GlucoseStatusScreen.tsx`)
- **Python**: snake_case (`individual_model.py`)
- **Data files**: lowercase with hyphens (`mock-glucose-data.json`)

---

## 🔐 What NOT to Commit (`.gitignore`)

```
# Dependencies
node_modules/
.venv/

# Build outputs
dist/
build/
*.pyc
__pycache__/

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

---

## 📚 Next Steps

1. **Week 1**: Build `/mobile-interface/logic/` (no UI)
2. **Week 2**: Add message templates
3. **Week 3**: Initialize Expo app
4. **Week 4**: Build first screen
5. **Week 5**: Create Python API
6. **Week 6**: Connect everything

---

This structure keeps concerns separated while allowing easy integration. The digital twin "brain" (Python) stays independent, and the mobile interface (TypeScript/React Native) can evolve without breaking the core model.
