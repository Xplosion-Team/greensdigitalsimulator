# 💾 Module: Database Vibe Coding

## Building a Memory for Your Digital Twin

**Objective**: Use "Vibe Coding" (Prompt-Driven Development) to add a database that remembers every glucose reading, meal, and prediction.

---

### 🌊 Concept: What is "Vibe Coding"?

Instead of memorizing SQL syntax or Python boilerplate, you act as the **Architect**. You tell the AI *what* you want, and it writes the *how*.

**The Stack:**

* **SQLite**: A lightweight database that lives in a single file (`greens.db`). No servers to manage.
* **SQLAlchemy**: The Python tool (ORM) that translates Python classes into SQL tables.

---

### 🏗️ Step 1: The Schema Prompt (The Blueprint)

*Goal: Create the tables to store our data.*

**Your Prompt to the AI:**
> "I need to add a database to my FastAPI app using SQLAlchemy and SQLite.
>
> Please create a file `api/database.py` with:
>
> 1. A `GlucoseReading` model with fields: `id` (int, primary key), `bg_value` (float), `timestamp` (datetime), and `note` (string, optional).
> 2. A function `init_db()` to create the tables if they don't exist.
> 3. A dependency `get_db` to use in my routes."

**What to look for in the code:**

* Does it import `Base` from `sqlalchemy.ext.declarative`?
* Does it have a `class GlucoseReading(Base):`?
* Does it create a file named `greens.db`?

---

### 🔌 Step 2: The CRUD Prompt (The Logic)

*Goal: Create the API routes to Create, Read, Update, and Delete data.*

**Your Prompt to the AI:**
> "Now, update `api/main.py`.
>
> 1. Add a POST route `/v1/readings` that accepts a JSON object (value, note) and saves it to the database.
> 2. Add a GET route `/v1/readings` that returns the last 24 hours of data.
> 3. Ensure validation using Pydantic models."

**Verification:**

* Run the server (`uvicorn api.main:app --reload`).
* Go to `http://localhost:8000/docs`.
* Try the "Try it out" button on the `POST /v1/readings` endpoint.

---

### 🔍 Step 3: The Verification (Trust but Verify)

*How do we know the data is actually there?*

**The "Vibe Check" Prompt:**
> "Write a small script called `examine_db.py` that connects to `greens.db` and prints out the last 5 rows added to the table, just so I can verify the data is safe."

**Run it:**

```bash
python examine_db.py
```

If you see your data printed in the terminal, **Success!** You have built a persistent memory.

---

### 🧠 Challenge: The "User" Layer

*Take it to the next level.*

**Prompt:**
> "Refactor the database models. Add a `User` table.
>
> 1. A User has many GlucoseReadings (One-to-Many relationship).
> 2. Update the API so that when I save a reading, I must provide a `user_id`."

---

### 🚀 Phase 4: Production Connect (Replit & Lovable)

*Connecting the wires across the cloud.*

#### 1. Replit Persistence

* **The Check**: SQLite saves data to a file (`greens.db`). In Replit, files are persistent.
* **The Trap**: If you see your data disappearing, check if `greens.db` is in `.gitignore`. It *should* be ignored by Git (for security), but Replit will keep the local file safe.

#### 2. Lovable Wiring

* **The Prompt to Lovable**:
    > "I have a new API endpoint: `POST https://[YOUR-REPL-URL].replit.app/v1/readings`.
    > Please update the 'Add Reading' button to send the JSON body `{ 'bg_value': 120, 'note': 'Lunch' }` to this URL."

#### 3. The CORS Check

* If Lovable says "Network Error" only on the POST request:
* **Go to `api/main.py`** and ensure your CORS settings allow the `POST` method (or `allow_methods=["*"]`).
