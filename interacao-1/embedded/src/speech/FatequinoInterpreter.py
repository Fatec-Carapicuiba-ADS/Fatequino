from subprocess import call
from typing import Union
import speech_recognition as sr
from gtts import gTTS

PORTUGESE_LANGUAGE = 'pt-BR'
STARTING_POINT_WORDS = ("iniciar",)
AUDIO_FILE_NAME = "response.mp3"


class FatequinoInterpreter:

    def __init__(self):
        self.speech_recognizer = sr.Recognizer()
    
    def process_question(self):
        sentence = self.listen_to_speech(10)
        
        if sentence.lower() in STARTING_POINT_WORDS:
            self.speak("Estou te escutando")
            
            sentence = self.listen_to_speech(10)
            
            while not sentence:
                sentence = self.listen_to_speech(10)

            if sentence:
                self.speak("Vou pensar na resposta e já te retorno...")
                # Processamento...
                self.speak(f"Sua pergunta é: {sentence}")
        else:
            self.speak("Para começar a falar comigo, diga a palavra 'iniciar' primeiro")

    def listen_to_speech(self, phrase_time_limit: int=None) -> Union[str, None]:
        sentence = ''

        try:
            with sr.Microphone() as mic:
                self.speech_recognizer.adjust_for_ambient_noise(mic)

                audio_data = self.speech_recognizer.listen(
                    mic,
                    phrase_time_limit=phrase_time_limit
                )
            
                sentence = self.speech_recognizer.recognize_google(
                    audio_data=audio_data,
                    language=PORTUGESE_LANGUAGE
                )
        except sr.UnknownValueError:
            self.speak("Pode repetir, por favor? Não entendi")

        return sentence
    
    def speak(self, text: str, language: str='pt', os_audio_interpreter: str="mpg321"):
        text_to_be_said = gTTS(text=text, lang=language, slow=False)
        text_to_be_said.save(AUDIO_FILE_NAME)
        call(f"{os_audio_interpreter} {AUDIO_FILE_NAME}", shell=True)


if __name__ == '__main__':
    interpreter = FatequinoInterpreter()
    interpreter.process_question()