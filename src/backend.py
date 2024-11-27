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

# Models
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(200))

class Buyer(db.Model):
    __tablename__ = 'buyers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # In production, hash the password!
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Home Page
@app.route('/')
def home_page():
    return render_template('home.html')
# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                # Handle form data if not JSON
                username = request.form.get('username')
                email = request.form.get('email') 
                password = request.form.get('password')
            else:
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')

            # Validate required fields
            if not all([username, email, password]):
                if request.is_json:
                    return jsonify({"error": "All fields are required"}), 400
                return "All fields are required", 400

            # Check if user already exists by username or email
            existing_user = Buyer.query.filter(
                (Buyer.email == email) | (Buyer.username == username)
            ).first()
            
            if existing_user:
                if existing_user.email == email:
                    if request.is_json:
                        return jsonify({"error": "Email already registered"}), 400
                    return "Email already registered", 400
                else:
                    if request.is_json:
                        return jsonify({"error": "Username already taken"}), 400
                    return "Username already taken", 400

            # Create new user
            new_user = Buyer(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            # Log the user in after registration
            session['buyer_id'] = new_user.id
            session['username'] = new_user.username
            
            if request.is_json:
                return jsonify({"message": "Registration successful"}), 200
            return redirect(url_for('shop_page'))

        except Exception as e:
            db.session.rollback()
            if request.is_json:
                return jsonify({"error": f"Registration failed: {str(e)}"}), 500
            return "Unable to register. Please try again.", 500

    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Validate user credentials
        buyer = Buyer.query.filter_by(email=email, password=password).first()
        if buyer:
            # Store buyer info in session
            session['buyer_id'] = buyer.id
            session['username'] = buyer.username
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials. Please try again."}), 401

    return render_template('login.html')  # A form for login

# Shop Page (Product List)
@app.route('/shop')
def shop_page():
    # Check if user is logged in
    if 'buyer_id' not in session:
        return redirect(url_for('login_page'))  # Redirect to login if not logged in

    # Fetch all products
    products = Product.query.all()
    return render_template('shop.html', products=products)  # Render product list

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)