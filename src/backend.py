from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://petcare:password@localhost:5002/petcare'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to suppress warnings
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    __tablename__ = 'products'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Buyer Model
class Buyer(db.Model):
    __tablename__ = 'buyers'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='buyer', lazy=True)

# Order Model
class Order(db.Model):
    __tablename__ = 'orders'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref='orders')

# Home Route
@app.route('/')
def home():
    return "Welcome to the Marketplace API!", 200

# Product Routes
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_list = []

    for product in products:
        products_list.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price
        })

    return jsonify({'products': products_list}), 200

# Buyer Routes
@app.route('/buyer/register', methods=['POST'])
def register_buyer():
    data = request.get_json()

    if not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400

    new_buyer = Buyer(
        username=data['username'],
        email=data['email'],
        password=data['password']  # In production, hash the password!
    )

    try:
        db.session.add(new_buyer)
        db.session.commit()
        return jsonify({'message': 'Buyer registered successfully', 'buyer_id': new_buyer.id}), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': 'Username or email already exists'}), 400

@app.route('/buyer/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    if not all(key in data for key in ['buyer_id', 'product_id', 'quantity']):
        return jsonify({'error': 'Missing required fields'}), 400

    # Fetch the product to get the price
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    total_price = product.price * data['quantity']

    new_order = Order(
        buyer_id=data['buyer_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        total_price=total_price
    )

    try:
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully'}), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': 'Failed to create order'}), 400

@app.route('/buyer/orders/<int:buyer_id>', methods=['GET'])
def get_buyer_orders(buyer_id):
    orders = Order.query.filter_by(buyer_id=buyer_id).all()
    orders_list = []

    for order in orders:
        orders_list.append({
            'id': order.id,
            'product_id': order.product_id,
            'product_name': order.product.name,
            'quantity': order.quantity,
            'total_price': order.total_price,
            'status': order.status,
            'created_at': order.created_at
        })

    return jsonify({'orders': orders_list}), 200

@app.route('/buyer/profile/<int:buyer_id>', methods=['GET', 'PUT'])
def buyer_profile(buyer_id):
    buyer = Buyer.query.get_or_404(buyer_id)

    if request.method == 'GET':
        return jsonify({
            'username': buyer.username,
            'email': buyer.email,
            'created_at': buyer.created_at
        }), 200

    elif request.method == 'PUT':
        data = request.get_json()

        if 'username' in data:
            buyer.username = data['username']
        if 'email' in data:
            buyer.email = data['email']

        try:
            db.session.commit()
            return jsonify({'message': 'Profile updated successfully'}), 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'error': 'Failed to update profile'}), 400

@app.route('/shop')
def shop():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Add sample products if they don't exist
        if not Product.query.first():
            sample_products = [
                Product(name='Widget A', description='A useful widget.', price=19.99),
                Product(name='Gadget B', description='An amazing gadget.', price=29.99),
                Product(name='Thingamajig C', description='An essential thingamajig.', price=9.99),
            ]
            db.session.bulk_save_objects(sample_products)
            db.session.commit()

    app.run(debug=True)
