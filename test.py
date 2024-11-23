import unittest
from basic import app, db, Buyer, Order
import json

class TestBuyerRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_buyer_orders(self):
        # Create test buyer
        buyer = Buyer(username='testbuyer', email='test@test.com')
        db.session.add(buyer)
        db.session.commit()

        # Create test order
        order = Order(buyer_id=buyer.id, product_id=1, quantity=2, total_price=20.0, status='pending')
        db.session.add(order)
        db.session.commit()

        # Test getting orders
        response = self.app.get(f'/buyer/orders/{buyer.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['orders']), 1)
        self.assertEqual(data['orders'][0]['product_id'], 1)
        self.assertEqual(data['orders'][0]['quantity'], 2)

    def test_get_buyer_profile(self):
        # Create test buyer
        buyer = Buyer(username='testbuyer', email='test@test.com')
        db.session.add(buyer)
        db.session.commit()

        # Test getting profile
        response = self.app.get(f'/buyer/profile/{buyer.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'testbuyer')
        self.assertEqual(data['email'], 'test@test.com')

    def test_update_buyer_profile(self):
        # Create test buyer
        buyer = Buyer(username='testbuyer', email='test@test.com')
        db.session.add(buyer)
        db.session.commit()

        # Test updating profile
        update_data = {
            'username': 'newusername',
            'email': 'newemail@test.com'
        }
        response = self.app.put(
            f'/buyer/profile/{buyer.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # Verify update
        buyer = Buyer.query.get(buyer.id)
        self.assertEqual(buyer.username, 'newusername')
        self.assertEqual(buyer.email, 'newemail@test.com')

if __name__ == '__main__':
    unittest.main()
