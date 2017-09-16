import logging


def get_logger(filename, level):
    logger = logging.getLogger(filename)
    bot = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    bot.setFormatter(formatter)
    logger.addHandler(bot) 
    logger.setLevel(level)
    return logger