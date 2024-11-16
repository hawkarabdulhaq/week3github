import sqlite3

# Create a database and establish a connection
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table for storing Mandelbrot parameters
cursor.execute('''
CREATE TABLE IF NOT EXISTS parameters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    width INTEGER,
    height INTEGER,
    max_iter INTEGER
)
''')

# Insert sample parameters (default values for the Mandelbrot set)
cursor.execute('''
INSERT INTO parameters (width, height, max_iter) 
VALUES (800, 800, 100)
''')

# Commit changes and close the connection
conn.commit()
conn.close()
