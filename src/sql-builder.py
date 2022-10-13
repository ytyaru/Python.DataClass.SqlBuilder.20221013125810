#!/usr/bin/env python3
# coding: utf8
import dataclasses 
from decimal import Decimal
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import typing
class SqlBuilder:
    def table_name(self, data):
        if isinstance(data, type): return data.__name__
        else: return type(data).__name__
    def column_names(self, data): return list(data.__dataclass_fields__.keys())
    def column_index(self, data, name): return self.column_names(data).index(name)
    def to_type(self, type): # INTEGER,REAL,TEXT,BLOB,NULL
        if type is int or type is bool: return 'integer'
        elif type is float or type is complex: return 'real'
        elif type is list: return 'blob'
        else: return 'text'
        '''
        match type:
            case int(): return 'integer'
            case bool(): return 'integer'
            case float() | complex(): return 'real'
            #case list[int]: return 'blob'
            case _: return 'text'
        '''
        '''
        match type:
            case int: return 'integer'
            case bool: return 'integer'
            case float | complex: return 'real'
            #case list[int]: return 'blob'
            case _: return 'text'
        '''
    def to_const(self, f): # primary key, unique, not null, check(), default
        consts = ['not null']
        if 'id' == f.name: consts.append('primary key')
        if f.type is bool: consts.append(f"check({f.name} = 0 or {f.name} = 1)")
        if type(f.default) is not dataclasses._MISSING_TYPE: consts.append(f"default {f.default}")
        if isinstance(f.metadata, list): consts += [self.expand_metadata(k,v) for k,v in f.metadata.items()]
        #if isinstance(f.metadata, list): consts += f.metadata
        return ' '.join(consts)
    def from_iso(self, iso): return datetime.fromisoformat(iso.replace('Z', '+00:00'))
    def quote(self, v):
        t = type(v)
        #print(v, t)
        if t is int or t is float: return str(v)
        elif t is bool: return str(1 if v else 0)
        elif t is datetime: return f"'{v.isoformat().replace('+00:00', 'Z')}'"
        else: return f"'{v}'"
        '''
        print(v, type(v), isinstance(v, bool))
        if isinstance(v, (int, float)): return str(v)
        elif isinstance(v, bool): return str(1 if v else 0)
        elif isinstance(v, bool): return str(1 if v else 0)
        elif isinstance(v, (datetime, date, time)): return v.isoformat() 
        else: return f"'{v}'"
        '''
        '''
        if isinstance(v, (int, float)):
            print('int,float-------')
            return str(v)
        elif isinstance(v, bool):
            print('bool-------')
            return str((1 if v else 0))
        elif isinstance(v, (datetime, date, time)):
            print('datetime, date, time-------')
            return v.isoformat() 
        #else: return f"'{v}'"
        else:
            print('else-------')
            return f"'{v}'"
        '''
        '''
        match type(v):
            case int() | float(): return str(v)
            #case complex(): return return ?
            case bool(): return str(1 if v else 0)
            case _: return f"'{v}'"
        '''
    def expand_metadata(self, k, v):
        match key:
            case 'PK': return 'primary key'
            case 'UK': return 'unique'
            case 'FK': 
                w = f.metadata[key].split(' ')
                return f'references {w[1]}({w[2]})'
            case 'CK': return f'check ({f.metadata[key]})'
            case _: return v
    def create_table(self, data):
        #for name, type in data.__annotations__.entries():
        #map(lambda f: [f.name, self.to_type(f.type), self.to_const(f)], data.__dataclass_fields__.values())
        #map(lambda f: [f.name, self.to_type(f.type()), self.to_const(f)], data.__dataclass_fields__.values())
        columns = []
        for field in data.__dataclass_fields__.values():
            #print(field)
            columns.append(' '.join([field.name, self.to_type(field.type), self.to_const(field)]))
        return f"create table if not exists {self.table_name(data)} ({','.join(columns)});"
    def insert(self, data):
        return f"insert into {self.table_name(data)} values ({','.join([getattr(data, key) for k in data.__dataclass_fields__.keys() if type(v) is not dataclasses._MISSING_TYPE])});"
    def update(self, data, where):
        values = ','.join([f'{k} = {self.quote(v)}' for k,v in data.__dataclass_fields__.items() if type(v) is not dataclasses._MISSING_TYPE])
        conds = ','.join([f'{k} = {self.quote(v)}' for k,v in where.__dataclass_fields__.items() if type(v) is not dataclasses._MISSING_TYPE])
        return f"update {self.table_name(data)} set {values} where {conds};"
    def delete(self, where):
        conds = ','.join([f'{k} = {self.quote(v)}' for k,v in where.__dataclass_fields__.items() if type(v) is not dataclasses._MISSING_TYPE])
        return f"delete from {self.table_name(data)} where {conds};"
    def clear(self): return f"delete from {self.table_name(data)};"
    #def insert_preper(self, data): # sqlite3.exec(sql, params)の引数をタプルで返す
    #    return (f"insert into {self.table_name(data)} values ({','.join(list('?' * len(data.__dataclass_fields__.keys())))});", data.__dataclass_fields__.values())
    def _get_exists_kvs(self, data): return [(k,v) for k,v in data.__dataclass_fields__.items() if type(v) is not dataclasses._MISSING_TYPE]
    def _get_exists_keys(self, data): return [k for k,v in data.__dataclass_fields__.items() if type(v) is not dataclasses._MISSING_TYPE]
    def _get_exists_values(self, data): return [v for k,v in data.__dataclass_fields__.items() if type(v) is not dataclasses._MISSING_TYPE]
    def insert_preper(self, data): # sqlite3.exec(sql, params)の引数をタプルで返す
        #ks = self._get_exists_keys(data)
        ks = ','.join(list('?' * len(data.__dataclass_fields__.keys())))
        vs = self._get_exists_values(data)
        return (f"insert into {self.table_name(data)}({','.join(ks)}) values ({','.join(vs)})", vs)
        #kvs = self._get_exists_cols(data)
        #ks = [k for k,v in kvs]
        #vs = [v for k,v in kvs]
        #datas = [(k,v) for k,v in data.__dataclass_fields__.items() if type(v) is not dataclasses._MISSING_TYPE]
        #return (f"insert into {self.table_name(data)} values ({','.join(list('?' * len(data.__dataclass_fields__.keys())))});", data.__dataclass_fields__.values())
    def update_preper(self, data, where): # sqlite3.exec(sql, params)の引数をタプルで返す
        dks = self._get_exists_keys(data)
        dvs = self._get_exists_values(data)
        wks = self._get_exists_keys(where)
        wvs = self._get_exists_values(where)
        return (f"update {self.table_name(data)} set {','.join([f'{k} = ?' for k in dks])} where {','.join([f'{k} = ?' for k in wks])};", dvs + wvs)
        """
        datas = [(k,v) for k,v in data.__dataclass_fields__.items() if type(v) is not dataclasses._MISSING_TYPE]
        conds = [(k,v) for k,v in where.__dataclass_fields__.items() if type(v) is not dataclasses._MISSING_TYPE]
        return (f"update {self.table_name(data)} set {','.join([f'{k} = ?' for k,v in datas])} where {','.join([f'{k} = ?' for k,v in conds])};", )
        #values = ','.join([f'{k} = ?' for k,v in data.__dataclass_fields__.items() if type(v) is not dataclasses._MISSING_TYPE])
        #conds = ','.join([f'{k} = ?' for k,v in where.__dataclass_fields__.items() if type(v) is not dataclasses._MISSING_TYPE])
        #return (f"update {self.table_name(data)} set {values} where {conds};", )
        #return (f"update {self.table_name(data)} set {','.join([f'{k} = ?' for k,v in data.__dataclass_fields__.items() if type(v) is not dataclasses._MISSING_TYPE])};", data.__dataclass_fields__.values())
        """
