import json
import os

CURRENT_DIR, _ = os.path.split(os.path.abspath(__file__))


class FatequinoChatbot():
    def __init__(self, bot, Trainer):
        self.bot = bot
        self.trainer = Trainer(self.bot)
        self.conversations = json.loads(open(os.path.join(CURRENT_DIR, 'trainn/conversas.json'), 'r').read())
        self.unknown_conversations = []

    def trainn_bot(self, talk):
        return self.trainer.train(talk)

    def sent_message(self, received_message):
        print(received_message)
        if (float(self.bot.get_response(received_message).confidence) > 0.5):
            return self.bot.get_response(received_message)
        if received_message in self.conversations:
            return self.bot.get_response(received_message)
        else:
            if not (received_message in self.conversations):
                self.unknown_conversations.append(received_message)
                with open(os.path.join(CURRENT_DIR, 'trainn/conversasSemResposta.json'), 'w', encoding='utf-8') as save_conversation:
                    json.dump(self.unknown_conversations, save_conversation,
                              ensure_ascii=False, indent=4, separators=(',', ':'))
                return "Ainda não sei te responder sobre isso, mas irei pesquisar para conseguir te responder."
