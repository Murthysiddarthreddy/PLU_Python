# # 2. Hospital Patient Queue Management
# ### Problem Statement
# A hospital stores patient details in SQLite.
# Each patient has:
# * Patient ID
# * Name
# * Age
# * Priority Level
# ### Requirements
# 1. Fetch all patients.
# 2. Create a **Priority Queue** based on Priority Level.
# 3. Attend patients in order of priority.
# 4. After attending a patient, update the database.
# 5. Display the remaining patients.
# ### Concepts
# * SQLite
# * Priority Queue
# * UPDATE Query
# * Heap/Priority Queue

import sqlite3
import heapq

conn = sqlite3.connect("hospital.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS patients")

cur.execute("""
CREATE TABLE patients(
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    priority INTEGER,
    status TEXT
)
""")

data = [
    (101, "Rahul", 35, 3, "Waiting"),
    (102, "Anjali", 28, 1, "Waiting"),
    (103, "Rohan", 50, 2, "Waiting"),
    (104, "Priya", 40, 4, "Waiting"),
    (105, "Amit", 60, 1, "Waiting")
]

cur.executemany("INSERT INTO patients VALUES(?,?,?,?,?)", data)
conn.commit()

cur.execute("SELECT * FROM patients WHERE status='Waiting'")
rows = cur.fetchall()

pq = []
for i in rows:
    heapq.heappush(pq, (i[3], i))

patient = heapq.heappop(pq)[1]

print("Attending Patient")
print(patient)

cur.execute("UPDATE patients SET status='Attended' WHERE id=?", (patient[0],))
conn.commit()

print("\nRemaining Patients")
cur.execute("SELECT * FROM patients WHERE status='Waiting'")
for i in cur.fetchall():
    print(i)

conn.close()