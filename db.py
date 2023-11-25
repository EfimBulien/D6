import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS Products
    (id INTEGER PRIMARY KEY, 
    name TEXT, description TEXT, 
    price REAL, category TEXT)
''')

conn.commit()

conn.close()
