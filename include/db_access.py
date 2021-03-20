import sqlite3
from typing import List


class DbSetUp:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()


class DbWriter(DbSetUp):
    def __init__(self, db_path: str):
        super().__init__(db_path)

    def insert(self, *args) -> None:
        sql = "insert into InputData(file_name, extension_name, data, created_at) values (?,?,?,?)"
        self.cursor.execute(sql, args)
        self.conn.commit()

    def __del__(self):
        self.cursor.close()


class DbSelect(DbSetUp):
    def __init__(self, db_path: str):
        super().__init__(db_path)

    def select(self, sql: str, *args) -> List:
        self.cursor.execute(sql, args)
        data = self.cursor.fetchall()
        return data

    def __del__(self):
        self.cursor.close()