import os
from src import testing_loggingINI

parent_dir = os.path.dirname(os.getcwd())

if __name__ == '__main__':
    print(__name__)
    import logging.config
    logging.config.fileConfig(os.path.join(parent_dir,"logging.ini"), disable_existing_loggers=False)
    test = testing_loggingINI.LoggingTest
    test.start(test)