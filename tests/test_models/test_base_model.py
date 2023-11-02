#!/usr/bin/python3
"""Unittest for base_model([..]) after task 3"""
import datetime
import json
import os
import re
from shutil import copy2
import unittest

from models.base_model import BaseModel
from models import storage


def test_default_init(testobj, basemodel):
    # obj is an instance of BaseModel
    testobj.assertIsInstance(basemodel, BaseModel)

    # obj was assigned with UUID, created_at and updated_at
    testobj.assertIsNotNone(basemodel.id)
    testobj.assertIsNotNone(basemodel.created_at)
    testobj.assertIsNotNone(basemodel.updated_at)


def test_default_id(testobj, basemodel):
    # id is string
    testobj.assertIs(type(basemodel.id), str)
    testobj.assertIsInstance(basemodel.id, str)

    # id is in uuid format
    UUIDv4_regex = ('^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-'
                    '[89ab][a-f0-9]{3}-[a-f0-9]{12}$')
    UUIDv4 = re.compile(UUIDv4_regex, re.IGNORECASE)
    testobj.assertRegex(basemodel.id, UUIDv4)


def test_default_created_at(testobj, basemodel):
    # created_at is a datetime object
    testobj.assertIs(type(basemodel.created_at), datetime.datetime)
    testobj.assertIsInstance(basemodel.created_at, datetime.datetime)

    # created_at in UTC (tzinfo = None)
    testobj.assertIsNone(basemodel.created_at.tzinfo)

    # created_at for new instance matches current time (to the second)
    current = datetime.datetime.now()
    testobj.assertEqual(current.isoformat()[:-6],
                        basemodel.created_at.isoformat()[:-6])

    # created_at can be converted to ISO format string
    ISO_format = '%Y-%m-%dT%H:%M:%S.%f'
    dt_str = basemodel.created_at.strftime(ISO_format)
    testobj.assertEqual(dt_str, basemodel.created_at.isoformat())


def test_default_updated_at(testobj, basemodel):
    # updated_at is a datetime object
    testobj.assertIs(type(basemodel.updated_at), datetime.datetime)
    testobj.assertIsInstance(basemodel.updated_at, datetime.datetime)

    # updated_at in UTC (tzinfo = None)
    testobj.assertIsNone(basemodel.updated_at.tzinfo)

    # updated_at for new instance matches current time (to the second)
    current = datetime.datetime.now()
    testobj.assertEqual(current.isoformat()[:-6],
                        basemodel.updated_at.isoformat()[:-6])

    # updated_at can be converted to ISO format string
    ISO_format = '%Y-%m-%dT%H:%M:%S.%f'
    dt_str = basemodel.updated_at.strftime(ISO_format)
    testobj.assertEqual(dt_str, basemodel.updated_at.isoformat())


