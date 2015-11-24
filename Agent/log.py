# coding=utf-8
# __author__ = 'JakeyWang'

import logging

logfile = 'agent.log'

logger = logging.getLogger()
hdlr = logging.FileHandler(logfile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

class logger_traceback:
    def __init__(self):
        pass

    def error(self, message=''):
        """
        error 日志
        """
        message = self.get_error_info(message)
        logger.error(message)

    def info(self, message=''):
        """
        info 日志
        """
        message = self.get_error_info(message)
        logger.info(message)

    def warning(self, message=''):
        """
        warning 日志
        """
        message = self.get_error_info(message)
        logger.warning(message)

    def debug(self, message=''):
        """
        debug 日志
        """
        message = self.get_error_info(message)
        logger.debug(message)

    def get_error_info(self, message):
        """
                    获取日志信息
        """
        try:
            info = sys.exc_info()
            for filename, lineno, function, text in traceback.extract_tb(info[2]):
                msg = u"%s line: %s in %s" % (filename, lineno, function)
                message = u"%s;%s\n%s\n" % (message, msg, text)
            sys.exc_clear()
            return message
        except Exception, e:
            return message

Logger = logger_traceback()