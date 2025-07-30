#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    数据库操作的公共入口
    Add By :e4ting  2023-03-10 14:35:41
"""
import sys, os
import json, time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

from .utilredis import RedisDB,MapListRedis,MapDictRedis,INRC
from .pymongos  import mongodb