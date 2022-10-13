#!/usr/bin/env python3
# coding: utf8
import unittest
import importlib
SqlBuilder = importlib.import_module("sql-builder").SqlBuilder
import dataclasses
from dataclasses import dataclass, field, Field
from decimal import Decimal
from datetime import date
from datetime import datetime 
@dataclass
class TestRecord1:
    id: int = 0
    name: str = '山田'
    birth: date = datetime.now()
    value: Decimal = Decimal('0.893')
@dataclass
class TestRecord2:
    id: int
    name: str
    birth: date
    value: Decimal

class TestSqlBuilder(unittest.TestCase):
    def setUp(self): self.target = SqlBuilder()
    def tearDown(self): pass
    def test_table_name_1(self):
        self.assertEqual(TestRecord1.__name__, self.target.table_name(TestRecord1()))
    def test_column_names_1(self):
        self.assertEqual(['id', 'name', 'birth', 'value'], self.target.column_names(TestRecord1()))
    def test_column_index_0(self):
        for id, name in [(0, 'id'), (1, 'name'), (2, 'birth'), (3, 'value')]:
            with self.subTest(f'{name}'):
                self.assertEqual(id, self.target.column_index(TestRecord1(), name))
    def test_to_type(self):
        for actual, expected in [(int, 'integer'), (bool, 'integer'), (float, 'real'), (complex, 'real'), (Decimal, 'text'), (date, 'text')]:
            with self.subTest(f'{actual}'):
                self.assertEqual(expected, self.target.to_type(actual))
    def test_to_const_id(self):
        self.assertEqual('not null primary key', self.target.to_const(TestRecord2.__dataclass_fields__['id']))
        self.assertEqual('not null primary key default 0', self.target.to_const(TestRecord1.__dataclass_fields__['id']))
        #TestRecord1.__dataclass_fields__.values():
        #self.assertEqual('primary key', self.target.to_const(field(name='id', type=int, default=dataclasses.MISSING)))
        #kself.assertEqual('primary key', self.target.to_const(field('id', int, dataclasses.MISSING)))
        #self.assertEqual('primary key', self.target.to_const(Field(name='id')))
        #self.assertEqual('primary key', self.target.to_const(Field('id', int, dataclasses.MISSING)))
        
    """
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    """

if __name__ == '__main__':
    unittest.main()
