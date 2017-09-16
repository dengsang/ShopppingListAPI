import unittest
import json
from app import create_app, db

"""This class represents the shopping list test case"""


class ShoppingListApiTestCase(unittest.TestCase):
    """Define test variables and initialize app."""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.shopping_list = {'item': 'Items in my shopping list'}
        # self.shopping_app_user = {'username': 'my name is charles'}

        # create all tables
        with self.app.app_context():
            db.create_all()

    def test_shopping_list_creation(self):
        """Test API can create a shopping list (POST request)"""
        res = self.client().post('/dashboard/', data=self.shopping_list)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Add items to the shopping list', str(res.data))

    """Test API can get a shopping list (GET request)."""

    def test_api_can_get_all_shopping_lists(self):
        res = self.client().post('/dashboard/', data=self.shopping_list)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/dashboard/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Add items to the shopping list', str(res.data))

        """Test API can get a single shopping list by using it's id."""

    def test_api_can_get_shopping_list_by_item(self):
        rv = self.client().post('/dashboard/', data=self.shopping_list)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/dashboard/{}'.format(result_in_json['item']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Check shopping list', str(result.data))

        """Test API can edit an existing shopping list. (PUT request)"""

    def test_shopping_list_can_be_edited(self):
        rv = self.client().post(
            '/dashboard/',
            data={'item': 'Items can be changed'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/dashboard/1',
            data={
                "item": "Items in the list can be added or removed"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/dashboard/<item>')
        self.assertIn('Be checking the list ', str(results.data))

    """Test API can delete an existing shopping list. (DELETE request)."""

    def test_shopping_list_deletion(self):
        rv = self.client().post(
            '/dashboard/',
            data={'item': 'carrots, chocolate and maize'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/dashboard/<item>')
        self.assertEqual(res.status_code, 200)

        # Test to see if it exists, should return a 404
        result = self.client().get('/dashboard/<item>')
        self.assertEqual(result.status_code, 404)

    """teardown all initialized variables."""

    # drop all tables
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
