import sqlite3

conn = sqlite3.connect('db/coffee_shop.db')
c = conn.cursor()

# Buat baca tabel category sebelum nambahin product
c.execute("SELECT id, category_name FROM product_category")
category_map = {name: cid for cid, name in c.fetchall()}

# detail produk
products = [
        ("namaPR", 99999, "Condiment", "default.jpg", "Ini adalag tempat deskripsi produk."),
]

# Query Insert ke database
for name, price, cat_name, img, desc in products:
    cat_id = category_map[cat_name]
    c.execute('''
        INSERT INTO products (name, price, active, category_id, image_path, description)
        VALUES (?, ?, 1, ?, ?, ?)
    ''', (name, price, cat_id, img, desc))

conn.commit()
conn.close()

print("✅ Menu baru berhasil ditambahkan")