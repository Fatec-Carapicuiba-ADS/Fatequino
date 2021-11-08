class Utils():
    def get_week_day(day: str):
        WEEK_DAYS = {
            "1": "Domingo",
            "2": "Segunda",
            "3": "Terça",
            "4": "Quarta",
            "5": "Quinta",
            "6": "Sexta",
            "7": "Sábado"
        }
        return WEEK_DAYS[day]
