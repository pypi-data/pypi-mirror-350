#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    其他发送模块
    Add By :e4ting  2023-03-10 14:35:41
"""

import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

import logging, logging.handlers

def set_syslog(logger, host="172.31.50.25", port=514):
    import syslog
    address=(host, port)
    syslog_handler = logging.handlers.SysLogHandler(address, logging.handlers.SysLogHandler.LOG_AUTH)
    # 设置syslog处理程序的格式和日志级别
    syslog_handler.setFormatter(logging.Formatter("[%(asctime)s][%(funcName)s %(levelname)s] %(message)s\n"))
    syslog_handler.setLevel(logging.CRITICAL)
    # 将syslog处理程序添加到日志记录器
    logger.addHandler(syslog_handler)
    logger.info("已添加syslog {address}".format(address=address))

class OtherHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super(OtherHandler, self).__init__(level=level)

    def emit(self, record):
        # 判断日志级别是否符合条件
        if record.levelno >= logging.ERROR:
            self.dosomething(record.msg)

    def dosomething(self, msg):
        # print("严重错误", record.msg)
        pass
