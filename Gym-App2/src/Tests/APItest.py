import unittest
import json
import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(parent_dir)

# Import modules
from app import app, internal_search_food, internal_full_API_Method
from models import Response

# Undo the path change
if parent_dir in sys.path:
    sys.path.remove(parent_dir)


class SearchTest(unittest.TestCase):

    def setUp(self):
        # Set up the application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Load JSON data from a file
        with open('Gym-App2/src/Tests/chicken.json', 'r') as file:
            self.data = json.load(file)

    def tearDown(self):
        # Tear down the application context
        self.app_context.pop()

    def test_food_search(self):
        result = internal_search_food('chicken')
        self.assertEqual(result, self.data)

    def test_food_db(self):
        # Perform a database query within the application context
        '''
        result = Response.query.filter((Response.search == "chicken")).first()
        self.assertEqual(result, self.data)
        '''

    def test_full_function(self):
        result = internal_full_API_Method("chicken")
        self.assertEqual(result, self.data)

        empty_response = json.loads('''
        {
            "foods": {
                "max_results": "20",
                "page_number": "0",
                "total_results": "0"
            }
        }
        ''')
        result = internal_full_API_Method("sxdfghjk")
        self.assertEqual(result, empty_response)


if __name__ == '__main__':
    unittest.main()