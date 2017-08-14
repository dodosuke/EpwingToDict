import sqlite3

connect = sqlite3.connect("dictionary.db")
c = connect.cursor()
c.execute("SELECT * FROM Category")
print(c.fetchall())
