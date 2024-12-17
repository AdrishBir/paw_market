from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Add this line
from datetime import datetime
import os
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = os.urandom(24)  # To keep session data safe

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://petcare:password@localhost:5002/petcare'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Static File Configuration
app.static_folder = 'static'

# Models
# Update Product Model
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(200))
    age = db.Column(db.Integer)

    # Foreign key for Seller
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    
class Seller(db.Model):
    __tablename__ = 'sellers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    home_delivery = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with Product
    products = db.relationship('Product', backref='seller', lazy=True)

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
        seller = Seller.query.get(product.seller_id)
        return render_template('product_details.html', product=product, seller=seller)
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
            "image_url": product.image_url,
            "seller_id": product.seller_id  # Include seller_id in the response
        })
    else:
        return jsonify({"error": "Product not found"}), 404

# Seller Page to Add Pets for Adoption
@app.route('/list-pet', methods=['GET', 'POST'])
def list_pet():
    if request.method == 'POST':
        # Pet details
        name = request.form.get('name')
        age = request.form.get('age')
        description = request.form.get('description')
        image_url = request.form.get('image_url')

        # Seller details
        seller_name = request.form.get('seller_name')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        home_delivery = request.form.get('home_delivery') == 'on'

        if not all([name, age, description, image_url, seller_name, phone_number, address]):
            return "All fields are required", 400

        try:
            # Create new seller
            seller = Seller(
                name=seller_name,
                phone_number=phone_number,
                address=address,
                home_delivery=home_delivery
            )
            db.session.add(seller)
            db.session.flush()  # Flush to get the seller ID

            # Create new product linked to the seller
            new_pet = Product(
                name=name, 
                description=description, 
                age=int(age), 
                image_url=image_url, 
                price=0, 
                seller_id=seller.id
            )
            db.session.add(new_pet)
            db.session.commit()
            return redirect(url_for('shop_page'))
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}", 500

    return render_template('list_pet.html')

# API Endpoint to fetch seller details
# @app.route('/api/seller/<int:seller_id>')
# def api_seller_details(seller_id):
#     seller = Seller.query.get(seller_id)
#     if seller:
#         return jsonify({
#             "seller_name": seller.name,
#             "phone_number": seller.phone_number,
#             "address": seller.address,
#             "home_delivery": seller.home_delivery
#         })
#     else:
#         return jsonify({"error": "Seller not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create new tables with updated schema
    app.run(debug=True)