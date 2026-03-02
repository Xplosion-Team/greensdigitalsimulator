"""
Simulate Database Vibe Coding operations.
Uses SQLite to demonstrate CRUD (Create, Read, Update, Delete) 
without writing raw complex SQL.
"""
import sqlite3
from datetime import datetime

def vibe_db_demo():
    # 1. Connect (The 'Creation' Vibe)
    print("\n--- 'Vibe Coding' a Database ---")
    conn = sqlite3.connect(":memory:") # Using in-memory for the demo
    cursor = conn.cursor()
    
    # 2. Create Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS GlucoseReadings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value REAL,
        timestamp TEXT,
        source TEXT
    )
    ''')
    print("[SUCCESS] Table 'GlucoseReadings' created via AI-generated schema.")
    
    # 3. Create (Insert)
    now = datetime.now().isoformat()
    cursor.execute("INSERT INTO GlucoseReadings (value, timestamp, source) VALUES (?, ?, ?)", 
                   (125.5, now, "Simulation"))
    conn.commit()
    print(f"[SUCCESS] Data Inserted: 125.5 mg/dL at {now}")
    
    # 4. Read (Query)
    cursor.execute("SELECT * FROM GlucoseReadings")
    row = cursor.fetchone()
    print(f"[INFO] Data Retrieved: ID={row[0]}, Value={row[1]}, Source={row[3]}")
    
    conn.close()

if __name__ == "__main__":
    vibe_db_demo()
