# 🤖 Module: Agentic Workflows (The Guardian)

## Turning the AI into an Active Participant

**Objective**: Move beyond "Chatting" with data. Build an Agent that *watches* your data 24/7 and takes action (e.g., emailing family, booking doctors) when things go wrong.

---

### 🧠 Concept: Passive vs. Active

* **Passive AI (Chatbot)**: You ask a question, it gives an answer. It waits for you.
* **Active AI (Agent)**: It has a goal ("Keep glucose in range") and **Tools** (Email, Calendar, SMS). It acts on its own (within limits).

**The Magic Key: Function Calling**
Modern LLMs (OpenAI, Anthropic) have a feature called "Tool Use" or "Function Calling". You describe a Python function to the AI, and if the AI decides it needs that function, it will give you the *arguments* to run it.

---

### 🧪 Lab 1: The "Mom, I'm High" Alert

*Goal: If glucose spikes dangerously high while you are asleep, text a loved one.*

#### 1. The Tool Definition

You don't write the email text. You give the AI the *capability*.

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "send_emergency_sms",
            "description": "Sends an urgent text to a contact when glucose is dangerous.",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_name": {"type": "string"},
                    "message": {"type": "string", "description": "The urgent message."}
                },
                "required": ["contact_name", "message"]
            }
        }
    }
]
```

#### 2. The Prompt
>
> "You are The Guardian. Monitor the glucose reading. If it exceeds 250 mg/dL, immediately use `send_emergency_sms` to contact 'Mom'."

#### 3. The Result

The AI sees `255 mg/dL`. It does *not* reply with text. It replies with a **Function Call**:
`send_emergency_sms(contact_name="Mom", message="Alert: Glucose is 255. Please check on me.")`

---

### 📅 Lab 2: The "Doctor, I Need You" Scheduler

*Goal: Detect long-term burnout and handle the logistics of getting help.*

#### 1. The Tool

`find_appointment_slot(doctor_type: str, urgency: str)`

#### 2. The Logic (The Workflow)

You can chain these together using a **LangChain** or **swarms** framework:

1. **Analyzer Agent**: Reads the last 14 days of data.
    * *Finding*: "Time in Range is only 40%. Urgent."
2. **Logistics Agent**: Takes the finding.
    * *Action*: Calls `find_appointment_slot(doctor_type="Endocrinologist", urgency="High")`.

---

### 🛡️ Lab 3: The Control Room (Safety First)

*We don't want the AI booking surgery or texting your ex.*

**The Constitution (System Prompt):**
> "You are a helpful health assistant.
>
> 1. You **MUST** ask for user confirmation before sending any external message.
> 2. You **CANNOT** provide medical advice or change insulin dosages.
> 3. You **MUST** prioritize safety over convenience."

**Human-in-the-loop**:
When the AI wants to call `send_emergency_sms`, your code should pause and show a popup:
> "The Guardian wants to text Mom. Allow? [Yes] [No]"

---

### 🚀 Implementation Strategy

For this project, we recommend using **LangGraph** or **PydanticAI** to manage these workflows. They define the "Nodes" (Agents) and "Edges" (Logic) that control the flow.
