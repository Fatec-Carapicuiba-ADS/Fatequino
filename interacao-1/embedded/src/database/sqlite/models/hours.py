from src.database.sqlite.models.dao import DAO
from src.database.sqlite.connection import SQLite

OPTIONS = {
    "TABLE": "hours"
}


class Hours(DAO):
    def __init__(self) -> None:
        super().__init__()
        self.sqlite = SQLite()

    def find_one(self, where: dict) -> tuple:
        criteria = []
        try:
            for key in where:
                criteria.append('{}=:{}'.format(key, key))

            query = 'SELECT * FROM {0} WHERE {1} LIMIT 1'.format(OPTIONS['TABLE'], ' AND '.join(criteria))
            row = self.sqlite.execute(query, where)
            return row
        except Exception as e:
            raise e

    def find_all(self, where: dict) -> tuple:
        criteria = []
        try:
            query = 'SELECT * FROM {0}'.format(OPTIONS['TABLE'])
            
            for key in where:
                criteria.append('{}=:{}'.format(key, key))
            if where != {}:
                query +=  ' WHERE {}'.format(' AND '.join(criteria))

            row = self.sqlite.execute(query, where)
            return row
        except Exception as e:
            raise e

    def create(self, data: dict) -> tuple:
        try:
            query = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(
                OPTIONS['TABLE'], ','.join(data.keys()), ','.join(list(map(lambda x: '\'{}\''.format(str(x)), data.values()))))
            row = self.sqlite.execute_script(query)
            return row
        except Exception as e:
            raise e

    def to_json(self, data: tuple) -> dict:
        result = {
            "local": data[1],
            "days": data[2],
            "startTime": data[3],
            "endTime": data[4],
        }
        return result

    def to_json_list(self, data: list) -> list:
        results = []
        for row in data:
            results.append(self.to_json(row))
        return results
