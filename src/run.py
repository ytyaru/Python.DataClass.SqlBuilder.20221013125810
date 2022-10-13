#!/usr/bin/env python3
# coding: utf8
import importlib
SqlBuilder = importlib.import_module("sql-builder").SqlBuilder
DbTables = importlib.import_module("monaledge-db-tables")
Users = DbTables.Users
Categories = DbTables.Categories
Articles = DbTables.Articles
Comments = DbTables.Comments

print(SqlBuilder().create_table(Users(0, 'xxxxxx', '2000-01-01T00:00:00Z', '2000-01-01T00:00:00Z', 'name1', 'url1')))

'''
Users = importlib.import_module("monaledge-db-tables.Users")
Categories = importlib.import_module("monaledge-db-tables.Categories")
Articles = importlib.import_module("monaledge-db-tables.Articles")
Comments = importlib.import_module("monaledge-db-tables.Comments")
'''
