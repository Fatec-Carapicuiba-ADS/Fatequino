import json
import os
from chatterbot import ChatBot
from src.bot.fatequino_chatbot import FatequinoChatbot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from src.database.sqlite.ddl.create import Create
from src.database.sqlite.ddl.index import Index
from src.services.class_service import ClassService
from src.services.hours_service import HoursService
from src.commons.utils import Utils

CURRENT_DIR, _ = os.path.split(os.path.abspath(__file__))


class Main (object):
    def __init__(self) -> None:
        super().__init__()
        self.create_table = Create()
        self.index = Index()
        self.class_service = ClassService()
        self.hours_service = HoursService()
        self.utils = Utils()
        self.bot = None
        self.fatequino = None

    def run(self):
        try:
            self.__create_db_tables()
            self.__create_db_indexes()

            self.__trainn_chatbot()

            self.class_service.create()
            self.hours_service.create()

            self.__menu()
        except Exception as e:
            print({"event": "Main.run", "error": str(e)})
            raise e

    def __create_db_tables(self) -> None:
        self.create_table.classes()
        self.create_table.hours()

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
            open(os.path.join(CURRENT_DIR, '.src/bot/trainn/conversas.json'),
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

        print('Olá eu sou o Fatequino.\n')
        print('Tenho aqui algumas sugestões de perguntas. Pressione o número correspondete a sugestão ou se preferir presione 0 para perguntar!\n\n')
        print('1 - Tem aula hoje?\n')
        print('2 - Quando abre a secretaria?\n')
        print('3 - Quando abre a biblioteca?\n')
        print('4 - Arquivos Fatec\n')
        print('0 - Pergunte-me algo\n')

        while True:
            switch = {
                "1": self.fatequino.sent_message('tem aula hoje'),
                "2": self.fatequino.sent_message('quando abre a secretria'),
                "3": self.fatequino.sent_message('quando abre a biblioteca'),
                "4": self.fatequino.sent_message('arquivos fatec'),
                "0": input("Qual a sua dúvida?")
            }
            question = str(input(">>>>>: "))

            if question == "0":
                question = str(switch[question])
                question = self.utils.remove_special_characters(question)
                question = self.utils.remove_accent(question)
                print(self.fatequino.sent_message(question))
            
            response = switch[str(question)] or "Ops, não entendi sua pergunta, poderia digitar novamente?"
            print(response)


if __name__ == "main":
    main = Main()
    main.run()