import unittest
# from unittest.mock import patch
from server import app
# # from mongomock import MongoClient
#
# from mongoengine import connect, disconnect
import mongomock
# from pymongo import MongoClient

class MongoTests(unittest.TestCase):

    def test__can_create_db_without_path(self):
        self.assertIsNotNone(mongomock.MongoClient())

    def test__can_create_db_with_path(self):
        self.assertIsNotNone(mongomock.MongoClient('mongodb://localhost'))

    def test__repr(self):
        self.assertEqual(repr(mongomock.MongoClient()),
                         "mongomock.MongoClient('localhost', 27017)")

class MongoDBTests(unittest.TestCase):

    def setUp(self):
        super(MongoDBTests, self).setUp()
        self.client = mongomock.MongoClient()

    def test__getting_database_via_getattr(self):
        test_db = self.client.test_database
        self.assertIs(test_db, self.client['test_database'])
        self.assertIs(test_db.client, self.client)

    def test__drop_database(self):
        test_db = self.client.test_database
        test_collection = test_db.test_database
        test_items = test_collection.insert_one({'item_id': 12345678}).inserted_id
        self.assertEqual(test_collection.count_documents({'_id': test_items}), 1)

        self.client.drop_database('test_database')
        self.assertEqual(test_collection.count_documents({'_id': test_items}), 0)

    def test__find_by_id(self):
        test_db = self.client.test_database
        test_collection = test_db.test_database
        test_items = test_collection.insert_one({'item_id': 12345678}).inserted_id
        item = test_collection.find_one({'item_id': 12345678})
        self.assertEqual(test_items, item.get('_id'))

    def test__update_by_id(self):
        test_db = self.client.test_database
        test_collection = test_db.test_database
        test_items = test_collection.insert_one({'item_id': 12345678, 'price': 4.99}).inserted_id
        item = test_collection.find_one({'price': 4.99})
        self.assertEqual(test_items, item.get('_id'))

class FlaskTestsBasic(unittest.TestCase):
    """Flask tests."""

    def setUp(self):
        """Before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage."""
        result = self.client.get("/")
        self.assertIn(b"Landing page for myRetail RESTful API", result.data)

    def test_products_home(self):
        """Test products landing page."""
        result = self.client.get('/products')
        self.assertIn(b"Getting warmer.", result.data)

    def test_product_id_page(self):
        """Test product ID that is known to be working."""
        result = self.client.get('/products/13860428', follow_redirects=True)
        self.assertIn(b"current_price", result.data)

    def test_error_response_no_product(self):
        """Test app error handling with integer"""
        result = self.client.get('/products/00000000', follow_redirects=True)
        self.assertIn(b"message", result.data)

    def test_error_response_bad_input(self):
        """Test app error handling with gibberish"""
        result = self.client.get('/products/?g@rb@ge?!', follow_redirects=True)
        self.assertIn(b"message", result.data)


# client = MongoClient('localhost', 27017)
# db = client.products
# product_price = db.product_price
#
# class Product(db):
#     item_id = item_id.self
#
# class TestProduct(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         connect('mongoenginetest', host='mongomock://localhost')
#
#     @classmethod
#     def tearDownClass(cls):
#        disconnect()
#
#     def test_thing(self):
#         item = Product(_id='12345678')
#         item.save()
#
#         new_item = Product.objects().first()
#         assert new_item._id ==  '12345678'

# class MongoTestProducts(unittest.TestCase):
#     def test_create_product(self):
#         request = {
#                 "_id" : 12345678,
#                 "current_price" : {
#                     "value" : 24.99,
#                     "currency_code" : "USD"
#                 }
#         }
#
#         with patch.object(server.db, "test"):
#             client = MongoClient('localhost', 27017)
#             db = client.products
#             product_price = db.product_price
#             app = server.db.test_client()
#             response = app.post("/products<id>", json=request)
#             self.assertEqual(response.status_code, 201)
#
#             # Validate the content
#             response_json = response.get_json()
#             expected_json = {
#                 "_id": response_json["_id"],
#                 "current_price" : {
#                     "value" : 24.99,
#                     "currency_code" : "USD"
#                 }
#             }
#             self.assertEqual(response_json, expected_json)



# class MockAPITests(unittest.TestCase):
#     """Flask tests that use the database and mock API call."""
#
#     def setUp(self):
#         """Before every test."""
#         self.client = app.test_client()
#         app.config['TESTING'] = True
#
#         connect_to_db(app, "mongo:///test_products", echo=False)
#
#         # Create tables and seed data
#         db.create_all()
#         example_data()
#
#         def _mock_get_product_api(product_id):
#             """Mock test of API call"""
#
#             return {"data":{"product":{"tcin":"84836363","item":{"product_description":{"title":"Round Velvet Decorative Throw Pillow - Threshold™","downstream_description":"The Round Velvet Decorative Throw Pillow from Threshold™ is the perfect addition to your furniture whether you want to relax in your room or enjoy the outdoor ambiance on your patio. The throw pillow has a round shape, and is fashioned in a solid velvet fabric with densely fringed trim in a matching hue that adds luxurious style to any space inside or outside your home. Boasting a 100% cotton construction that feels plush to the touch, this decorative throw pillow also features a soft fill for comfortable sitting and lounging. Place it on your loveseat, lounge chair, sofa or porch swing for a stunning look.<br /><br />Threshold™: Quality & Design / Casual classics for house and home."},"enrichment":{"images":{"primary_image_url":"https://target.scene7.com/is/image/Target/GUEST_0e0a5653-ac33-400a-bc23-8dc193bda221"}},"product_classification":{"product_type_name":"HOME","merchandise_type_name":"Decorative accent pillows"},"primary_brand":{"name":"Threshold"}}}}, 'status': 'OK'}
#
#         server.get_item_price = _mock_get_product_api
#
#     def tearDown(self):
#         """Do at end of every test."""
#
#         db.session.remove()
#         db.drop_all()
#         db.engine.dispose()
#
#     @unittest.expectedFailure   #autoincrement issue with related table, but does show connection to DB with API results
#     def test_get_prodcuct_api_with_mock(self):
#         """Mock API call with data."""
#
#         result = self.client.post('/product<id>')
#         self.assertEqual(result.status_code, 200)

if __name__ == "__main__":
    import unittest

    unittest.main()
