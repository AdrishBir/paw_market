import unittest
from src.backend import app, db, Product, Buyer, Order

class MarketplaceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

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

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_choose_product_place_order(self):
        # Register a new buyer
        response = self.app.post('/buyer/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 201)

        # Get the list of products
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        products = response.get_json()['products']
        self.assertGreater(len(products), 0)

        # Choose the first product
        product_id = products[0]['id']

        # Place an order for the chosen product
        response = self.app.post('/orders', json={
            'buyer_id': 1,
            'product_id': product_id,
            'quantity': 1,
            'total_price': products[0]['price']
        })
        self.assertEqual(response.status_code, 201)

        # Log out (for simplicity, we assume logging out is just ending the session)
        # In a real application, this might involve token invalidation or session destruction

if __name__ == '__main__':
    unittest.main()
