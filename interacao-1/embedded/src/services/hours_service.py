import json
import os
from src.database.sqlite.models.hours import Hours

CURRENT_DIR, _ = os.path.split(os.path.abspath(__file__))


class HoursService:
    def __ini__(self) -> None:
        self.hours = Hours()

    def create(self) -> list:
        data = []
        try:
            data = self.hours.find_all({})
            if len(data) > 0:
                return data

            hours = json.loads(open(os.path.join(CURRENT_DIR, '../database/static/horarios.json', 'r')).read())
            for hour in hours:
                row = self.classes.create(self.__to_database_dict(hour))
                data.append(self.classes.to_json(row))
            return data
        except Exception as e:
            raise e

    def __to_database_dict(self, data: dict) -> dict:
        _class = {
            "local": data['Local'],
            "days": data['Dias'],
            "start_time": data['HorarioInicio'],
            "end_time": data['HorarioFim']
        }
        return _class
