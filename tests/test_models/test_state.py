#!/usr/bin/python3
"""test for state"""
import unittest
import MySQLdb
from models import storage
import os
from models.state import State
from models.base_model import BaseModel
import pep8


class TestState(unittest.TestCase):
    """this will test the State class"""

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.state = State()
        cls.state.name = "CA"

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.state

    def tearDown(self):
        """Close the MySQL connection after testing"""
        try:
            os.remove("file.json")
        except Exception:
            pass
            
     @unittest.skipIf(storage._DBStorage__engine == 'db', "Skipping MySQL test for db storage engine")
     def test_create_state(self):
        # Establish database connection
        db = MySQLdb.connect(host="HBNB_MYSQL_HOST", user="HBNB_MYSQL_USER", passwd="HBNB_MYSQL_PWD", db="BNB_MYSQL_DB")
        cursor = db.cursor()
        
        # Get the number of current records in the states table
        self.cursor.execute("SELECT COUNT(*) FROM states")
        count_before = self.cursor.fetchone()[0]

        # Create a new State object
        new_state = State(name="California")

        # Add the State object to the database
        self.storage.new(new_state)
        self.storage.save()

        # Get the number of records in the states table after adding the new State
        self.cursor.execute("SELECT COUNT(*) FROM states")
        count_after = self.cursor.fetchone()[0]

        # Assert that the count increased by 1 after adding the new State
        self.assertEqual(count_after, count_before + 1)
        
        # Close cursor and database connection
        cursor.close()
        db.close()

    def test_pep8_Review(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/state.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_State(self):
        """checking for docstrings"""
        self.assertIsNotNone(State.__doc__)

    def test_attributes_State(self):
        """chekcing if State have attributes"""
        self.assertTrue('id' in self.state.__dict__)
        self.assertTrue('created_at' in self.state.__dict__)
        self.assertTrue('updated_at' in self.state.__dict__)
        self.assertTrue('name' in self.state.__dict__)

    def test_is_subclass_State(self):
        """test if State is subclass of BaseModel"""
        self.assertTrue(issubclass(self.state.__class__, BaseModel), True)

    def test_attribute_types_State(self):
        """test attribute type for State"""
        self.assertEqual(type(self.state.name), str)

    def test_save_State(self):
        """test if the save works"""
        self.state.save()
        self.assertNotEqual(self.state.created_at, self.state.updated_at)

    def test_to_dict_State(self):
        """test if dictionary works"""
        self.assertEqual('to_dict' in dir(self.state), True)


if __name__ == "__main__":
    unittest.main()
