from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from src.commons.utils import Utils
from src.database.sqlite.models.classes import Classes


class ClassAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.utils = Utils()
        self.classes = Classes()

    def can_process(self, statement):
        subject = ['disciplina', 'matéria', 'aula', 'materias', 'disciplinas', 'sala']
        question = ['qual', 'quando', 'onde', 'quem', 'quais']

        if any(x in statement.text.split() for x in question):
            if any(x in statement.text.split() for x in subject):
                return True

        return False

    def process(self, statement, _):
        rows = self.classes.find_all({})
        parsed_rows = self.classes.to_json_list(rows)

        classes = list(filter(lambda f: f['class'].lower() in statement.text.lower(), parsed_rows))

        if len(classes) == 0:
            return Statement(text='')

        message = ""

        for _class in classes:
            week_day = self.utils.get_week_day(_class['weekDay'])

            message += 'A disciplina {} ocorreu toda(o) {} às {} com o(a) professor(a) {} na sala {}. São {} aulas <br>'.format(
                _class['class'], week_day, _class['startTime'], _class['professor'], _class['roomNumber'], _class['classPerDay']
            )

        response_statement = Statement(text=message)
        response_statement.confidence = 1

        return response_statement
