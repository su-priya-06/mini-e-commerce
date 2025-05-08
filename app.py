from flask import Flask, render_template, redirect, url_for, request, session, flash
import json

app = Flask(__name__)
app.secret_key = 'your-secret'

# Load products from JSON
with open('products.json') as f:
    products = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(product_id)
    session.modified = True
    flash("Item added to cart!")
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = []
    total = 0
    if 'cart' in session:
        for pid in session['cart']:
            for product in products:
                if product['id'] == pid:
                    cart_items.append(product)
                    total += product['price']
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return render_template('checkout.html')

# Optional Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['user'] = username
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
