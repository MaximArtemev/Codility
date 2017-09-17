import requests, subprocess, os, logging
from bs4 import BeautifulSoup
import speech_recognition as sr

speech = sr.Recognizer()



def get_location(latitude, longitude):
    try:
        xml = """<?xml version="1.0"?>
            <getNearATM>
                <coordinates>
                    <latitude>{}</latitude>
                    <longitude>{}</longitude>
                </coordinates>
            </getNearATM>
        """.format(latitude, longitude)
        headers = {'Content-Type': 'application/xml'}
        response = requests.post("https://api.open.ru/geocoding/1.0.0/getNearATM", data=xml, headers=headers)
        text = str(response.content, 'utf-8', errors='replace')
        soup = BeautifulSoup(text, 'lxml')
        latitude = float(soup.find_all('latitude')[0].get_text())
        longitude = float(soup.find_all('longitude')[0].get_text())
        return [latitude, longitude]
    except Exception as e:
        return "Something wrong {}".format(e)
    
def get_rates():
    try:
        response = requests.get("https://api.open.ru/getrates/1.0.0/rates/cash")
    except Exception as e:
        return "Произошла ошибка. Попробуйте позже еще раз"
    else:
        selling = []
        buying = []
        for var in response.json()['rates']:
            if var['operationType'] == 'B':
                selling.append({'name':var['curCharCode'],
                                'value':var['rateValue']})
            else:
                buying.append({'name':var['curCharCode'],
                               'value':var['rateValue']})
        return [selling, buying]
    
    
def sound2text(path):
    subprocess.call(['ffmpeg', '-loglevel', 'quiet', '-i', path + '_wb.mp3', path + '_wb.wav'])
    audio = ''
    with sr.AudioFile(path + '_wb.wav') as source:
        audio = speech.record(source)
    os.remove(path+'_wb.mp3')
    os.remove(path+'_wb.wav')
    try:
        text = speech.recognize_google(audio, language='ru')
        return str(text)
    except Exception as e:
        return ("Exception: "+str(e))
    

def get_logger(filename, level):
    logger = logging.getLogger(filename)
    bot = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    bot.setFormatter(formatter)
    logger.addHandler(bot) 
    logger.setLevel(level)
    return logger
