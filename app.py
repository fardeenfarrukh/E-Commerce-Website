from flask import Flask, render_template, request, redirect, url_for
import sqlite3
 
app = Flask(__name__)
 
def initialize_database():
    with sqlite3.connect("database.db") as connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS products(
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                image TEXT NOT NULL
            )
        ''')
        # Clear the table before inserting for demo purposes (remove in production)
        connection.execute("DELETE FROM products")
        connection.execute("INSERT INTO products(name, price, stock, image) VALUES ('Blank Shirt 1', 20.00, 10, 'images/product1.jpg')")
        connection.execute("INSERT INTO products(name, price, stock, image) VALUES ('Blank Shirt 2', 25.00, 10, 'images/product2.jpg')")
        connection.execute("INSERT INTO products(name, price, stock, image) VALUES ('Blank Shirt 3', 30.00, 10, 'images/product3.jpg')")
 
@app.route('/')
def display_products():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    product_list = cursor.fetchall()
    connection.close()
    return render_template('index.html', products=product_list)
 
@app.route('/buy/<int:product_id>', methods=['POST'])
def purchase_product(product_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE products SET stock = stock - 1 WHERE product_id = ?", (product_id,))
    connection.commit()
    connection.close()
    return redirect(url_for('display_products'))
 
if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
