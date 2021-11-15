import logging
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from src.commons.constants import LOGGER

logging.Formatter(LOGGER['FORMAT'])


class FileAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.logger = logging.getLogger(__name__)

    def can_process(self, statement):
        subject = ['arquivo', 'arquivos', 'atestado', 'atestados', 'declaracao',
                   'declaracoes', 'documento', 'documentos', 'estagio', 'calendario']

        if any(x in statement.text.lower().split() for x in subject):
            self.logger.info({"event": "FileAdapter.can_process",
                              "canProccess": True, "statement": statement})
            return True

        self.logger.info({"event": "FileAdapter.can_process",
                          "canProccess": False, "statement": statement})
        return False

    def process(self, statement, _):
        message = 'Tenho aqui alguns arquivos que podem ser uteis pra você. Dê uma olhada nos arquivos da Fatec aqui no meu repositório do <a href="https://drive.google.com/drive/folders/1n0GuGD-meSgFtyFqD6r3AH-7_LG4Q72u?usp=sharing">drive</a>'

        msg = Statement(text=message)
        msg.confidence = 1
        
        self.logger.info({"event": "FileAdapter.process", "responseStatement": message})
        return msg
