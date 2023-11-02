#!/usr/bin/python3
"""Unittest for review([..]) after task 9"""
import unittest
import json
import os
from shutil import copy2

from models.review import Review
from models import storage


class TestReview(unittest.TestCase):
    """Tests `Review` class.
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
            del (r1, r2)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_Review(self):
        """Task 9
        Tests `Review` class.
        """
        # Normal use: no args
        r1 = Review()
        self.assertIsInstance(r1, Review)

        # attr `place_id` defaults to empty string
        self.assertIsInstance(r1.place_id, str)
        self.assertEqual(r1.place_id, '')

        # attr `user_id` defaults to empty string
        self.assertIsInstance(r1.user_id, str)
        self.assertEqual(r1.user_id, '')

        # attr `text` defaults to empty string
        self.assertIsInstance(r1.text, str)
        self.assertEqual(r1.text, '')

        # Review can be serialized to JSON by FileStorage
        r1.place_id = 'test'
        r1.user_id = 'test'
        r1.text = 'test'
        self.assertIn(r1, storage._FileStorage__objects.values())
        r1.save()
        with open(storage._FileStorage__file_path, encoding='utf-8') as file:
            content = file.read()
        key = r1.__class__.__name__ + '.' + r1.id
        self.assertIn(key, json.loads(content))

        # Review can be deserialized from JSON by FileStorage
        self.assertIn(key, storage._FileStorage__objects.keys())
        storage._FileStorage__objects = dict()
        storage.reload()
        self.assertIn(key, storage._FileStorage__objects.keys())
