#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting  2023-03-10 17:23:44
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent
from functools import partial

from e4ting                  import log,util
# from celerys.app             import app

def imports(app):
    globals()["app"] = app
    for mod in app.conf['include']:
        try:
            exec('from {mod} import *'.format(mod=mod), globals())
            log.info('from {mod} import *'.format(mod=mod))
        except ImportError:
            log.info("from {mod} import * 失败".format(mod=mod))
            pass

class TaskTemplate(object):
    def __init__(self, second=10, queue=None):
        self.queue = queue

        # 阻塞多少秒返回
        self.timeout = second

# 单词是匿名的意思
class Anon(TaskTemplate):
    # async 异步调用，完全不关心集群中是否有节点执行此任务
    def apply_async(self, func, *args, **kwargs):
        if self.queue is None:
            return globals()["app"].send_task(func, args=args, kwargs=kwargs)
        return globals()["app"].send_task(func, args=args, kwargs=kwargs, queue=self.queue)

    def __getattr__(self, func):
        return partial(self.apply_async, func)


class Async(Anon):
    ...
    # async 异步调用
    # def apply_async(self, func, *args, **kwargs):
    #     if self.queue is None:
    #         return func.apply_async(args=args, kwargs=kwargs)
    #     return func.apply_async(args=args, kwargs=kwargs, queue=self.queue)

    # def __getattr__(self, func):
    #     assert func in globals(), "未定义此函数"
    #     return partial(self.apply_async, globals()[func])


class Block(Async):
    # block 阻塞调用

    def run(self, func, *args, **kwargs):
        if self.timeout is None or self.timeout <= 0:
            return self.apply_async(func, *args, **kwargs).get()
        return self.apply_async(func, *args, **kwargs).get(self.timeout)

    def __getattr__(self, func):
        from celerys.tasks      import task
        assert func in task.globals(), "未定义此函数"
        return partial(self.run, task.globals()[func])
