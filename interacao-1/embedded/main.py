import json
import os
import logging
from chatterbot import ChatBot
from src.bot.fatequino_chatbot import FatequinoChatbot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from src.database.sqlite.ddl.create import Create
from src.database.sqlite.ddl.index import Index
from src.services.class_service import ClassService
from src.services.hours_service import HoursService
from src.commons.utils import Utils
from src.commons.constants import LOGGER
from src.speech.FatequinoInterpreter import FatequinoInterpreter


logging.Formatter(LOGGER['FORMAT'])
CURRENT_DIR, _ = os.path.split(os.path.abspath(__file__))


class Main (object):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.create_table = Create()
        self.index = Index()
        self.class_service = ClassService()
        self.hours_service = HoursService()
        self.utils = Utils()
        self.bot = None
        self.fatequino = None
        self.voice_interpreter = FatequinoInterpreter()

    def run(self):
        try:
            self.__create_db_tables()
            self.__create_db_indexes()
            self.logger.info({"event": "Main.run", "details": "TABLES LOADED"})

            self.__trainn_chatbot()
            self.logger.info({"event": "Main.run", "details": "TRAINN LOADED"})

            self.class_service.create()
            self.hours_service.create()
            self.logger.info({"event": "Main.run", "details": "DATA POPULATED ON DATABASE"})

            self.__menu()
        except Exception as e:
            self.logger.error({"event": "Main.run", "error": str(e)})
            raise e

    def __create_db_tables(self) -> None:
        self.create_table.classes()
        self.create_table.hours()
        self.create_table.unknown_questions()

    def __create_db_indexes(self):
        self.index.create()

    def __trainn_chatbot(self):
        fatequino_instance = self.__get_fatequino()
        fatequino_instance.trainn_bot('chatterbot.corpus.portuguese')
        trainer = ListTrainer(self.__get_chatbot())
        trainer.train(self.__get_trainn_data())

    def __get_trainn_data(self):
        trainn = []
        data = json.loads(
            open(os.path.join(CURRENT_DIR, 'src/bot/trainn/conversas.json'),
                 'r', encoding='utf-8').read())
        for row in data:
            trainn.append(row['question'])
            trainn.append(row['answer'])
        return trainn

    def __get_fatequino(self):
        if self.fatequino is not None:
            return self.fatequino

        self.fatequino = FatequinoChatbot(self.__get_chatbot(), ChatterBotCorpusTrainer)
        return self.fatequino

    def __get_chatbot(self):
        if self.bot is not None:
            return self.bot

        self.bot = ChatBot('Fatequino Chat Bot',
                           storage_adapter='chatterbot.storage.SQLStorageAdapter',
                           logic_adapters=[
                               'chatterbot.logic.BestMatch',
                               {'import_path': 'src.adapters.class.ClassAdapter'},
                               {'import_path': "src.adapters.hours.HoursAdapter"},
                               {'import_path': 'src.adapters.professor.ProfessorAdapter'},
                               {'import_path': "src.adapters.file.FileAdapter"},
                               {'import_path': 'src.adapters.week_day.WeekDayAdapter'},
                           ],
                           filters=['chatterbot.filters.RepetitiveResponseFilter'],
                           input_adapter='chatterbot.input.TerminalAdapter',
                           output_adapter='chatterbot.output.TerminalAdapter'
                           )
        return self.bot

    def __menu(self) -> None:
        fatequino = self.__get_fatequino()
        ALLOWED_OPTIONS = ['1', '2', '3', '4', '0']

        print('Olá eu sou o Fatequino.\n')
        print('Tenho aqui algumas sugestões de perguntas. Pressione o número correspondete a sugestão ou se preferir presione 0 para perguntar!\n\n')
        print('1 - Tem aula hoje?\n')
        print('2 - Onde fica a secretaria?\n')
        print('3 - Quando abre a biblioteca?\n')
        print('4 - Arquivos Fatec\n')
        print('0 - Pergunte-me algo\n')

        try:
            while True:
                question = str(input(">>>>>: "))

                if question == ALLOWED_OPTIONS[0]:
                    self.voice_interpreter.speak(fatequino.sent_message('tem aula hoje'))
                elif question == ALLOWED_OPTIONS[1]:
                    self.voice_interpreter.speak(fatequino.sent_message('Onde fica a secretaria?'))
                elif question == ALLOWED_OPTIONS[2]:
                    self.voice_interpreter.speak(fatequino.sent_message('quando abre a biblioteca'))
                elif question == ALLOWED_OPTIONS[4]:
                    question = self.voice_interpreter.process_question()
                    question = self.utils.remove_special_characters(question)
                    question = self.utils.remove_accent(question)
                    self.voice_interpreter.speak(fatequino.sent_message(question))
                else:
                    print('Ops, não entendi sua opção, poderia digitar novamente?\n')
        except KeyboardInterrupt as e:
            print('\nSaindo...\n')


if __name__ == "__main__":
    main = Main()
    main.run()

# If you're running on Linux, you will need to run thw following commands before installing the requirements:
# sudo apt install portaudio19-dev python3-pyaudio
# sudo apt-get install mpg321
