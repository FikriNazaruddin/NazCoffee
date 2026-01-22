from flask import Blueprint, request, flash, render_template, redirect, url_for, session, g
import sqlite3

main = Blueprint('main', __name__)
DATABASE = 'db/coffee_shop.db'

# --- Database Helpers ---
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@main.teardown_app_request
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- Routes ---
@main.route('/')
def home():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()

        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            session['user_id'] = user['id']
            return redirect(url_for('main.home'))
        else:
            flash('Username atau password tidak valid!', 'danger')

    return render_template('login.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email')
        phone = request.form.get('phone')

        try:
            db = get_db()
            db.execute(
                'INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)',
                (username, password, email, phone)
            )
            db.commit()
            flash('Akun berhasil dibuat! Anda sekarang bisa login.', 'success')
            return redirect(url_for('main.login'))
        except sqlite3.IntegrityError:
            flash('Username telah dipakai, silahkan pakai yang lain.', 'danger')
        except Exception as e:
            flash(f'Error creating account: {str(e)}', 'danger')

    return render_template('signup.html')

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))

@main.route('/menu')
def menu():
    db = get_db()
    categories = db.execute("SELECT * FROM product_category").fetchall()

    category_products = {}
    for category in categories:
        products = db.execute(
            "SELECT * FROM products WHERE category_id = ?",
            (category['id'],)
        ).fetchall()
        category_products[category['category_name']] = products

    return render_template('menu.html', category_products=category_products)

@main.route('/order', methods=['GET', 'POST'])
def order():
    if not session.get('logged_in'):
        flash("Silakan Log In untuk melakukan order.", "danger")
        return redirect(url_for('main.login'))

    product_id = request.args.get('product_id', type=int)
    if not product_id:
        flash("Belum Memilih Produk.", "danger")
        return redirect(url_for('main.menu'))

    db = get_db()
    product = db.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    if not product:
        flash("Product tidak ditemukan.", "danger")
        return redirect(url_for('main.menu'))

    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        total_price = quantity * product['price']
        user_id = session['user_id']

        db.execute(
            "INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES (?, ?, ?, ?)",
            (user_id, product_id, quantity, total_price)
        )
        db.commit()
        flash("Order Berhasil!", "success")
        return redirect(url_for('main.my_orders'))

    return render_template('order.html', product=product)

@main.route('/my-orders')
def my_orders():
    if 'user_id' not in session:
        flash('Silakan Log In untuk melihat order anda.', "warning")
        return redirect(url_for('main.login'))

    db = get_db()
    orders = db.execute('''
        SELECT o.id, o.quantity, o.total_price, 
               p.name as product_name, p.image_path
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.user_id = ?
    ''', (session['user_id'],)).fetchall()

    return render_template('my_orders.html', orders=orders)

@main.route('/delete-order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    if not session.get('logged_in'):
        flash('Silakan Log In untuk menghapus Order.', 'warning')
        return redirect(url_for('main.login'))

    db = get_db()
    db.execute(
        "DELETE FROM orders WHERE id = ? AND user_id = ?",
        (order_id, session['user_id'])
    )
    db.commit()

    flash('Order berhasil dihapus!', 'warning')
    return redirect(url_for('main.my_orders'))

@main.route('/edit-order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    if not session.get('logged_in'):
        flash('Silakan log in untuk mengedit pesanan.', 'warning')
        return redirect(url_for('main.login'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT o.id, o.quantity, o.total_price, o.product_id,
               p.name as product_name, p.price, p.image_path, p.description
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.id = ? AND o.user_id = ?
    ''', (order_id, session['user_id']))
    
    order = cursor.fetchone()
    if not order:
        flash("Order tidak ditemukan atau tidak valid.", "danger")
        return redirect(url_for('main.my_orders'))

    if request.method == 'POST':
        new_quantity = int(request.form['quantity'])
        new_total_price = new_quantity * order['price']

        cursor.execute('''
            UPDATE orders
            SET quantity = ?, total_price = ?
            WHERE id = ? AND user_id = ?
        ''', (new_quantity, new_total_price, order_id, session['user_id']))
        db.commit()

        flash("Pesanan berhasil diperbarui!", "success")
        return redirect(url_for('main.my_orders'))

    return render_template('edit_order.html', order=order)


@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/products')
def products():
    return render_template('products.html')
