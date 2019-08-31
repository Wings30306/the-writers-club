import unittest
import app
from helper import calculate_age, stories_collection, users_collection
import os
from datetime import date, datetime



class testApp(unittest.TestCase):
    
    """
    Test suite for app.py
    """
    def test_is_this_thing_on(self):
        self.assertEqual(1, 1)

    def test_env_variables(self):
        database_url = os.getenv("MONGO_URI")
        self.assertEqual(database_url, os.getenv("MONGO_URI"))
        database_name = os.getenv("MONGO_DBNAME")
        self.assertEqual(database_name, os.getenv("MONGO_DBNAME"))
        secret_key = os.getenv("SECRET_KEY")
        self.assertEqual(secret_key, os.getenv("SECRET_KEY"))
    
    def test_database_name_matches_database_url(self):
        database_url = os.getenv("MONGO_URI")
        database_name = os.getenv("MONGO_DBNAME")
        self.assertIn(database_name, database_url)

    def test_age_calculator(self):
        age1 = calculate_age("1984-06-21")
        age2 = calculate_age("2010-11-10")
        age3 = calculate_age(datetime.strftime(date.today(), '%Y-%m-%d'))
        self.assertGreaterEqual(age1, 34)
        self.assertLess(age2, 18)
        self.assertEqual(age3, 0)

    def test_collections(self):
        self.assertIsNotNone(stories_collection.find())
        self.assertIsNotNone(users_collection.find())

    

    