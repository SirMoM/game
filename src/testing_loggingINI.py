import logging
logger = logging.getLogger('test01')

logging.info("start")

class LoggingTest:
    def __init__(self):
        logging.info("INIT")

    def start(self):
        print(__name__)
        logging.debug('This is a debug message')
        logging.info('This is an info message')
        logging.warning('This is a warning message')
        logging.error('This is an error message')
        logging.critical('This is a critical message')