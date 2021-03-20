import sqlite3
from typing import List


class DbSetUp:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()


class DbWriter(DbSetUp):
    def __init__(self, path: str):
        super().__init__(path)

    def insert(self, sql: str, *args) -> None:
        self.cursor.execute(sql, args)
        self.conn.commit()

    def __del__(self):
        self.cursor.close()


class DbSelect(DbSetUp):
    def __init__(self, path: str):
        super().__init__(path)

    def select(self, sql: str, *args) -> List:
        self.cursor.execute(sql, args)
        data = self.cursor.fetchall()
        return data

    def __del__(self):
        self.cursor.close()