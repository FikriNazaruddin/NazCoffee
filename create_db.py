import sqlite3
import os

# Make sure the 'db' folder exists
os.makedirs('db', exist_ok=True)

# Connect to the SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('db/coffee_shop.db')
c = conn.cursor()

# Buat tabel users
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    phone TEXT
)
''')

# Buat tabel product_category
c.execute('''
CREATE TABLE IF NOT EXISTS product_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
)
''')

# Buat tabel products
c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    active INTEGER NOT NULL CHECK (active IN (0, 1)),
    category_id INTEGER,
    image_path TEXT,
    FOREIGN KEY (category_id) REFERENCES product_category(id)
)
''')

# Buat tabel orders
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    total_price REAL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
''')

# Commit changes dan close connection
conn.commit()
conn.close()

print("✅ Database and all tables created successfully, including image_path in products table.")
