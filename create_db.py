import sqlite3
import random

# Connect to the SQLite database. If it doesn't exist, it will be created.
conn = sqlite3.connect('stock_data.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Drop the table if it already exists
cursor.execute("DROP TABLE IF EXISTS STOCK_DATA")

# Create table as per requirement
sql = '''CREATE TABLE STOCK_DATA (
         id INTEGER PRIMARY KEY,
         description TEXT NOT NULL,
         quantity INTEGER NOT NULL
         )'''
cursor.execute(sql)

# List of famous books to use as descriptions
books = [
    "To Kill a Mockingbird",
    "1984",
    "The Great Gatsby",
    "One Hundred Years of Solitude",
    "A Passage to India",
    "Invisible Man",
    "Don Quixote",
    "Beloved",
    "Mrs. Dalloway",
    "Things Fall Apart"
]

# Insert 10 entries
for i in range(1, 11):
    description = books[i-1]  # Get book title from list
    quantity = random.randint(0, 15)  # Generate a random quantity between 0 and 15
    cursor.execute("INSERT INTO STOCK_DATA (id, description, quantity) VALUES (?, ?, ?)", (i, description, quantity))

print("10 entries added successfully")

# Commit your changes in the database
conn.commit()

# Close the connection
conn.close()
