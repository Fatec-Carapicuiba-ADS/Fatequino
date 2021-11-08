from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


def obter_dia_da_semana(dia):
    if dia == '1':
        return 'Domingo'
    if dia == '2':
        return 'Segunda'
    if dia == '3':
        return 'Terça'
    if dia == '4':
        return 'Quarta'
    if dia == '5':
        return 'Quinta'
    if dia == '6':
        return 'Sexta'
    if dia == '7':
        return 'Sábado'

class ProfessorAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        subject = ['professsor', 'professora', 'prof']
        question = ['qual', 'quando', 'onde', 'quem', 'quais']

        if any(x in statement.text.split() for x in question):
            if any(x in statement.text.split() for x in subject):
                return True

        return False


    def process(self, statement, _):
        # TODO: Continuar Refatoração para implementação na Raspeberry PI
        rows = []
        professores = list(filter(lambda f: f['professor'].lower() in statement.text.lower(), rows))

        if len(professores) == 0:
            return Statement(text='')

        mensagem = ''

        for professor in professores:
            dia = obter_dia_da_semana(professor['Dia'])

            mensagem += 'O(a) professor(a) {} leciona {} na {} às {} na sala {} <br>'.format(
                professor['Professor'], professor['Disciplina'], dia, professor['Horario'], professor['Sala']
            )

        response_statement = Statement(text=mensagem)
        response_statement.confidence = 1 

        return response_statement
