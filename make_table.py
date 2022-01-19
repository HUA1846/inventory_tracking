import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = """
    CREATE TABLE items (id int, category text, name text, price real, unit text)
"""

cursor.execute(create_table)

insert_query = "INSERT INTO items (category, name, price, unit) VALUES (?, ?, ?, ?)"

items = [
    ('fruits', 'apple', 0.99, 'lb'),
    ('fruits', 'orange', 2.99, 'lb'),
    ('fruits', 'blueberry', 7.99, '8oz'),
    ('dairy', 'whole milk', 2.19, 'gallon'),
    ('vegetable', 'spinach', 3.19, '10oz')
]

cursor.executemany(insert_query, items)

connection.commit()
connection.close()