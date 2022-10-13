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
    birth: datetime = datetime.now()
    value: Decimal = Decimal('0.893')
@dataclass
class TestRecord2:
    id: int
    name: str
    birth: datetime 
    value: Decimal

class TestSqlBuilder(unittest.TestCase):
    def setUp(self): self.target = SqlBuilder()
    def tearDown(self): pass
    def test_table_name_from_class(self):
        self.assertEqual(TestRecord1.__name__, self.target.table_name(TestRecord1))
    def test_table_name_1(self):
        self.assertEqual(TestRecord1.__name__, self.target.table_name(TestRecord1()))
    def test_column_names_from_class(self):
        self.assertEqual(['id', 'name', 'birth', 'value'], self.target.column_names(TestRecord1))
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
    def test_quote(self):
        self.assertEqual('123', self.target.quote(123))
        self.assertEqual('123.45', self.target.quote(123.45))
        self.assertEqual('1', self.target.quote(True))
        self.assertEqual('0', self.target.quote(False))
        self.assertEqual("'ABC'", self.target.quote('ABC'))
        self.assertEqual("'2000-01-01T00:00:00Z'", self.target.quote(datetime.fromisoformat('2000-01-01T00:00:00+00:00')))
        #self.assertEqual("'2000-01-01T00:00:00Z'", datetime.fromisoformat('2000-01-01T00:00:00Z'))
    def test_create_table(self):
        self.assertEqual('create table if not exists TestRecord2 (id integer not null primary key,name text not null,birth text not null,value text not null);', self.target.create_table(TestRecord2))
        
        
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
