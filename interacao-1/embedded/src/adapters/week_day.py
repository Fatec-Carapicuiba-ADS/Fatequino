from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from datetime import date
from src.commons.utils import Utils
from src.database.sqlite.models.classes import Classes


class WeekDayAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.utils = Utils()
        self.classes = Classes()

    def can_process(self, statement):
        DAYS = ['hoje', 'amanhã', 'amanha', 'segunda', 'terça', 'terca',
                'quarta', 'quinta', 'sexta', 'sábado', 'sabado', 'domingo']

        if any(x in statement.text.lower().split() for x in DAYS):
            return True

        return False

    def process(self, statement, _):
        week_day = self.__get_day(statement.text)
        rows = self.classes.find_all({"week_day": week_day})
        parsed_rows = self.classes.to_json_list(rows)
 
        if len(parsed_rows) == 0:
            resp = Statement(text='{} não tem aulas, mas aproveite para estudar!'.format(
                self.utils.get_week_day(week_day)))
            resp.confidence = 1
            return resp

        message = '{} é dia de '.format(self.utils.get_week_day(week_day))

        for row in parsed_rows:
            message = '{} {} às {} para o ciclo {} com {} <br>'.format(
                message, row['class'], row['startTime'], row['semester'], row['professor'])

        message.replace(',', '.', len(message) - 1)

        msg = Statement(text=message)
        msg.confidence = 1

        return msg

    def __get_day(self, mensagem):
        if 'hoje' in mensagem.lower():
            dia = date.today().weekday() + 2
            print(dia)
            return str(dia if dia < 8 else 1)

        if 'amanhã' in mensagem.lower() or 'amanha' in mensagem.lower():
            dia = date.today().weekday()
            return str(dia + 2 if dia != 6 else 2)

        if 'segunda' in mensagem.lower():
            return '2'

        if 'terca' in mensagem.lower() or 'terça' in mensagem.lower():
            return '3'

        if 'quarta' in mensagem.lower():
            return '4'

        if 'quinta' in mensagem.lower():
            return '5'

        if 'sexta' in mensagem.lower():
            return '6'

        if 'sábado' in mensagem.lower() or 'sabado' in mensagem.lower():
            return '7'

        if 'domingo' in mensagem.lower():
            return '1'
