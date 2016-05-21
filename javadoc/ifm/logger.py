#-*- coding: utf-8 -*-
import logging.handlers
import ConfigParser,os

class Logger():
    def __init__(self,scriptPath):
        # 创建一个logger
        self.logger = logging.getLogger('ifmlogger')
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        self.fh = logging.handlers.TimedRotatingFileHandler(os.path.join(scriptPath,'ifm.log'),when='d')
        self.fh.setLevel(logging.INFO)
        # 再创建一个handler，用于输出到控制台
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(formatter)
        self.ch.setFormatter(formatter)

    def __addHandlers__(self):
        # 给logger添加handler
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

    def __removeHandlers__(self):
        self.fh.flush()
        self.ch.flush()
        self.logger.removeHandler(self.fh)
        self.logger.removeHandler(self.ch)

    def info(self, msg, *args, **kwargs):
        self.__addHandlers__()
        self.logger.info(msg)
        self.__removeHandlers__()

    def debug(self, msg, *args, **kwargs):
        self.__addHandlers__()
        self.logger.debug(msg)
        self.__removeHandlers__()

    def error(self, msg, *args, **kwargs):
        self.__addHandlers__()
        self.logger.error(msg)
        self.__removeHandlers__()

    def exception(self, msg, *args, **kwargs):
        self.__addHandlers__()
        self.logger.exception(msg)
        self.__removeHandlers__()
