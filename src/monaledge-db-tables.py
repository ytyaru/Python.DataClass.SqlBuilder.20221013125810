#!/usr/bin/env python3
# coding: utf8
from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime 
#@dataclass(slots=True)
@dataclass
class Users:
    id: int
    address: str = field(metadata={'UK':True})
    created: datetime 
    updated: datetime 
    name: str
    icon_image_path: str
#@dataclass(slots=True)
@dataclass
class Categories:
    id: int
    name: str = field(metadata={'UK':True})
#@dataclass(slots=True)
@dataclass
class Articles:
    id: int
    created: datetime 
    updated: datetime 
    title: str
    sent_mona: Decimal
    access: int
    ogp_path: str
    category_id: int
    content: str
#@dataclass(slots=True)
@dataclass
class Comments:
    id: int
    article_id: int
    created: datetime 
    updated: datetime 
    user_id: int
    content: str

"""
user1 = Users(0, 'xxxxxx', '2000-01-01T00:00:00Z', '2000-01-01T00:00:00Z', 'name1', 'url1')
print(dir(user1))
print(user1)
print(user1.__dict__)
print(user1.__dict__.keys())
print(user1.name)
#print(user1['name']) #TypeError: 'Users' object is not subscriptable
#print(user1.__getattr__('name')) # AttributeError: 'Users' object has no attribute '__getattr__'. Did you mean: '__setattr__'?
print(getattr(user1, 'name'))
"""
