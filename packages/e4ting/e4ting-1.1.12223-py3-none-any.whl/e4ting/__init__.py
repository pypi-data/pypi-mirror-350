#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    一些公共的工具
    Add By :e4ting  2023-03-10 14:35:41
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent
# from log.general_log import handle_uncaught_exception

# 强迫 接管系统未知异常
from .log import all_exception

class Error(Exception):
    def __init__(self, payload={}, code=500):
        self.__dict__["code"] = 500
        self.__dict__["data"] = payload

    def __iter__(self):
        # 返回一个迭代器对象
        return iter(self.__dict__.items())

import builtins
__builtins__["Error"] = Error

