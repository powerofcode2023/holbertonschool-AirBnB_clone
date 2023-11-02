#!/usr/bin/python3
"""Unittest for city([..]) after task 9"""
import unittest
import json
import os
from shutil import copy2

from models.city import City
from models import storage


class TestCity(unittest.TestCase):
    """Tests `City` class.
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
            del (c1, c2)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_City(self):
        """Task 9
        Tests `City` class.
        """
        # Normal use: no args
        c1 = City()
        self.assertIsInstance(c1, City)

        # attr `name` defaults to empty string
        self.assertIsInstance(c1.name, str)
        self.assertEqual(c1.name, '')

        # attr `state_id` defaults to empty string
        self.assertIsInstance(c1.state_id, str)
        self.assertEqual(c1.state_id, '')

        # City can be serialized to JSON by FileStorage
        c1.name = 'test'
        c1.state_id = 'test'
        self.assertIn(c1, storage._FileStorage__objects.values())
        c1.save()
        with open(storage._FileStorage__file_path, encoding='utf-8') as file:
            content = file.read()
        key = c1.__class__.__name__ + '.' + c1.id
        self.assertIn(key, json.loads(content))

        # City can be deserialized from JSON by FileStorage
        self.assertIn(key, storage._FileStorage__objects.keys())
        storage._FileStorage__objects = dict()
        storage.reload()
        self.assertIn(key, storage._FileStorage__objects.keys())
