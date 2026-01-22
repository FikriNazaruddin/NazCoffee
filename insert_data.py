import sqlite3

conn = sqlite3.connect('db/coffee_shop.db')
c = conn.cursor()

try:
    c.execute("ALTER TABLE products ADD COLUMN description TEXT")
except sqlite3.OperationalError:
    pass

users = [
    ("user1", "user12345", "user1@gmail.com", "081234567891"),
    ("user2", "user12345", "user2@gmail.com", "082134567892"),
    ("user3", "user12345", "user3@gmail.com", "083134567893"),
]
c.executemany("INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)", users)

# --- CATEGORIES ---
categories = ["Coffee", "Non-Coffee", "Main Dish", "Condiment"]
for cat in categories:
    c.execute("INSERT OR IGNORE INTO product_category (category_name) VALUES (?)", (cat,))

c.execute("SELECT id, category_name FROM product_category")
category_map = {name: cid for cid, name in c.fetchall()}

products = [
    # Coffee
    ("Espresso", 10000, "Coffee", "espresso.jpg", "Espresso kuat dan pekat untuk dorongan energi cepat."),
    ("Caffe Latte", 15000, "Coffee", "caffe_latte.jpg", "Kopi espresso lembut berpadu dengan susu hangat."),
    ("Caramel Macchiato", 17000, "Coffee", "caramel_macchiato.jpg", "Rasa manis karamel yang menggoda dengan espresso."),
    ("Smoked Milk-Aren", 20000, "Coffee", "smoked_milk_aren.jpg", "Susu asap unik dipadu dengan gula aren tradisional."),
    ("Spiced Affogato", 20000, "Coffee", "spiced_affogato.jpg", "Espresso panas disajikan di atas es krim rempah."),
    ("Pandan Cold-Brew", 23000, "Coffee", "pandan_cold_brew.jpg", "Cold brew segar dengan aroma khas pandan."),

    # Non-Coffee
    ("Matcha Latte", 15000, "Non-Coffee", "matcha_latte.jpg", "Matcha pilihan dengan susu lembut yang menyegarkan."),
    ("Chocolate Hazelnut", 20000, "Non-Coffee", "chocolate_hazelnut.jpg", "Cokelat kaya rasa dengan sentuhan kacang hazelnut."),
    ("Berry Sparkle", 20000, "Non-Coffee", "berry_sparkle.jpg", "Minuman soda buah beri segar yang menyegarkan."),
    ("Taro Milk Cheese", 17000, "Non-Coffee", "taro_milk_cheese.jpg", "Taro manis berpadu keju lembut yang nikmat."),

    # Main Dish
    ("Nasi Ayam Sambal Matah", 20000, "Main Dish", "nasi_ayam_sambal_matah.jpg", "Nasi ayam gurih dengan sambal matah khas Bali."),
    ("Teriyaki Rice Bowl", 23000, "Main Dish", "teriyaki_rice_bowl.jpg", "Nasi ayam dengan saus teriyaki manis gurih."),
    ("Chicken Mushroom Rice Bowl", 25000, "Main Dish", "chicken_mushroom.jpg", "Ayam empuk dalam saus jamur krim yang lezat."),
    ("Sambal Korek Rice Bowl", 23000, "Main Dish", "sambal_korek.jpg", "Nasi hangat dengan ayam dan sambal korek pedas."),

    # Condiment
    ("French Fries", 10000, "Condiment", "french_fries.jpg", "Kentang goreng renyah dengan bumbu spesial."),
    ("Chicken Wings", 18000, "Condiment", "chicken_wings.jpg", "Sayap ayam gurih dibalut saus khas kami."),
    ("Onion Rings", 15000, "Condiment", "onion_rings.jpg", "Cincin bawang goreng renyah dan menggoda."),
    ("Sosis Asam Manis", 10000, "Condiment", "sosis_asam_manis.jpg", "Sosis goreng disiram saus asam manis lezat."),
]

for name, price, cat_name, img, desc in products:
    cat_id = category_map[cat_name]
    c.execute('''
        INSERT INTO products (name, price, active, category_id, image_path, description)
        VALUES (?, ?, 1, ?, ?, ?)
    ''', (name, price, cat_id, img, desc))

# Commit dan close
conn.commit()
conn.close()

print("✅ Semua data sample berhasil dimasukkan.")
