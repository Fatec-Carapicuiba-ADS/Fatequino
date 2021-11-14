from src.database.sqlite.connection import SQLite
from sqlite3 import DatabaseError

class Index():
    def __init__(self) -> None:
        self.sqlite = SQLite()

    def create(self):
        try:
            for script in self.__classes_idx_list():
                self.sqlite.execute_script(script)
        except Exception as e:
            raise e
        except DatabaseError as dbe:
            raise dbe

    def __classes_idx_list(self) -> list:
        script = []
        script.append('''CREATE INDEX IF NOT EXISTS CLASSES_WEEK_DAY_IDX ON classes(week_day)''')
        script.append('''CREATE INDEX IF NOT EXISTS CLASSES_SEMESTER_IDX ON classes(semester)''')
        script.append('''CREATE INDEX IF NOT EXISTS CLASSES_PERIOD_IDX ON classes(period)''')
        script.append('''CREATE INDEX IF NOT EXISTS CLASSES_PROFESSOR_IDX ON classes(professor)''')
        return script