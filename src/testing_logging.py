import logging
import tempfile
import os

# print os tempdir
print(tempfile.gettempdir())

# not writing events to a file
##has to be set on info, else no informations are available in the files
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Start LoggerTest')
# some information here
info = {'noah': 19, 'jeff': 22}
logger.debug('Current info: %s', info)
logger.info('Updating info ...')
# set new info
info = {'noah': 20, 'jeff': 23}
logger.debug('Updated Info: %s', info)
logger.info('Finish updating records')


# create specific filehandlers
handler_DEBUG =logging.FileHandler(os.path.join(tempfile.gettempdir(), "GameLog_DEBUG.log"))
handler_INFO = logging.FileHandler(os.path.join(tempfile.gettempdir(), "GameLog_INFO.log"))
handler_WARN = logging.FileHandler(os.path.join(tempfile.gettempdir(), "GameLog_WARN.log"))
handler_ERR = logging.FileHandler(os.path.join(tempfile.gettempdir(), "GameLog_ERR.log"))

handler_DEBUG.setLevel(logging.DEBUG)
handler_INFO.setLevel(logging.INFO)
handler_WARN.setLevel(logging.WARNING)
handler_ERR.setLevel(logging.ERROR)


# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler_DEBUG.setFormatter(formatter)
handler_INFO.setFormatter(formatter)
handler_WARN.setFormatter(formatter)
handler_ERR.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler_DEBUG)
logger.addHandler(handler_INFO)
logger.addHandler(handler_WARN)
logger.addHandler(handler_ERR)

logger.info("this is an info test")
logger.debug("this is a debug test")
logger.warning("this is a warning test")
logger.error("this is an error test")


#works good --> all levels can be written to diffrent files and basiologging level should be INFO




