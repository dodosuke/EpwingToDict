import sqlite3

connect = sqlite3.connect("dictionary.db")
c = connect.cursor()
c.execute("SELECT * FROM Meaning order by id desc limit 5")
print(c.fetchall())