class TestBaseModel(unittest.TestCase):
    """Tests `BaseModel` class.
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
            del (bm1, bm2, bm3, bm4, bm5)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_BaseModel(self):
        """Task 3. BaseModel; Task 5. Store first object
        Tests instantiation and type of class `BaseModel`.
        """
        # Normal use: no args
        bm1 = BaseModel()
        test_default_init(self, bm1)

        # only arg (no kwarg) as an argument
        bm2 = BaseModel(None)
        test_default_init(self, bm2)
        test_default_id(self, bm2)
        test_default_created_at(self, bm2)
        test_default_updated_at(self, bm2)

        # arg and kwarg both passed as arguments
        bm1_kwarg = bm1.to_dict()
        bm3 = BaseModel("Holberton", **bm1_kwarg)
        test_default_init(self, bm3)
        test_default_id(self, bm3)
        self.assertEqual(bm1.id, bm3.id)
        test_default_created_at(self, bm3)
        self.assertEqual(bm1.created_at, bm3.created_at)
        test_default_updated_at(self, bm3)
        self.assertEqual(bm1.updated_at, bm3.updated_at)

        # passing kwarg only + keys not in dictionary
        bm1.name = "Holbie"
        bm1.num = 98
        bm1_kwarg = bm1.to_dict()
        bm4 = BaseModel(**bm1_kwarg)
        test_default_init(self, bm4)
        self.assertIsNotNone(bm4.name)
        self.assertEqual(bm1.name, bm4.name)
        self.assertIsNotNone(bm4.num)
        self.assertEqual(bm1.num, bm4.num)
        test_default_id(self, bm4)
        self.assertEqual(bm1.id, bm4.id)
        test_default_created_at(self, bm4)
        self.assertEqual(bm1.created_at, bm4.created_at)
        test_default_updated_at(self, bm4)
        self.assertEqual(bm1.updated_at, bm4.updated_at)

        # empty dictionary as argument
        empty = {}
        bm5 = BaseModel(**empty)
        test_default_init(self, bm5)
        test_default_id(self, bm5)
        test_default_created_at(self, bm5)
        test_default_updated_at(self, bm5)

        # storage.new() called in BaseModel.__init__ to add obj to __objects
        self.assertIn(bm1, storage._FileStorage__objects.values())

    def test_id(self):
        """Task 3. BaseModel
        Tests public instance attribute `id`.
        """
        # Normal use:
        bm1 = BaseModel()
        test_default_id(self, bm1)

        # id is functionally unique for each instance
        bm2 = BaseModel()
        bm3 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)
        self.assertNotEqual(bm2.id, bm3.id)

        # id is public attr, can be manually reassigned
        bm1.id = bm2.id
        self.assertEqual(bm1.id, bm2.id)

        # direct manual reassignment risks invalid UUID format
        bm3.id = '1234567890'
        UUIDv4_regex = ('^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-'
                        '[89ab][a-f0-9]{3}-[a-f0-9]{12}$')
        self.assertIsNone(re.match(UUIDv4_regex, bm3.id, re.IGNORECASE))

    def test_created_at(self):
        """Task 3. BaseModel
        Tests public instance attribute `created_at`.
        """
        # Normal use:
        bm1 = BaseModel()
        test_default_created_at(self, bm1)

        # created_at is public attr, can be manually reassigned
        bm2 = BaseModel()
        bm1.created_at = bm2.created_at
        self.assertEqual(bm1.created_at, bm2.created_at)

        # direct manual reassignment risks invalid format
        bm2.created_at = '1234567890'
        self.assertNotIsInstance(bm2.created_at, datetime.datetime)

    def test_updated_at(self):
        """Task 3. BaseModel
        Tests public instance attribute `updated_at`.
        """
        # Normal use: no args
        bm1 = BaseModel()
        test_default_updated_at(self, bm1)

        # updated_at is public attr, can be manually reassigned
        bm2 = BaseModel()
        bm1.updated_at = bm2.updated_at
        self.assertEqual(bm1.updated_at, bm2.updated_at)

        # direct manual reassignment risks invalid format
        bm2.updated_at = '1234567890'
        self.assertNotIsInstance(bm2.updated_at, datetime.datetime)

    def test___str__(self):
        """Task 3. BaseModel
        Tests private instance method `__str__`.
        """
        # Normal use:
        bm1 = BaseModel()

        # prints '[<class name>] (<self.id>) <self.__dict__>'
        __str = str(bm1)
        self.assertEqual(__str, '[' + bm1.__class__.__name__ + '] (' +
                         bm1.id + ') ' + str(bm1.__dict__))

        # BaseModel.__str__ without instantiation
        self.assertEqual(str(BaseModel),
                         "<class 'models.base_model.BaseModel'>")

    def test_save(self):
        """Task 3. BaseModel; Task 5. Store first object
        Tests public instance method `save`.
        """
        # Normal use:
        bm1 = BaseModel()

        # updated_at starts at same time (to the second) as created_at
        self.assertEqual(bm1.created_at.isoformat()[:-6],
                         bm1.updated_at.isoformat()[:-6])

        # updated_at is public attr, can be manually reassigned
        ISO_format = '%Y-%m-%dT%H:%M:%S.%f'
        example_ISO = '1900-05-13T01:10:20.000001'
        dt_update = datetime.datetime.strptime(example_ISO, ISO_format)
        bm1.updated_at = dt_update
        self.assertNotEqual(bm1.created_at.year, bm1.updated_at.year)

        # save() updates updated_at to match the current time (to the second)
        current = datetime.datetime.now()
        bm1.save()
        self.assertEqual(current.isoformat()[:-6],
                         bm1.updated_at.isoformat()[:-6])

        # updated_at still in UTC (tzinfo = None)
        self.assertIsNone(bm1.updated_at.tzinfo)

        # updated_at still can be converted to ISO format string
        ISO_format = '%Y-%m-%dT%H:%M:%S.%f'
        dt_str = bm1.updated_at.strftime(ISO_format)
        self.assertEqual(dt_str, bm1.updated_at.isoformat())

        # calls storage.save() to update JSON file
        bm1.save()
        self.assertTrue(os.path.isfile(storage._FileStorage__file_path))
        with open(storage._FileStorage__file_path, encoding='utf-8') as file:
            self.assertIn('BaseModel.' + bm1.id, json.load(file))

    def test_to_dict(self):
        """Task 3. BaseModel
        Tests public instance method `to_dict`.
        """
        # Normal use:
        bm1 = BaseModel()

        # returns a dictionary
        self.assertIs(type(bm1.to_dict()), dict)

        # returns a dict that contains all members of self.__dict__
        for item in bm1.__dict__:
            self.assertIn(item, bm1.to_dict())

        # returned dict also contains self.__class__.__name__ as '__class__'
        bm1_dict = bm1.to_dict()
        self.assertIn('__class__', bm1_dict)
        self.assertEqual(bm1.__class__.__name__, bm1_dict['__class__'])

        # returned dict also contains self.created_at as 'created_at'
        self.assertIn('created_at', bm1_dict)
        self.assertEqual(bm1.created_at.isoformat(),
                         bm1_dict['created_at'])

        # returned dict also contains self.updated_at as 'updated_at'
        self.assertIn('updated_at', bm1_dict)
        self.assertEqual(bm1.updated_at.isoformat(),
                         bm1_dict['updated_at'])
