#!/usr/bin/python3
"""Unittest for state([..]) after task 9"""
import unittest
import json
import os
from shutil import copy2

from models.state import State
from models import storage


class TestState(unittest.TestCase):
    """Tests `State` class.
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
            del (s1, s2)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_State(self):
        """Task 9
        Tests `State` class.
        """
        # Normal use: no args
        s1 = State()
        self.assertIsInstance(s1, State)

        # attr `name` defaults to empty string
        self.assertIsInstance(s1.name, str)
        self.assertEqual(s1.name, '')

        # State can be serialized to JSON by FileStorage
        s1.name = 'test'
        self.assertIn(s1, storage._FileStorage__objects.values())
        s1.save()
        with open(storage._FileStorage__file_path, encoding='utf-8') as file:
            content = file.read()
        key = s1.__class__.__name__ + '.' + s1.id
        self.assertIn(key, json.loads(content))

        # State can be deserialized from JSON by FileStorage
        self.assertIn(key, storage._FileStorage__objects.keys())
        storage._FileStorage__objects = dict()
        storage.reload()
        self.assertIn(key, storage._FileStorage__objects.keys())
