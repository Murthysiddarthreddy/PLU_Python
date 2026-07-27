# # 3. Online Banking Transaction Analyzer
# ### Problem Statement
# A bank stores transactions in SQLite.
# Each transaction contains:
# * Transaction ID
# * Account Number
# * Amount
# * Date
# * Type (Credit/Debit)
# ### Requirements
# 1. Retrieve all transactions.
# 2. Sort them by amount using **Quick Sort**.
# 3. Search transactions using Transaction ID.
# 4. Calculate total credits and debits.
# 5. Display the top 5 highest-value transactions.
# ### Concepts
# * SQL
# * Quick Sort
# * Binary Search
# * Aggregation

import sqlite3

conn = sqlite3.connect("bank.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS trans(id INTEGER PRIMARY KEY, acc TEXT, amount REAL, type TEXT)")
cur.execute("SELECT COUNT(*) FROM trans")
if cur.fetchone()[0] == 0:
    data = [(101,"A101",5000,"Credit"),(102,"A102",2500,"Debit"),
            (103,"A103",12000,"Credit"),(104,"A104",7000,"Debit"),
            (105,"A105",15000,"Credit"),(106,"A106",3000,"Debit")]
    cur.executemany("INSERT INTO trans VALUES(?,?,?,?)", data)
    conn.commit()

cur.execute("SELECT * FROM trans")
rows = cur.fetchall()

def quick(arr):
    if len(arr) <= 1:
        return arr
    p = arr[0]
    left = [x for x in arr[1:] if x[2] <= p[2]]
    right = [x for x in arr[1:] if x[2] > p[2]]
    return quick(left) + [p] + quick(right)

def binary(arr, key):
    l, h = 0, len(arr)-1
    while l <= h:
        m = (l+h)//2
        if arr[m][0] == key:
            return arr[m]
        elif arr[m][0] < key:
            l = m+1
        else:
            h = m-1
    return None

print("Sorted by Amount:")
for i in quick(rows):
    print(i)

rows = sorted(rows)
x = int(input("Enter Transaction ID: "))
print("Found:", binary(rows, x))

credit = sum(i[2] for i in rows if i[3] == "Credit")
debit = sum(i[2] for i in rows if i[3] == "Debit")
print("Total Credit:", credit)
print("Total Debit:", debit)

print("Top 5 Transactions:")
for i in sorted(rows, key=lambda x: x[2], reverse=True)[:5]:
    print(i)
conn.close()