from src.database.sqlite.models.unknown_questions import UnknownQuestions


class UnkownQuestionsService:
    def __init__(self) -> None:
        self.unknow_questions = UnknownQuestions()

    def create(self, question: str) -> list:
        try:
            self.unknow_questions.create(self.__to_database_dict(question))
        except Exception as e:
            raise e

    def __to_database_dict(self, question: str) -> dict:
        _unknown_question = {
            "question": question
        }
        return _unknown_question
