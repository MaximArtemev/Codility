from chatterbot import ChatBot
import pymorphy2
import speech_recognition as sr


class PythonChatBot:
    def __init__(self, threshold=0.5, read_only=False):
        self.speech = sr.Recognizer()
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
                           read_only=read_only
        )
    
    def normalize_preprocessor(self, text):
        return ' '.join([self.morph.parse(i)[0].normal_form for i in text.lower().split()])
    
    
    def response_sound(self, path):
        audio = ''
        with sr.AudioFile(path) as source:
            audio = self.speech.record(source)
        try:
            text = self.speech.recognize_google(audio, language='ru')
            return self.response(text)
        except Exception as e:
            return ("Exception: "+str(e))
    
        
    def train(self, question, answer):
        self.bot.train([self.normalize_preprocessor(question), answer])
        return 'Спасибо, фраза выучена'
    
    def response(self, question):
        try:
            good_question = self.normalize_preprocessor(question)
            return str(self.bot.get_response(good_question))
        except Exception as e:
            return ("Exception: "+str(e))
    