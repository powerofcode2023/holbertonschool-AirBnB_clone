#!/usr/bin/python3
"""Unittest for place([..]) after task 9"""
import unittest
import json
import os
from shutil import copy2

from models.place import Place
from models import storage


class TestPlace(unittest.TestCase):
    """Tests `Place` class.
    For interactions with *args and **kwargs, see test_base_model.

    Attributes:
        __objects_backup (dict): copy of current dict of `FileStorage` objects
        json_file (str): filename for JSON file of `FileStorage` objects
        json_file_backup (str): filename for backup of `json_file`

    """
    __objects_backup = storage._FileStorage__objects
    json_file = storage._FileStorage__file_path
    json_file_backup = storage._FileStorage__file_path + '.bup'

    @classmethod
    def setUpClass(cls):
        """Setup for all tests in module.
        """
        storage._FileStorage__objects = dict()
        if os.path.exists(cls.json_file):
            copy2(cls.json_file, cls.json_file_backup)
            os.remove(cls.json_file)

    @classmethod
    def tearDownClass(cls):
        """Teardown after all tests in module.
        """
        storage._FileStorage__objects = cls.__objects_backup
        if os.path.exists(cls.json_file_backup):
            copy2(cls.json_file_backup, cls.json_file)
            os.remove(cls.json_file_backup)

    def tearDown(self):
        """Any needed cleanup, per test method.
        """
        try:
            del (p1, p2)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_Place(self):
        """Task 9
        Tests `Place` class.
        """
        # Normal use: no args
        p1 = Place()
        self.assertIsInstance(p1, Place)

        # attr `city_id` defaults to empty string
        self.assertIsInstance(p1.city_id, str)
        self.assertEqual(p1.city_id, '')

        # attr `user_id` defaults to empty string
        self.assertIsInstance(p1.user_id, str)
        self.assertEqual(p1.user_id, '')

        # attr `name` defaults to empty string
        self.assertIsInstance(p1.name, str)
        self.assertEqual(p1.name, '')

        # attr `description` defaults to empty string
        self.assertIsInstance(p1.description, str)
        self.assertEqual(p1.description, '')

        # attr `number_rooms` defaults to int 0
        self.assertIsInstance(p1.number_rooms, int)
        self.assertEqual(p1.number_rooms, 0)

        # attr `number_bathrooms` defaults to int 0
        self.assertIsInstance(p1.number_bathrooms, int)
        self.assertEqual(p1.number_bathrooms, 0)

        # attr `max_guest` defaults to empty int 0
        self.assertIsInstance(p1.max_guest, int)
        self.assertEqual(p1.max_guest, 0)

        # attr `price_by_night` defaults to int 0
        self.assertIsInstance(p1.price_by_night, int)
        self.assertEqual(p1.price_by_night, 0)

        # attr `latitude` defaults to float 0.0
        self.assertIsInstance(p1.latitude, float)
        self.assertEqual(p1.latitude, 0.0)

        # attr `longitude` defaults to float 0.0
        self.assertIsInstance(p1.longitude, float)
        self.assertEqual(p1.longitude, 0.0)

        # attr `amenity_ids` defaults to empty list
        self.assertIsInstance(p1.amenity_ids, list)
        self.assertEqual(p1.amenity_ids, [])

        # Place can be serialized to JSON by FileStorage
        p1.city_id = 'test1'
        p1.user_id = 'test2'
        p1.name = 'test3'
        p1.description = 'test4'
        p1.number_rooms = 1
        p1.number_bathrooms = -2
        p1.max_guest = 3
        p1.price_by_night = -4
        p1.latitude = -5.5
        p1.longitude = 6.6
        p1.amenity_ids = ['id1', 'id2']
        self.assertIn(p1, storage._FileStorage__objects.values())
        p1.save()
        with open(storage._FileStorage__file_path, encoding='utf-8') as file:
            content = file.read()
        key = p1.__class__.__name__ + '.' + p1.id
        self.assertIn(key, json.loads(content))

        # Place can be deserialized from JSON by FileStorage
        self.assertIn(key, storage._FileStorage__objects.keys())
        storage._FileStorage__objects = dict()
        storage.reload()
        self.assertIn(key, storage._FileStorage__objects.keys())
