import telegram, logging, subprocess, os, apiwrapper
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from chatbotwrapper import PythonChatBot

train_log = apiwrapper.get_logger('train_bot.log', logging.INFO)
chatbot = PythonChatBot(threshold=0.5)

def start_train(bot, update):    
    bot.send_message(chat_id=update.message.chat_id, text="""Привет! Я готов обучаться!\nПришли сообщением вопрос и ответ на него.\nНе забудь разделить их вот этим симоволом "|" """)
    
def train(bot, update):
    user = update.message.from_user
    text = update.message.text
    train_log.info("text of %s: %s" % (user.first_name, text))
    bot.send_message(chat_id=update.message.chat_id, text="""Спасибо, я постараюсь запомнить.\nЕще больше примеров мне бы не помешало""")
    try:
        train_text = text.split('|')
        chatbot.train(train_text[0], train_text[1])
    except Exception as e:
        train_log.warning("Произошла ошибка -{}- \nНа обучающем тексте -{}-".format(e, text))
        bot.send_message(chat_id=update.message.chat_id, text="Не получилось обучиться. Может быть неправильный формат?")
    else:
        train_log.info("Обучение на обучающем тексте -{}- прошло успешно".format(text))

def run():
    bot_train = telegram.Bot(token='386950793:AAFWQO5Exopgk-WwzHcrKEArN7tVM20OL4A')
    updater_train = Updater(token='386950793:AAFWQO5Exopgk-WwzHcrKEArN7tVM20OL4A')
    dispatcher_train = updater_train.dispatcher

    start_handler_train = CommandHandler('start', start_train)
    text_handler_train = MessageHandler(Filters.text, train)

    dispatcher_train.add_handler(start_handler_train)
    dispatcher_train.add_handler(text_handler_train)

    updater_train.start_polling()
    
    
if __name__ == "__main__":
    run()