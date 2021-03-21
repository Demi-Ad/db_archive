import sqlite3
from typing import List, Generator, Optional
from pprint import pprint
from collections import OrderedDict


class DbSetUp:
    def __init__(self, db_path: str):
        self._conn = sqlite3.connect(db_path)
        self._cursor = self._conn.cursor()

    def clear(self):
        sql = "delete from InputData"
        sql2 = "update sqlite_sequence set seq = 0 where name = 'InputData'"
        self._cursor.execute(sql)
        self._cursor.execute(sql2)
        self._conn.commit()

class DbWriter(DbSetUp):
    def __init__(self, db_path: str):
        super().__init__(db_path)

    def insert(self, *args) -> None:
        sql = "insert into InputData(file_name, extension_name, data, created_at) values (?,?,?,?)"
        self._cursor.execute(sql, args)
        self._conn.commit()

    def __del__(self):
        self._cursor.close()


class DbSelect(DbSetUp):
    def __init__(self, db_path: str):
        super().__init__(db_path)

    def select(self, *args, extension: bool = False, file_name: bool = False):
        if len(args) > 0:
            if extension:
                self.__extension_filter(args)
            elif file_name:
                self.__name_filter(args)
            else:
                self.__normal()
        else:
            self.__normal()

        data = self._cursor.fetchall()
        view_data = dict()
        for index, col in enumerate(data):
            view_data[col[0]] = {'file_name': col[1], 'extension': col[2], "created_at": col[3]}
        pprint(view_data)

    def __extension_filter(self, args):
        sql = "select ID, file_name, extension_name, created_at from InputData where extension_name = (?)"
        self._cursor.execute(sql, args)

    def __name_filter(self, args):
        sql = "select ID, file_name, extension_name, created_at from InputData where file_name LIKE '%' || (?) || '%'"
        self._cursor.execute(sql, args)

    def __normal(self):
        sql = "select ID, file_name, extension_name, created_at from InputData"
        self._cursor.execute(sql)

    def __del__(self):
        self._cursor.close()


class DbOutPut(DbSetUp):
    def __init__(self, db_path: str):
        super().__init__(db_path)
        self.__out_list = []

    def extension_out(self, args):
        sql = "select file_name, extension_name, data from InputData where extension_name = (?)"
        loop = len(args)

        for i in range(loop):
            self._cursor.execute(sql, (args[i],))
            self.__out_list.append(self._cursor.fetchall())

        yield from self.__out_list

    def file_name_out(self, arg):
        sql = "select file_name, extension_name, data from InputData where file_name LIKE '%' || (?) || '%'"
        self._cursor.execute(sql, arg)
        self.__out_list.append(self._cursor.fetchall())

        yield from self.__out_list

    def index_out(self, *args):
        sql = "select file_name, extension_name, data from InputData where ID between (?) and (?)"
        self._cursor.execute(sql, args)
        self.__out_list.append(self._cursor.fetchall())
        yield from self.__out_list

    def out(self, args):
        sql = "select file_name, extension_name, data from InputData where id = (?)"
        for i in args:
            self._cursor.execute(sql, (int(i), ))
            self.__out_list.append(self._cursor.fetchone())
        yield from self.__out_list

    def all_out(self):
        sql = "select file_name, extension_name, data from InputData"
        self._cursor.execute(sql)
        data = self._cursor.fetchall()
        yield from data

    def __del__(self):
        self._cursor.close()
