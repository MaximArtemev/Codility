import telegram, logging, subprocess, os, apiwrapper
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from chatbotwrapper import PythonChatBot
from loggers import get_logger

test_log = apiwrapper.get_logger('test_bot.log', logging.INFO)
chatbot_predict = PythonChatBot(threshold=0.5, read_only=True)


def start_predict(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="""Привет! Меня еще учат, но кажется что я более-менее готов отвечать на вопросы""")
    
def predict(bot, update):
    user = update.message.from_user
    text = update.message.text
    test_log.info("text of %s: %s" % (user.first_name, text))
    try:
        response = str(chatbot_predict.response(text))
    except Exception as e:
        bot.send_message(chat_id=update.message.chat_id, text="К сожалению что-то пошло не так")
        test_log.warning("Произошла ошибка -{}- \nПытался ответить на -{}-".format(e, text))
    else:
        bot.send_message(chat_id=update.message.chat_id, text=response)
        check_api(bot, update, response)
        test_log.info("Ответ на вопрос -{}- прошел успешно".format(text))
        
def predict_sound(bot, update):
    user = update.message.from_user
    filepath = '{}_question'.format(user.first_name)
    try:
        file_id = update.message.voice.file_id
        newFile = bot.get_file(file_id)
        newFile.download(filepath + '_wb.mp3')
        text = apiwrapper.sound2text(filepath)
        response = str(chatbot_predict.response(text))
    except Exception as e:
        test_log.warning("Произошла ошибка -{}- \nПытался ответить на звук".format(e))
        bot.send_message(chat_id=update.message.chat_id, text="К сожалению что-то пошло не так")
    else:
        bot.send_message(chat_id=update.message.chat_id, text=response)
        check_api(bot, update, response)
        test_log.info("Ответ на вопрос -{}- прошел успешно. Ответ на звук".format(str(text)))
        
def get_user_location(bot, update):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    reply_markup = telegram.ReplyKeyboardRemove()
    bot.send_message(chat_id=update.message.chat_id, text="Он находится вот здесь", reply_markup=reply_markup)
    answer = apiwrapper.get_location(lat, lon)
    if type(answer) == 'str':
        bot.send_message(chat_id=update.message.chat_id, text="Что-то пошло не так. Попробуйте снова")
    else:
        bot.send_location(update.message.chat_id, answer[0], answer[1], text='Ближайший банкомат')
        
def check_api(bot, update, response):
    if response.strip().lower() == 'Найти ближайший банкомат?'.strip().lower():
        reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('Поделиться местоположением', request_location=True)]])
        bot.sendMessage(chat_id=update.message.chat_id, text='Я найду ближайший банкомат, но мне нужно знать ваше местоположение ',
                        reply_markup=reply_markup)
    elif response.strip().lower() == 'Курсы валют?'.strip().lower():
        rates = apiwrapper.get_rates()
        if type(rates) == 'str':
            bot.send_message(chat_id=update.message.chat_id, text=rates)
            return
        selling = "Вот по таким ценам сейчас проходит продажа иностранных валют\n" + '\n'.join(['{} -> {} рублей за штуку'.format(i['name'], i['value']) for i in rates[0]])
        bot.send_message(chat_id=update.message.chat_id, text=selling)
        
        buying = "А вот по таким ценам проходит покупка иностранных валют\n" + '\n'.join(['{} -> {} рублей за штуку'.format(i['name'], i['value']) for i in rates[1]])
        bot.send_message(chat_id=update.message.chat_id, text=buying)

        
        
def run():
    bot_predict = telegram.Bot(token='383933408:AAHmUeE2FX_tODZfiqZUSDMNHYuO-31q1p4')
    updater_predict = Updater(token='383933408:AAHmUeE2FX_tODZfiqZUSDMNHYuO-31q1p4')
    dispatcher_predict = updater_predict.dispatcher
    
    start_handler_predict = CommandHandler('start', start_predict)
    text_handler_predict = MessageHandler(Filters.text & (~Filters.voice) & (~Filters.location), predict)
    voice_handler_predict = MessageHandler(Filters.voice & (~Filters.location), predict_sound)
    location_handler = MessageHandler(Filters.location, get_user_location)
    dispatcher_predict.add_handler(start_handler_predict)
    dispatcher_predict.add_handler(text_handler_predict)
    dispatcher_predict.add_handler(voice_handler_predict)
    dispatcher_predict.add_handler(location_handler)

    updater_predict.start_polling()
    
if __name__ == "__main__":
    run()