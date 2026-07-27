# # 6. Food Delivery Route Optimizer
# ### Problem Statement
# A food delivery company stores restaurants and delivery locations.
# Database tables:
# Restaurant
# Delivery
# Orders
# ### Requirements
# 1. Fetch all pending orders.
# 2. Build a **Graph** representing restaurants and delivery areas.
# 3. Find the shortest delivery path using **BFS**.
# 4. Display delivery order sequence.
# 5. Mark completed deliveries in SQLite.
# ### Concepts
# * Graph
# * BFS
# * SQL JOIN
# * UPDATE
# ---
import sqlite3
from collections import deque

conn = sqlite3.connect("food.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Restaurant(id INTEGER PRIMARY KEY,name TEXT,area TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS Delivery(id INTEGER PRIMARY KEY,area1 TEXT,area2 TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS Orders(id INTEGER PRIMARY KEY,restaurant_id INTEGER,destination TEXT,status TEXT)")

cur.execute("DELETE FROM Restaurant")
cur.execute("DELETE FROM Delivery")
cur.execute("DELETE FROM Orders")

cur.executemany("INSERT INTO Restaurant VALUES(?,?,?)",
[(1,"Pizza Hut","A"),(2,"KFC","B")])

cur.executemany("INSERT INTO Delivery VALUES(?,?,?)",
[(1,"A","B"),(2,"B","C"),(3,"C","D")])

cur.executemany("INSERT INTO Orders VALUES(?,?,?,?)",
[(101,1,"D","Pending"),(102,2,"C","Pending")])

graph = {}
for a, b in cur.execute("SELECT area1,area2 FROM Delivery"):
    graph.setdefault(a, []).append(b)
    graph.setdefault(b, []).append(a)

def bfs(start, end):
    q = deque([(start, [start])])
    vis = {start}
    while q:
        node, path = q.popleft()
        if node == end:
            return path
        for x in graph.get(node, []):
            if x not in vis:
                vis.add(x)
                q.append((x, path + [x]))

rows = cur.execute("""
SELECT Orders.id,Restaurant.area,Orders.destination
FROM Orders
JOIN Restaurant ON Orders.restaurant_id=Restaurant.id
WHERE Orders.status='Pending'
""").fetchall()

for oid, start, end in rows:
    path = bfs(start, end)
    print("Order:", oid)
    print("Route:", " -> ".join(path))
    cur.execute("UPDATE Orders SET status='Completed' WHERE id=?", (oid,))

conn.commit()
print("\nUpdated Orders:")
for r in cur.execute("SELECT * FROM Orders"):
    print(r)

conn.close()