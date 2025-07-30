#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting  2023-05-11 16:31:29
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent
import functools,uuid
import consul

def decode(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        ret = function(*args, **kwargs)
        return ret.get("ModifyIndex", None), json.loads(ret.get("Value"))
    return wrapper

class TaskCore():
    def __init__(self, consul_host, consul_port=8500):
        self.api = consul.Consul(host=consul_host, port=consul_port, token="")
        self.work_list = {}

    @property
    def task_id(self):
        return str(uuid.uuid4())

    @decode
    def wait(self, key, index=None):
        """等待变化"""
        ret = self.api.kv.get(key, index=index)
        index = ret[0]
        if ret[1]:
            return ret[1]

        ret = self.api.kv.get(key, index=index)
        return ret[1]

    def register(self, function):
        # @functools.wraps(function)
        # def wrapper(*args, **kwargs):
        #     # task_data = {
        #     #     'func': function.__name__,
        #     #     'args': args,
        #     #     'kwargs':kwargs,
        #     #     'time': time.time(),
        #     #     'task_id':self.task_id,
        #     # }
        #     self.work_list.update(function.__name__, function)
        #     return task_data
        # return wrapper
        self.work_list[function.__name__] = function

    def task(self, function):
        # def _config(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            task_data = {
                'func': function.__name__,
                'args': args,
                'kwargs':kwargs,
                'time': time.time(),
                'task_id':self.task_id,
            }
            return task_data
        return wrapper
        # return _config

    def do(self, func, time, task_id, args=(), kwargs={}):
        # def _config(function):
        # @functools.wraps(function)
        # def wrapper(func, time, task_id, args=(), kwargs={}):
        #     return function(func, *args, **kwargs)
        # return wrapper
        return self.work_list[func](*args, **kwargs)

    def listen(self, key):
        # 监听变化
        def _config(function):
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                index,task_data = self.wait(key, wrapper.index)
                wrapper.index = index
                data = function(**task_data)
                # self.api.kv.put("e4ting/bot/results/{task_id}".format(**task_data), json.dumps(data), ttl="30s")
                self.api.kv.put("e4ting/bot/results/{task_id}".format(**task_data), json.dumps(data))
            wrapper.key = key
            wrapper.index = None
            return wrapper
        return _config

    def remote(self, key):
        def _config(function):
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                task_data = function(*args, **kwargs)
                # self.api.kv.put(wrapper.key, json.dumps(task_data), ttl="30s")
                self.api.kv.put(wrapper.key, json.dumps(task_data))
                index,payload = self.wait("e4ting/bot/results/{task_id}".format(**task_data))
                return payload
            wrapper.key = key
            return wrapper
        return _config

    def to(self, key):
        def _config(function):
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                ret = function(*args, **kwargs)
                # self.api.kv.put(wrapper.key, json.dumps(ret), ttl="30s")
                self.api.kv.put(wrapper.key, json.dumps(ret))
                return
            wrapper.key = key
            return wrapper
        return _config

    def start(self, key):
        index = None
        while True:
            index,task_data = self.wait(key, index)
            data = self.do(**task_data)
            # self.api.kv.put("e4ting/bot/results/{task_id}".format(**task_data), json.dumps(data), ttl="30s")
            self.api.kv.put("e4ting/bot/results/{task_id}".format(**task_data), json.dumps(data))




