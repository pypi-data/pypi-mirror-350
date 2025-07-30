#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    公共配置加载入口
    Add By :e4ting  2023-03-10 14:35:41
"""
import sys, os
import json, time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

from e4ting import util

class Setting():
    def __init__(self):
        # 配置有可能发生变化，应该时刻保持最新
        pass

    @property
    def wampserver(self):
        return os.environ.get("WAMP_SERVER")

    @property
    def authid(self):
        return os.environ.get("WAMP_AUTHID")

    @property
    def ticket(self):
        return os.environ.get("WAMPYSECRET")

    @property
    def realm(self):
        return os.environ.get("WAMP_REALM")

    @property
    def timeout(self):
        return 30

    @classmethod
    @util.redef_return(ret={})
    def yaml_to_json(cls, fname):
        yaml = yamlManage(fname)
        return yaml.content
