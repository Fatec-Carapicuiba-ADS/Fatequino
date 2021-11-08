import sqlite3
from src.commons.constants import DB


class SQLite:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(DB['NAME'])
        self.cursor = None

    def execute(self, query: str, data: dict):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(query, data)
            return self.cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            if self.cursor != None:
                self.cursor.close()

    def execute_script(self, query: str):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.executescript(query)
            return self.cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            if self.cursor != None:
                self.cursor.close()