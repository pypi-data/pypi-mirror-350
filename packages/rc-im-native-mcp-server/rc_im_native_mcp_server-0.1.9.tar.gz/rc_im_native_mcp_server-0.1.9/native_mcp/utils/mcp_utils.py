"""
MCP工具类模块

提供用于MCP服务器的通用工具函数和类
"""
import inspect
import logging
import os
import sys
from typing import Any


class ServerLog:
    __instances = {}
    level = None

    def __init__(self, level=None):
        self.level = level

    @classmethod
    def getLogger(cls, name=os.path.abspath(__name__)) -> logging.Logger:
        if name not in cls.__instances:
            logger = logging.getLogger(name)
            fmt = '%(asctime)s [%(levelname)s] [%(name)s] %(filename)s[line:%(lineno)d] %(message)s'
            formater = logging.Formatter(fmt)
            ch = logging.StreamHandler()
            ch.setLevel(cls.level or ServerLog.__getLogLevel())
            ch.setFormatter(formater)
            logger.addHandler(ch)
            # coloredlogs.install(fmt=fmt, level=cls.level or ServerLog.__getLogLevel(), logger=logger)
            logger.setLevel(cls.level or ServerLog.__getLogLevel())
            cls.__instances[name] = logger
        return cls.__instances[name]

    @staticmethod  # 设置日志等级
    def __getLogLevel():
        if os.environ.get("DEBUG") in ("1", "on", "true"):
            return logging.DEBUG
        if os.environ.get("ERROR") in ("1", "on", "true"):
            return logging.ERROR
        if sys.gettrace():
            return logging.DEBUG
        else:
            return logging.INFO
        
logger = ServerLog.getLogger("mcp_utils")