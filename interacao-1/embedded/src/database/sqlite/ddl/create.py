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

    def unknown_questions(self):
        try:
            query = self.__unknown_questions_ddl()
            self.sqlite.execute_script(query)
        except Exception as e:
            raise e
        except DatabaseError as dbe:
            raise dbe

    def __hours_ddl(self):
        script = '''CREATE TABLE IF NOT EXISTS hours(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            local VARCHAR(64) NOT NULL,
            days VARCHAR(64) NOT NULL,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL
        )'''

        return script

    def __classes_ddl(self):
        script = '''CREATE TABLE IF NOT EXISTS classes(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            class VARCHAR(64) NOT NULL,
            course VARCHAR(64) NOT NULL,
            period VARCHAR(64) NOT NULL,
            semester BIGINT NOT NULL,
            week_day INTEGER NOT NULL,
            start_time DATETIME NOT NULL,
            professor VARCHAR(128) NOT NULL,
            room_number BIGINT NOT NULL,
            class_per_day INTEGER NOT NULL
        )'''

        return script

    def __unknown_questions_ddl(self):
        script = '''CREATE TABLE IF NOT EXISTS unknown_questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            quetion VARCHAR(364) NOT NULL
        )'''

        return script
