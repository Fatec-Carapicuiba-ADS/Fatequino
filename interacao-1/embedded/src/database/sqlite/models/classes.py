from typing import Any
from src.database.sqlite.models.dao import DAO
from src.database.sqlite.connection import SQLite

OPTIONS = {
    "TABLE": "classes"
}


class Classes(DAO):
    def __init__(self) -> None:
        super().__init__()
        self.sqlite = SQLite()

    def find_one(self, where: dict) -> tuple:
        criteria = []
        try:
            for key in where:
                criteria.append('{}=:{}'.format(key, key))

            query = 'SELECT * FROM hours WHERE {} LIMIT 1'.format(' AND '.join(criteria))
            row = self.sqlite.execute(query)
            return row
        except Exception as e:
            raise e

    def find_all(self, where: dict) -> tuple:
        criteria = []
        try:
            for key in where:
                criteria.append('{}=:{}'.format(key, key))

            query = 'SELECT * FROM {0} WHERE {1}'.format(OPTIONS['TABLE'], ' AND '.join(criteria))
            row = self.sqlite.execute(query)
            return row
        except Exception as e:
            raise e

    def create(self, data: dict) -> tuple:
        try:
            query = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(OPTIONS['TABLE'], ','.join(data.keys()), ','.join(data.values()))
            row = self.sqlite.execute(query)
            return row
        except Exception as e:
            raise e
    
    def to_json(self, data: tuple) -> dict:
        result = {
            "class": data[1],
            "course": data[2],
            "period": data[3],
            "semester": data[4],
            "weekDay": data[5],
            "startTime": data[6],
            "professor": data[7],
            "roomNumber": data[8],
            "classPerDay": data[9]
        }
        return result

    def to_json_list(self, data: list) -> list:
        results = []
        for row in data:
            results.append(self.to_json(row))
        return results
