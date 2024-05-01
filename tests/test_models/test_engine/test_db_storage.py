#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import pep8
import unittest
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from models import storage
from models.base_model import Base


DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

class TestDBStorageGetMethod(unittest.TestCase):
    """Unittests for get method of db storage module"""

    @classmethod
    def setUpClass(cls):
        """DBStorage testing setup."""
        if type(models.storage) == DBStorage:
            cls.storage = DBStorage()
            Base.metadata.create_all(cls.storage._DBStorage__engine)
            Session = sessionmaker(bind=cls.storage._DBStorage__engine)
            cls.storage._DBStorage__session = Session()
            cls.storage._DBStorage__session.commit()

    @classmethod
    def tearDownClass(cls):
        """DBStorage testing teardown."""
        if type(models.storage) == DBStorage:
            # Remove all records from the tables
            cls.storage._DBStorage__session.execute(
                text("DELETE FROM amenities"))
            cls.storage._DBStorage__session.execute(text("DELETE FROM cities"))
            cls.storage._DBStorage__session.execute(text("DELETE FROM places"))
            cls.storage._DBStorage__session.execute(
                text("DELETE FROM reviews"))
            cls.storage._DBStorage__session.execute(text("DELETE FROM states"))
            cls.storage._DBStorage__session.execute(text("DELETE FROM users"))

            cls.storage._DBStorage__session.commit()

            # Delete the session
            cls.storage._DBStorage__session.close()

            # Delete the storage
            del cls.storage

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_amenity_wrong_id(self):
        """test get with amenity with wrong id"""
        self.assertEqual(storage.get(Amenity, '12345'), None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_city_wrong_id(self):
        """test get with city with wrong id"""
        self.assertEqual(storage.get(City, '12345'), None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_place_wrong_id(self):
        """test get with place with wrong id"""
        self.assertEqual(storage.get(Place, '12345'), None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_review_wrong_id(self):
        """test get with review with wrong id"""
        self.assertEqual(storage.get(Review, '12345'), None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_state_wrong_id(self):
        """test get with state with wrong id"""
        self.assertEqual(storage.get(State, '12345'), None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_user_wrong_id(self):
        """test get with user with wrong id"""
        self.assertEqual(storage.get(User, '12345'), None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_amenity_valid_id(self):
        """test get with amenity with valid id"""
        amenity = Amenity(name="Anything")
        amenity.save()
        amenity_from_get = storage.get(Amenity, amenity.id)
        self.assertEqual(amenity_from_get.to_dict(), amenity.to_dict())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_city_valid_id(self):
        """test get with city with valid id"""
        state = State(name="Anything")
        state.save()
        city = City(name="city_name", state_id=state.id)
        city.save()
        city_from_get = storage.get(City, city.id)
        self.assertEqual(city_from_get.to_dict(), city.to_dict())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_without_cls(self):
        """Test count without cls"""
        amenity = Amenity(name="amenity_name")
        amenity.save()
        state = State(name="state_name")
        state.save()
        city = City(name="city_name", state_id=state.id)
        city.save()
        user = User(fisrt_name="real",
                    last_name="3bdelrahman",
                    email="abdelrahman@gmail.com",
                    password="winner-winner_chicken-dinner")
        user.save()

        self.assertEqual(storage.count(), 4)
        self.assertEqual(storage.count(), len(storage.all()))


if __name__ == "__main__":
    unittest.main()
