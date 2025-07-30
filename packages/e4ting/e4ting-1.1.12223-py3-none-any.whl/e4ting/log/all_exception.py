#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    全局未捕获异常处理模块
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

# import os,sys
# import logging
# import logging.handlers

from . import set_syslog,logger,error

def handle_uncaught_exception(exc_type, exc_value, tb):
    msg = ['\n']
    # 循环异常堆栈信息以便找到真正出错的位置，否则所有错误来源都是本函数
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        # 文件名，行数，模块名称
        # msg += '  File "%.500s", line %d, in %.500s\n' % (filename, lineno, name)
        msg.append('  File "%.500s", line %d, in %.500s' % (filename, lineno, name))
        # msg.append('      File "%.500s"')
        tb = tb.tb_next
    # 最后加上错误类型和错误信息
    msg.append('%s: %s\n' % (exc_type.__name__, exc_value))
    # 所有信息组装成一条发送，按回车分割
    text = "\n".join(msg)
    logger.critical(text)
    # enter.excepthook(exc_type, exc_value, tb)

def enter():
    # logger = logging.getLogger("General Logger")

    # 可考虑后期加入配置文件以便于设置发送的IP
    # host = "127.0.0.1"
    # port = 514
    # syslog_handler = logging.handlers.SysLogHandler((host, port), logging.handlers.SysLogHandler.LOG_AUTH)
    # # 设置syslog处理程序的格式和日志级别
    # syslog_handler.setFormatter(logging.Formatter("[%(asctime)s][%(filename)s-%(lineno)d-%(funcName)s "
    #                                               "%(levelname)s] %(message)s\n"))
    # syslog_handler.setLevel(logging.ERROR)
    # # 将syslog处理程序添加到日志记录器
    # logger.addHandler(syslog_handler)

    host = os.environ.get("SYSLOG", "")
    if not host:
        logger.debug("env SYSLOG 未设置")
        return
    # 设置全局异常捕获函数为自定义的新函数
    set_syslog(logger, host=host)
    enter.excepthook = sys.excepthook
    sys.excepthook = handle_uncaught_exception

enter()
