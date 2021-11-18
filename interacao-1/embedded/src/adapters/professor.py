from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from src.database.sqlite.models.classes import Classes
from src.commons.utils import Utils


class ProfessorAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.classes = Classes()
        self.utils = Utils()

    def can_process(self, statement):
        subject = ['professsor', 'professora', 'prof']
        question = ['qual', 'quando', 'onde', 'quem', 'quais']

        if any(x in statement.text.split() for x in question):
            if any(x in statement.text.split() for x in subject):
                return True

        return False

    def process(self, statement, _):
        rows = self.classes.find_all({})
        parsed_rows = self.classes.to_json_list(rows)
        professors = list(filter(lambda f: f['professor'].lower() in statement.text.lower(), parsed_rows))

        if len(professors) == 0:
            return Statement(text='')

        message = ''

        for professor in professors:
            week_day = self.utils.get_week_day(professor['weekDay'])

            message += 'O(a) professor(a) {} leciona {} na {} às {} na sala {}, '.format(
                professor['professor'], professor['class'], week_day, professor['startTime'], professor['roomNumber']
            )

        response_statement = Statement(text=message)
        response_statement.confidence = 1

        return response_statement
