#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    公共的日志打印模块
    Add By :e4ting  2023-03-10 14:35:41
"""

import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

from functools  import partial

import logging,logging.handlers

from .otherhandle import set_syslog,OtherHandler

INF0 = (logging.INFO + logging.WARN)>>1
logging.addLevelName(INF0, "INF0")

logging.basicConfig(level=INF0,
                    format="[%(asctime)s][%(funcName)s %(levelname)s] %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler(), OtherHandler()]
                    )

# logging.getLogger('wampy').setLevel(logging.WARN)
# logging.getLogger('autobahn').setLevel(logging.CRITICAL)

# logging.CRITICAL
logger = logging.getLogger()
debug  = logger.debug
info   = partial(logger.log, INF0)
warn   = logger.warn
error  = logger.error

def __getattr__(__level__):
    """仅对python3有用"""
    func = getattr(logger, __level__)
    return func

if __name__ == '__main__':
    # 如果要使用其他 level
    from e4ting import log
    log.warning("test")

