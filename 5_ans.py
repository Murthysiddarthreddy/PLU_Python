# # 5. Movie Recommendation System
# ### Problem Statement
# A streaming platform stores movie information.
# Each movie contains
# * Movie ID
# * Title
# * Genre
# * Rating
# * Watch Count
# ### Requirements
# 1. Fetch all movies.
# 2. Sort movies based on Rating.
# 3. Search a movie using Movie ID.
# 4. Display Top 10 highest-rated movies.
# 5. Display the most watched movie in every genre.
# ### Concepts
# * Sorting
# * Searching
# * Dictionaries
# * SQL GROUP BY
import sqlite3

conn = sqlite3.connect("movies.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS movies")
cur.execute("CREATE TABLE movies(id INTEGER PRIMARY KEY,title TEXT,genre TEXT,rating REAL,watchcount INTEGER)")

data=[(1,"Inception","Sci-Fi",9.0,500),
      (2,"Avatar","Sci-Fi",8.5,700),
      (3,"Titanic","Romance",8.8,650),
      (4,"Joker","Drama",9.2,550),
      (5,"KGF","Action",8.9,800),
      (6,"Pushpa","Action",8.4,750)]

cur.executemany("INSERT INTO movies VALUES(?,?,?,?,?)",data)
conn.commit()

cur.execute("SELECT * FROM movies")
rows=cur.fetchall()

print("Sorted by Rating")
rows.sort(key=lambda x:x[3],reverse=True)
for i in rows:
    print(i)

def binary(a,key):
    l,h=0,len(a)-1
    while l<=h:
        m=(l+h)//2
        if a[m][0]==key:return a[m]
        elif a[m][0]<key:l=m+1
        else:h=m-1
    return None

rows.sort(key=lambda x:x[0])
x=int(input("Enter Movie ID: "))
print("Movie:",binary(rows,x))

print("\nTop 10 Rated Movies")
rows.sort(key=lambda x:x[3],reverse=True)
for i in rows[:10]:
    print(i)

print("\nMost Watched Movie in Each Genre")
cur.execute("SELECT genre,MAX(watchcount) FROM movies GROUP BY genre")
d={}
for g,w in cur.fetchall():
    d[g]=w
print(d)
conn.close()
