import unittest
import json
from app import create_app, db

"""This class represents the shopping list test case"""


class UserTestCase(unittest.TestCase):
    """Define test variables and initialize app."""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'email': 'my email is charles@name.com'}

        # create all tables
        with self.app.app_context():
            db.create_all()

    def test_user_signup(self):
        """Test API can register users (POST request)"""
        res = self.client().post('/signup/', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Add user to the  application account', str(res.data))

    """Test API can get a application users (GET request)."""

    def test_api_can_get_all_signup_user_lists(self):
        res = self.client().post('/signup/', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/signup/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('retrieve the user list', str(res.data))

        """Test API can get a single user by using it's email."""

    def test_api_user_signup_by_email(self):
        rv = self.client().post('/signup/', data=self.user)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/signup/{}'.format(result_in_json['email']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Check user email', str(result.data))

    """teardown all initialized variables."""

    # drop all tables
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


# Make the tests executable
if __name__ == "__main__":
    unittest.main()

