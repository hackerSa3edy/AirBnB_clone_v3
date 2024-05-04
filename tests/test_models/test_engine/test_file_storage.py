#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from models import storage
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))


class TestFileStorageGetMethod(unittest.TestCase):
    """Unittests for get method of file storage module"""

    @classmethod
    def setUp(cls):
        """Set up test methods"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(cls):
        """Tear down test methods"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_with_amenity_wrong_id(self):
        """test get with amenity with wrong id"""
        self.assertEqual(storage.get(Amenity, '12345'), None)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_with_city_wrong_id(self):
        """test get with city with wrong id"""
        self.assertEqual(storage.get(City, '12345'), None)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_with_place_wrong_id(self):
        """test get with place with wrong id"""
        self.assertEqual(storage.get(Place, '12345'), None)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_with_review_wrong_id(self):
        """test get with review with wrong id"""
        self.assertEqual(storage.get(Review, '12345'), None)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_with_state_wrong_id(self):
        """test get with state with wrong id"""
        self.assertEqual(storage.get(State, '12345'), None)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_with_user_wrong_id(self):
        """test get with user with wrong id"""
        self.assertEqual(storage.get(User, '12345'), None)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_with_amenity_valid_id(self):
        """test get with amenity with valid id"""
        amenity = Amenity()
        amenity.save()
        amenity_from_get = storage.get(Amenity, amenity.id)
        self.assertEqual(amenity_from_get.to_dict(), amenity.to_dict())

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_with_city_valid_id(self):
        """test get with city with valid id"""
        city = City()
        city.save()
        city_from_get = storage.get(City, city.id)
        self.assertEqual(city_from_get.to_dict(), city.to_dict())

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_with_place_valid_id(self):
        """test get with place with valid id"""
        place = Place()
        place.save()
        place_from_get = storage.get(Place, place.id)
        self.assertEqual(place_from_get.to_dict(), place.to_dict())

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_with_review_valid_id(self):
        """test get with Reviestate with valid id"""
        review = Review()
        review.save()
        review_from_get = storage.get(Review, review.id)
        self.assertEqual(review_from_get.to_dict(), review.to_dict())

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_with_state_valid_id(self):
        """test get with state with valid id"""
        state = State()
        state.save()
        state_from_get = storage.get(State, state.id)
        self.assertEqual(state_from_get.to_dict(), state.to_dict())

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_with_user_valid_id(self):
        """test get with user with valid id"""
        user = User()
        user.save()
        user_from_get = storage.get(User, user.id)
        self.assertEqual(user_from_get.to_dict(), user.to_dict())


class TestFileStorageCountMethod(unittest.TestCase):
    """Unittests for count method of file storage module"""

    @classmethod
    def setUp(cls):
        """Set up test methods"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

        return super().setUp()


    @classmethod
    def tearDown(cls):
        """Tear down test methods"""
        FileStorage._FileStorage__objects = {}
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

        return super().tearDown()

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count_without_cls(self):
        """Test count without cls"""
        amenity = Amenity()
        amenity.save()
        city = City()
        city.save()
        place = Place()
        place.save()
        review = Review()
        review.save()
        state = State()
        state.save()
        user = User()
        user.save()
        self.assertEqual(storage.count(), 6)
        self.assertEqual(storage.count(), len(storage.all()))

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count_with_amenity_cls(self):
        """Test count with amenity cls"""
        amenity = Amenity()
        amenity.save()
        city = City()
        city.save()
        place = Place()
        place.save()
        review = Review()
        review.save()
        state = State()
        state.save()
        user = User()
        user.save()
        print(len(storage.all()))
        self.assertEqual(len(storage.all()), 6)
        self.assertEqual(storage.count(Amenity), 1)
        self.assertNotEqual(storage.count(Amenity), len(storage.all()))

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count_with_city_cls(self):
        """Test count with city cls"""
        amenity = Amenity()
        amenity.save()
        city = City()
        city.save()
        place = Place()
        place.save()
        review = Review()
        review.save()
        state = State()
        state.save()
        user = User()
        user.save()
        self.assertEqual(storage.count(City), 1)
        self.assertNotEqual(storage.count(City), len(storage.all()))

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count_with_place_cls(self):
        """Test count with place cls"""
        amenity = Amenity()
        amenity.save()
        city = City()
        city.save()
        place = Place()
        place.save()
        review = Review()
        review.save()
        state = State()
        state.save()
        user = User()
        user.save()
        self.assertEqual(storage.count(Place), 1)
        self.assertNotEqual(storage.count(Place), len(storage.all()))

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count_with_review_cls(self):
        """Test count with review cls"""
        amenity = Amenity()
        amenity.save()
        city = City()
        city.save()
        place = Place()
        place.save()
        review = Review()
        review.save()
        state = State()
        state.save()
        user = User()
        user.save()
        self.assertEqual(storage.count(Review), 1)
        self.assertNotEqual(storage.count(Review), len(storage.all()))

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count_with_state_cls(self):
        """Test count with state cls"""
        amenity = Amenity()
        amenity.save()
        city = City()
        city.save()
        place = Place()
        place.save()
        review = Review()
        review.save()
        state = State()
        state.save()
        user = User()
        user.save()
        self.assertEqual(storage.count(State), 1)
        self.assertNotEqual(storage.count(State), len(storage.all()))

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count_with_user_cls(self):
        """Test count with user cls"""
        amenity = Amenity()
        amenity.save()
        city = City()
        city.save()
        place = Place()
        place.save()
        review = Review()
        review.save()
        state = State()
        state.save()
        user = User()
        user.save()
        self.assertEqual(storage.count(User), 1)
        self.assertNotEqual(storage.count(User), len(storage.all()))


if __name__ == '__main__':
    unittest.main()
