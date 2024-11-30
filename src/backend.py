from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # To keep session data safe

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://petcare:password@localhost:5002/petcare'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Static File Configuration
app.static_folder = 'static'

# Models
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(200))
    age = db.Column(db.Integer)

class Buyer(db.Model):
    __tablename__ = 'buyers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Home Page
@app.route('/')
def home_page():
    return render_template('home.html')

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        data = request.form if not request.is_json else request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return jsonify({"error": "All fields are required"}), 400

        existing_user = Buyer.query.filter(
            (Buyer.email == email) | (Buyer.username == username)
        ).first()

        if existing_user:
            return jsonify({"error": "Username or Email already exists"}), 400

        new_user = Buyer(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['buyer_id'] = new_user.id
        session['username'] = new_user.username

        return jsonify({"message": "Registration successful"}), 200

    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        data = request.form if not request.is_json else request.get_json()
        email = data.get('email')
        password = data.get('password')

        buyer = Buyer.query.filter_by(email=email, password=password).first()
        if buyer:
            session['buyer_id'] = buyer.id
            session['username'] = buyer.username
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    return render_template('login.html')

# Shop Page (Product List)
@app.route('/shop')
def shop_page():
    if 'buyer_id' not in session:
        return redirect(url_for('login_page'))

    products = Product.query.all()
    return render_template('shop.html', products=products)

# Product Details Page
@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return render_template('product_details.html', product=product)
    else:
        return "Product not found", 404

# API Product Details Endpoint
@app.route('/api/product/<int:product_id>')
def api_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "age": product.age,
            "description": product.description,
            "price": product.price,
            "image_url": product.image_url
        })
    else:
        return jsonify({"error": "Product not found"}), 404

# Seller Page to Add Pets for Adoption
@app.route('/list-pet', methods=['GET', 'POST'])
def list_pet():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        description = request.form.get('description')
        image_url = request.form.get('image_url')

        if not all([name, age, description, image_url]):
            return "All fields are required", 400

        try:
            new_pet = Product(name=name, description=description, age=int(age), image_url=image_url, price=0)
            db.session.add(new_pet)
            db.session.commit()
            return redirect(url_for('shop_page'))
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}", 500

    return render_template('list_pet.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)