#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging


class Logger(object):
    level_relations = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRIT": logging.CRITICAL,
    }
    logger = None

    def __init__(
        self,
        log_path="",
        level="INFO",
    ):
        fmt = "%(asctime)s - %(levelname)s: %(message)s"
        self.logger = logging.getLogger("robot")
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        if log_path != "":
            th = logging.FileHandler(filename=log_path, encoding="utf-8")
        else:
            th = logging.StreamHandler()
        th.setFormatter(format_str)
        self.logger.addHandler(th)
        Logger.logger = self.logger

    @staticmethod
    def get_logger():
        return Logger.logger

    @staticmethod
    def debug(
        msg: object,
    ):
        Logger.logger.debug(msg)

    @staticmethod
    def info(msg: object):
        Logger.logger.info(msg)

    @staticmethod
    def warn(msg: object):
        Logger.logger.warning(msg)

    @staticmethod
    def error(msg: object):
        Logger.logger.error(msg)

    @staticmethod
    def critical(msg: object):
        Logger.logger.critical(msg)
