from chatterbot import ChatBot
import pymorphy2
import speech_recognition


class PythonChatBot:
    def __init__(self, threshold=0.5):
        self.speech = speech_recognition.Recognizer()
        self.morph = pymorphy2.MorphAnalyzer()
        self.bot = ChatBot('Norman',
                           storage_adapter="chatterbot.storage.SQLStorageAdapter",
                           logic_adapters=[
                               {
                                   'import_path': 'chatterbot.logic.BestMatch'
                               },
                               {
                                   'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                                   'threshold': threshold,
                                   'default_response': 'Я недоучился, поэтому не могу понять о чем речь'
                               }
                           ],
                           trainer='chatterbot.trainers.ListTrainer',
        )
    
    def normalize_preprocessor(self, text):
        return ' '.join([self.morph.parse(i)[0].normal_form for i in text.split()])
    
    
    def response_sound(self, path):
        with speech_recognition.AudioFile(path) as source:
            audio = self.speech.record(source)
        try:
            return self.response(self.speech.recognize_google(audio, language='ru'))
        except Exception as e:
            return ("Exception: "+str(e))
    
        
    def train(self, question, answer):
        self.bot.train([self.normalize_preprocessor(question), answer])
        return 'Спасибо, фраза выучена'
    
    def response(self, question):
        try:
            return str(self.bot.get_response(question))
        except Exception as e:
            return ("Exception: "+str(e))
    