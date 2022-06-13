import unittest
import sys
import os
sys.path.insert(0, os.getcwd()+"/SubDirectory")
# import app.main.server
import mongomock
import server


class FlaskTestsBasic(unittest.TestCase):
    """Flask app tests"""

    def setUp(self):
        """Before every test"""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage"""
        result = self.client.get("/")
        self.assertIn(b"Landing page for myRetail RESTful API", result.data)

    def test_products_home(self):
        """Test products landing page"""
        result = self.client.get('/products')
        self.assertIn(b"Getting warmer.", result.data)

    def test_product_id_page(self):
        """Test product ID that is known to be working"""
        result = self.client.get('/products/13860428', follow_redirects=True)
        self.assertIn(b"current_price", result.data)

    def test_error_response_bad_input(self):
        """Test app error handling with gibberish"""
        result = self.client.get('/products/?g@rb@ge?!', follow_redirects=True)
        self.assertIn(b"message", result.data)

    def test_error_response_no_product(self):
        """Test app error handling with integer"""
        result = self.client.get('/products/00000000', follow_redirects=True)
        self.assertIn(b"message", result.data)

class MockAPITests(unittest.TestCase):
    """Tests that mock API call"""

    def setUp(self):
        super(MockAPITests, self).setUp()
        self.client = mongomock.MongoClient()

    def test_get_price_from_api(self):
        test_db = self.client.test_database
        test_collection = test_db.test_database
        test_items = test_collection.insert_one({"item_id":84836363, "current_price" : {"value" : 20.77, "currency_code" : "USD"}})
        item = test_collection.find_one({'item_id': 84836363})

        def _mock_get_product_api():
            """Dummy return of API call"""

            result = {"data":{"product":{"tcin":"84836363","item":{"product_description":{"title":"Round Velvet Decorative Throw Pillow - Threshold™","downstream_description":"The Round Velvet Decorative Throw Pillow from Threshold™ is the perfect addition to your furniture whether you want to relax in your room or enjoy the outdoor ambiance on your patio. The throw pillow has a round shape, and is fashioned in a solid velvet fabric with densely fringed trim in a matching hue that adds luxurious style to any space inside or outside your home. Boasting a 100% cotton construction that feels plush to the touch, this decorative throw pillow also features a soft fill for comfortable sitting and lounging. Place it on your loveseat, lounge chair, sofa or porch swing for a stunning look.<br /><br />Threshold™: Quality & Design / Casual classics for house and home."},"enrichment":{"images":{"primary_image_url":"https://target.scene7.com/is/image/Target/GUEST_0e0a5653-ac33-400a-bc23-8dc193bda221"}},"product_classification":{"product_type_name":"HOME","merchandise_type_name":"Decorative accent pillows"},"primary_brand":{"name":"Threshold"}}}}, 'status': 'OK'}

            return result

        data = _mock_get_product_api()
        id = data['data']['product']['tcin']

        price = test_collection.find_one({'_id': id})
        self.assertEqual(item['current_price']['value'], 20.77)

class MongoDBTests(unittest.TestCase):
    """Tests of MongoDB setup"""

    def test_can_create_db_without_path(self):
        self.assertIsNotNone(mongomock.MongoClient())

    def test_can_create_db_with_path(self):
        self.assertIsNotNone(mongomock.MongoClient('mongodb://localhost'))

    def test_repr(self):
        self.assertEqual(repr(mongomock.MongoClient()),
                         "mongomock.MongoClient('localhost', 27017)")

class MongoActionTests(unittest.TestCase):
    """Tests of MongoDB behavior and functionality"""

    def setUp(self):
        super(MongoActionTests, self).setUp()
        self.client = mongomock.MongoClient()

    def test_getting_database_via_getattr(self):
        test_db = self.client.test_database
        self.assertIs(test_db, self.client['test_database'])
        self.assertIs(test_db.client, self.client)

    def test_drop_database(self):
        test_db = self.client.test_database
        test_collection = test_db.test_database
        test_items = test_collection.insert_one({'item_id': 12345678}).inserted_id
        self.assertEqual(test_collection.count_documents({'_id': test_items}), 1)

        self.client.drop_database('test_database')
        self.assertEqual(test_collection.count_documents({'_id': test_items}), 0)

    def test_find_by_id(self):
        test_db = self.client.test_database
        test_collection = test_db.test_database
        test_items = test_collection.insert_one({'item_id': 12345678}).inserted_id
        item = test_collection.find_one({'item_id': 12345678})
        self.assertEqual(test_items, item.get('_id'))

    def test_update_by_id(self):
        test_db = self.client.test_database
        test_collection = test_db.test_database
        test_item = test_collection.insert_one({'item_id': 12345678, 'price': 9.99}).inserted_id
        find_test_item = test_collection.find_one({'price': 9.99})

        update_item = test_collection.update_one({'item_id': 12345678}, {"$set": { 'price': 4.99}})
        updated_test_item = test_collection.find_one({'price': 4.99})
        self.assertEqual(find_test_item['item_id'], updated_test_item['item_id'])

if __name__ == "__main__":
    import unittest

    unittest.main()
