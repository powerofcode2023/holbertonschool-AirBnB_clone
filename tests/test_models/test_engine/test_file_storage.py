#!/usr/bin/python3
"""Unittest for file_storage after task 5."""
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import json
import os
from shutil import copy2


class TestFileStorage(unittest.TestCase):
    """Tests `FileStorage` class.

    """
    __objects_backup = FileStorage._FileStorage__objects
    json_file = FileStorage._FileStorage__file_path
    json_file_backup = FileStorage._FileStorage__file_path + '.bup'

    @classmethod
    def setUpClass(cls):
        """Setup for all tests in module.

        """
        FileStorage._FileStorage__objects = dict()
        if os.path.exists(cls.json_file):
            copy2(cls.json_file, cls.json_file_backup)
            os.remove(cls.json_file)

    @classmethod
    def tearDownClass(cls):
        """Teardown after all tests in module.

        """
        FileStorage._FileStorage__objects = cls.__objects_backup
        if os.path.exists(cls.json_file_backup):
            copy2(cls.json_file_backup, cls.json_file)
            os.remove(cls.json_file_backup)

    def tearDown(self):
        """Any needed cleanup, per test method.

        """
        try:
            del (fs1, fs2, fs3, fs4)
        except NameError:
            pass
        try:
            del (bm1, bm2, bm3, bm4)
        except NameError:
            pass
        FileStorage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_FileStorage(self):
        """Task 5. Store first object
        Tests instantiation of class `FileStorage` and use in models__init__.

        """
        # TypeError: any args
        self.assertRaises(TypeError, FileStorage, 'arg')
        # no args
        fs1 = FileStorage()
        self.assertIsInstance(fs1, FileStorage)
        # Normal use: as `storage` attr in models.__init__, imprtd to BaseModel
        bm1 = BaseModel()
        from models import storage
        self.assertIsInstance(storage, FileStorage)

    def test___file_path(self):
        """Task 5. Store first object
        Tests private class attribute `__file_path`.

        """
        fs1 = FileStorage()
        # new FileStorage object has __file_path
        self.assertIsNotNone(fs1._FileStorage__file_path)
        # __file_path is a string
        __file_path = fs1._FileStorage__file_path
        self.assertIsInstance(__file_path, str)
        # __file_path ends in '.json'
        self.assertEqual(__file_path[-5:], '.json')
        # __file_path is writable (permissions)
        content = 'Test text 0123456789abcdefghijklmnopqrstuvwxyz'
        with open(__file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        with open(__file_path, 'r', encoding='utf-8') as file:
            self.assertEqual(content, file.read())

    def test___objects(self):
        """Task 5. Store first object
        Tests private class attribute `__objects`.

        """
        fs1 = FileStorage()
        # new FileStorage object has __objects
        self.assertIsNotNone(fs1._FileStorage__objects)
        # __objects is a dict
        __objects = fs1._FileStorage__objects
        self.assertIsInstance(__objects, dict)
        # __objects is empty to start
        self.assertEqual(len(__objects), 0)
        # __objects can store item with key:'<obj class name>.id', value: obj
        bm1 = BaseModel()
        bm1_dict = bm1.to_dict()
        bm1__objects_key = bm1_dict['__class__'] + '.' + bm1.id
        __objects[bm1__objects_key] = bm1
        self.assertIn(bm1__objects_key, __objects)
        self.assertEqual(__objects[bm1__objects_key], bm1)

    def test_all(self):
        """Task 5. Store first object
        Tests public instance method `all()`.

        """
        fs1 = FileStorage()
        # TypeError: any args
        self.assertRaises(TypeError, fs1.all, 'arg')
        # Normal use: no args
        fs1__objects = fs1.all()
        # returns __objects
        self.assertEqual(fs1._FileStorage__objects, fs1__objects)

    def test_new(self):
        """Task 5. Store first object
        Tests public instance method `new()`. See also
        TestBaseModel.test_BaseModel.

        """
        fs1 = FileStorage()
        # TypeError: no args
        self.assertRaises(TypeError, fs1.new)
        # TypeError: 2+ args
        self.assertRaises(TypeError, fs1.new, 'arg1', 'arg2')
        # called in BaseModel.__init__, to include new BM obj in __objects
        bm1 = BaseModel()
        from models import storage
        self.assertIn(bm1, storage._FileStorage__objects.values())
        # KeyError: __dict__ of arg obj doesn't include `id`
        # <arg obj>.id not string
        # Normal use: 1 arg of obj whose __dict__ includes `id`
        # cls.__objects updated with key:'<obj class name>.id', value: obj
        # key:'<obj class name>.id' already in self.__objects

    def test_save(self):
        """Task 5. Store first object
        Tests public instance method `save()`. See also
        TestBaseModel.test_save()

        """
        fs1 = FileStorage()
        # TypeError: any args
        self.assertRaises(TypeError, fs1.save, 'arg')
        # Correct use: no args
        fs1.save()
        # Normal use: called by BaseModel.save(), writes to __file_path
        self.assertTrue(os.path.isfile(fs1._FileStorage__file_path))
        # writes to __file_path a JSON serialized string of __objects
        with open(fs1._FileStorage__file_path, encoding='utf-8') as file:
            contents = file.read()
        self.assertEqual(json.loads(contents), fs1._FileStorage__objects)

    def test_reload(self):
        """Task 5. Store first object
        Tests public instance method `reload()`.

        """
        fs1 = FileStorage()
        # TypeError: any args
        self.assertRaises(TypeError, fs1.reload, 'arg')
        # Normal use: no args, file contains string compatible with json.load()
        fs1.save()
        self.assertTrue(os.path.isfile(fs1._FileStorage__file_path))
        fs1.reload()
        with open(fs1._FileStorage__file_path, encoding='utf-8') as file:
            self.assertEqual(json.load(file), fs1._FileStorage__objects)
        # if __file_path does not exist, do nothing, no exception raised
        fs2 = FileStorage()
        __objects_pre_reload = fs2._FileStorage__objects
        fs2.save()
        os.remove(fs2._FileStorage__file_path)
        fs2.reload()
        self.assertEqual(fs2._FileStorage__objects, __objects_pre_reload)
        # file exists already but doesn't contain JSON format string
        __file_path = fs2._FileStorage__file_path
        content = 'Test text 0123456789abcdefghijklmnopqrstuvwxyz'
        with open(__file_path, 'w+', encoding='utf-8') as file:
            file.write(content)
            print(file.read())
            self.assertRaises(ValueError, fs2.reload)
        # KeyError: object in .json file has no `id` attribute
        # cls.__objects updated with key:'<obj class name>.id', value: obj
        # key:'<obj class name>.id' already in self.__objects

    def test_models___init__1(self):
        """Task 5. Store first object
        Tests `models.__init__` for its use of `FileStorage` on instantiation
        of subclasses.

        Separated into 2 test methods to run `models.__init__` once per method.

        """
        bm1 = BaseModel()
        # `storage` attr created
        from models import storage
        self.assertIsNotNone(storage)
        # `storage` is a `FileStorage` object
        self.assertIsInstance(storage, FileStorage)

    def test_models___init__2(self):
        """Task 5. Store first object
        Tests `models.__init__` for its use of `FileStorage` on instantiation
        of subclasses.

        Separated into 2 test methods to run `models.__init__` once per method.

        """
        # storage.__objects loaded w/ objs from storage.__file_path JSON file
        # !!! could not devise a means to manually rerun models.__init__
        """
        contents = ('{"BaseModel.036b70ef-d24e-4cd7-9df2-7544f95de2da": ' +
        '{"id": "036b70ef-d24e-4cd7-9df2-7544f95de2da", ' +
        '"created_at": "2020-07-10T17:24:01.482145", ' +
        '"updated_at": "2020-07-10T17:24:11.923723", ' +
        '"__class__": "BaseModel"}}')
        __file_path = FileStorage._FileStorage__file_path
        with open(__file_path, 'w', encoding='utf-8') as file:
            file.write(contents)
        from models import storage
        key = 'BaseModel.036b70ef-d24e-4cd7-9df2-7544f95de2da'
        self.assertIn(key, storage._FileStorage__objects.keys())
        self.assertEqual(storage._FileStorage__objects[key].__dict__,
                         BaseModel(**(json.loads(contents)[key])).__dict__)
        """
        pass
