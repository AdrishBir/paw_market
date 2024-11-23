from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
db = SQLAlchemy(app)


@app.route('/')
def home():
    return "Welcome to the Marketplace API!", 200

# Buyer Model
class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='buyer', lazy=True)

# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
        return jsonify({'message': 'Buyer registered successfully'}), 201
    except:
        return jsonify({'error': 'Username or email already exists'}), 400

@app.route('/buyer/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    if not all(key in data for key in ['buyer_id', 'product_id', 'quantity', 'total_price']):
        return jsonify({'error': 'Missing required fields'}), 400
        
    new_order = Order(
        buyer_id=data['buyer_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        total_price=data['total_price']
    )
    
    try:
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully'}), 201
    except:
        return jsonify({'error': 'Failed to create order'}), 400

@app.route('/buyer/orders/<int:buyer_id>', methods=['GET'])
def get_buyer_orders(buyer_id):
    orders = Order.query.filter_by(buyer_id=buyer_id).all()
    orders_list = []
    
    for order in orders:
        orders_list.append({
            'id': order.id,
            'product_id': order.product_id,
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
        except:
            return jsonify({'error': 'Failed to update profile'}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
