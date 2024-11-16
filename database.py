import sqlite3

# Debugging output
print("Starting database setup...")

# Create a new SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create a simple table to test the database creation
cursor.execute('''
CREATE TABLE IF NOT EXISTS parameters (
    id INTEGER PRIMARY KEY,
    name TEXT,
    value REAL
)
''')

# Insert some test data
cursor.execute("INSERT INTO parameters (name, value) VALUES ('param1', 3.14)")
cursor.execute("INSERT INTO parameters (name, value) VALUES ('param2', 2.71)")

# Commit and close
conn.commit()
conn.close()

# Debugging output
print("Database setup completed successfully.")
