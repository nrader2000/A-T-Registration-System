import sqlite3

#create db connection
connection = sqlite3.connect('database.db')

#create db.sql and all its tables to connection
with open('db.sql') as f:
    connection.executescript(f.read())

#add data to the db
cur = connection.cursor()
cur.execute("INSERT INTO Students ()")

#close the connection
connection.commit()
connection.close()