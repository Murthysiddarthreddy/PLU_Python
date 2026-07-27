# # 1. Smart Inventory Management System
# ### Problem Statement
# An e-commerce warehouse stores product information in an SQLite database.
# Each product has:
# * Product ID
# * Product Name
# * Category
# * Quantity
# * Price
# ### Requirements
# 1. Fetch all products from the SQLite database.
# 2. Store them in Python objects.
# 3. Sort the products based on quantity using **Merge Sort**.
# 4. Allow the manager to search for a Product ID using **Binary Search**.
# 5. Display the complete product details.
# 6. Display products whose stock is below 10.
# ### Concepts
# * SQLite
# * Python Classes
# * Merge Sort
# * Binary Search
# * SQL SELECT

import sqlite3

conn = sqlite3.connect("inventory.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY,name TEXT,category TEXT,qty INTEGER,price REAL)")
cur.execute("SELECT COUNT(*) FROM products")
if cur.fetchone()[0] == 0:
    data=[(101,"Laptop","Electronics",15,55000),
          (102,"Mouse","Electronics",8,500),
          (103,"Keyboard","Electronics",12,1200),
          (104,"Chair","Furniture",5,3500),
          (105,"Table","Furniture",20,7000)]
    cur.executemany("INSERT INTO products VALUES(?,?,?,?,?)",data)
conn.commit()

cur.execute("SELECT * FROM products")
rows=cur.fetchall()

def merge(a):
    if len(a)<=1:return a
    m=len(a)//2
    l=merge(a[:m]);r=merge(a[m:]);res=[]
    while l and r:
        res.append(l.pop(0) if l[0][3]<r[0][3] else r.pop(0))
    return res+l+r

def binary(a,key):
    l,h=0,len(a)-1
    while l<=h:
        m=(l+h)//2
        if a[m][0]==key:return a[m]
        elif a[m][0]<key:l=m+1
        else:h=m-1
    return None

print("Sorted by Quantity")
for i in merge(rows):
    print(i)

rows.sort(key=lambda x:x[0])
x=int(input("Enter Product ID: "))
print(binary(rows,x))

print("Low Stock Products")
for i in rows:
    if i[3]<10:
        print(i)

conn.close()