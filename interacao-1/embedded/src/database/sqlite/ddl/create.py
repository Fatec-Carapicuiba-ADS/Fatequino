from src.database.sqlite.connection import SQLite
from sqlite3 import DatabaseError

class Create:
    def __init__(self) -> None:
        self.sqlite = SQLite()

    def hours(self) -> None:
        try:
            query = self.__hours_ddl()
            self.sqlite.execute_script(query)
        except Exception as e:
            raise e
        except DatabaseError as dbe:
            raise dbe

    def classes(self):
        try:
            query = self.__classes_ddl()
            self.sqlite.execute_script(query)
        except Exception as e:
            raise e
        except DatabaseError as dbe:
            raise dbe
    
    def __hours_ddl(self):
        script = '''CREATE TABLE IF NOT EXISTS hours(
            id BIGINT PRIMARY KEY AUTOINCREMENT NOT NULL,
            local VARCHAR(64) NOT NULL,
            days VARCHAR(64) NOT NULL,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL
        )'''

        return script
    
    def __classes_ddl(self):
        script = '''CREATE TABLE IF NOT EXISTS classes(
            id BIGINT PRIMARY KEY AUTOINCREMENT NOT NULL,
            class VARCHAR(64) NOT NULL,
            course VARCHAR(64) NOT NUL,
            period VARCHAR(64) NOT NUL,
            semester BIGINT NOT NUL,
            week_day INTEGER NOT NUL,
            start_time DATETIME NOT NUL,
            professor VARCHAR(128) NOT NUL,
            room_number BIGINT NOT NUL,
            class_per_day INTEGER NOT NULL
        )'''

        return script
