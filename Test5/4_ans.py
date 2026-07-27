# # 4. College Placement Portal
# ### Problem Statement
# A college stores student records in SQLite.
# Each student contains:
# * Roll Number
# * Name
# * CGPA
# * Skills
# * Placement Status
# ### Requirements
# 1. Retrieve all students.
# 2. Sort students by CGPA using **Heap Sort**.
# 3. Search students by Roll Number.
# 4. Display students eligible for placements (CGPA > 7.5).
# 5. Update placement status after selection.
# ### Concepts
# * Heap
# * Heap Sort
# * Binary Search
# * SQL UPDATE

import sqlite3, heapq

conn = sqlite3.connect("college.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS students")
cur.execute("CREATE TABLE students(roll INTEGER PRIMARY KEY,name TEXT,cgpa REAL,skills TEXT,status TEXT)")

data = [(1,"Rahul",8.5,"Python","Not Placed"),
        (2,"Anjali",7.2,"Java","Not Placed"),
        (3,"Rohan",9.1,"C++","Not Placed"),
        (4,"Priya",8.0,"Python,SQL","Not Placed"),
        (5,"Amit",6.9,"C","Not Placed")]

cur.executemany("INSERT INTO students VALUES(?,?,?,?,?)", data)
conn.commit()

cur.execute("SELECT * FROM students")
rows = cur.fetchall()

heap = []
for i in rows:
    heapq.heappush(heap, (i[2], i))

print("Students Sorted by CGPA")
sorted_rows = []
while heap:
    x = heapq.heappop(heap)[1]
    sorted_rows.append(x)
    print(x)

rows.sort(key=lambda x: x[0])

def binary(a, key):
    l, h = 0, len(a)-1
    while l <= h:
        m = (l+h)//2
        if a[m][0] == key: return a[m]
        elif a[m][0] < key: l = m+1
        else: h = m-1
    return None

r = int(input("Enter Roll Number: "))
print("Student:", binary(rows, r))

print("\nEligible Students")
for i in rows:
    if i[2] > 7.5:
        print(i)

cur.execute("UPDATE students SET status='Placed' WHERE roll=103")
conn.commit()

print("\nUpdated Records")
cur.execute("SELECT * FROM students")
for i in cur.fetchall():
    print(i)

conn.close()
