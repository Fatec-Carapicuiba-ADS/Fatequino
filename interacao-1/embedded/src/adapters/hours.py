from pymongo import MongoClient
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from src.database.sqlite.models.hours import Hours


class HoursAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.hours = Hours()

    def can_process(self, statement):
        subject = ['secretaria', 'biblioteca']
        question = ['abre', 'quando', 'fecha']

        if any(x in statement.text.split() for x in question):
            if any(x in statement.text.split() for x in subject):
                return True

        return False


    def process(self, statement, _):
        rows = self.hours.find_all({})
        parsed_rows = self.hours.to_json_list(rows)

        locals = list(filter(lambda f: f['local'].lower() in statement.text.lower(), parsed_rows))

        if len(locals) == 0:
            return Statement(text='')

        message = ''

        for local in locals:
            message += 'A {} abre {} das {} às {} <br>'.format(
                local['Local'], local['Dias'], local['HorarioInicio'], local['HorarioFim']
            )

        response_statement = Statement(text=message)
        response_statement.confidence = 1 

        return response_statement