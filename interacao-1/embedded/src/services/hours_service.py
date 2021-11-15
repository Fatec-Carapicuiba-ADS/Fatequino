import json
import os
from src.database.sqlite.models.hours import Hours

CURRENT_DIR, _ = os.path.split(os.path.abspath(__file__))


class HoursService:
    def __init__(self) -> None:
        self.hours = Hours()

    def create(self) -> list:
        data = []
        try:
            data = self.hours.find_all({})
            if len(data) > 0:
                return data

            hours_data = json.loads(open(os.path.join(CURRENT_DIR, '../database/static/horarios.json'), 'r').read())
            for hour in hours_data:
                row = self.hours.create(self.__to_database_dict(hour))
                print(row)
                data.append(row)
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
