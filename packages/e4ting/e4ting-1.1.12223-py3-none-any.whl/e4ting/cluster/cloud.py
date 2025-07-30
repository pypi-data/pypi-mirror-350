#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting 2023-05-11 16:31:29
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent
import functools,uuid
import ssl,requests
# ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()

from consul import Consul

from e4ting          import log,util
from e4ting.db       import MapListRedis

class Reporter():
    """ 上报者 """
    def __init__(self, key=None, kv=None, url=None, redis=None, schedule=None, wrapper=print, cloud=None):
        self.key = key
        self.kv = kv
        self.url = url
        self.rds_key = redis
        self.schedule = schedule
        self.wrapper  = wrapper
        self.cloud    = cloud
        self.init()

    def init(self):
        if self.kv:
            # 调用远端consul
            self.api = Consul(host=self.cloud.remote, port=80, scheme="http", token=os.environ.get("CONSUL_TOEKN"), verify=False)
            self.remote_url = "e4ting/nodes/{self.kv}".format(self=self)
        elif self.url:
            # 调用远端API上报
            if self.url.startswith(("http://", "https://")):
                self.remote_url = self.url
            else:
                self.remote_url = "https://{self.cloud.remote}{self.url}".format(self=self)
        elif self.key:
            # 调用远端 redis 上报
            self.remote_url = "https://{self.cloud.remote}/push?{self.key}".format(self=self)
        elif self.rds_key:
            self.redis = MapListRedis()
            self.remote_url = self.rds_key
        log.info(self.remote_url)

    @util.redef_return(ret=None)
    def push(self, data):
        if self.kv:
            if type(data) is str:
                payload = data
            else:
                payload = json.dumps(data, indent=2, ensure_ascii=False).encode()
            ret = self.api.kv.put(self.remote_url, payload)
            # self.cloud.push_to_cloud(self.remote_url, payload)
        elif self.url:
            res = requests.post(self.remote_url, json=data, verify=False, headers={"access-token": Const.HONEY_REQUEST_TOKEN})
            assert res.status_code == 200 , "返回码错误 : {res.status_code}".format(res=res)
            ret = res.json()
        elif self.key:
            ret = requests.post(self.remote_url, json=data, verify=False)
        elif self.rds_key:
            ret = self.redis.push(self.remote_url, data, timeout=7200)
        return ret

    def __call__(self):
        import gevent
        while True:
            gevent.sleep(self.schedule)
            log.info("开始调度{self.wrapper.__name__} {self.wrapper.__doc__}".format(self=self))
            self.wrapper()
        return True

class Linsener():
    """ 监听者 """
    def __init__(self, key=None, kv=None, url=None, schedule=None, wrapper=print, cloud=None):
        self.key = key
        self.kv = kv
        self.url = url
        self.schedule = schedule
        self.wrapper  = wrapper
        self.cloud    = cloud
        self.init()

    def init(self):
        if self.kv:
            self.api = Consul(host=self.cloud.remote, port=80, scheme="http", token=os.environ.get("CONSUL_TOEKN"), verify=False)
            self.remote_url = "e4ting/nodes/{self.kv}".format(self=self)
        elif self.url:
            if self.url.startswith(("http://", "https://")):
                self.remote_url = self.url
            else:
                self.remote_url = "https://{self.cloud.remote}{self.url}".format(self=self)
        elif self.key:
            self.redis = MapListRedis()
            self.remote_url = "{self.key}".format(self=self)
        log.info(self.remote_url)

    # @util.redef_return(ret=None)
    def pull(self):
        if self.kv:
            self.index,data0 = self.api.kv.get(self.remote_url)
            data = json.loads(data0["Value"])
        elif self.url:
            data = requests.get(self.remote_url, verify=False)
            data = data.json()
        elif self.key:
            data = self.redis.pop(self.remote_url, timeout=0.05)
            data = json.loads(data or '{}')
        return data

    def __call__(self):
        import gevent
        while True:
            gevent.sleep(self.schedule)
            log.debug("开始调度{self.wrapper.__name__} {self.wrapper.__doc__}".format(self=self))
            self.wrapper()
        return True
        return

class Cloud():
    """云核心接口"""
    def __init__(self, remote="127.0.0.1"):
        # 未设置就使用自己的UID
        # self.uid = uid or WebSetting().node_id
        self.remote = remote
        self.workers = []
        # log.info("初始化 {self.uid}".format(self=self))
        # self.init()

    # @util.redef_return(ret=None)
    # def init(self):
    #     # 初始化 公有云
    #     self.center = None
    #     etc = Setting()
    #     self.center = Consul(host=etc.cloud_host, port=etc.cloud_port, scheme="http", token=etc.cloud_token, verify=False)

    # @util.redef_return(ret=None)
    # def push_to_cloud(self, remote_url, payload):
    #     if self.center is None:
    #         return True
    #     self.center.kv.put(remote_url, payload)

    def add_worker(self, worker):
        self.workers.append(worker)

    def pull(self, key=None, kv=None, url=None, schedule=None):
        # 监听变化
        def _config(function):
            @functools.wraps(function)
            def wrapper_pull(**kwargs):
                # 监听值，并将数据交给回调函数处理
                payload = wrapper_pull.worker.pull()
                # 执行该函数
                # log.info(payload)
                data = function(payload)
                return data
            wrapper_pull.worker = Linsener(key=key, kv=kv, url=url, schedule=schedule, wrapper=wrapper_pull, cloud=self)
            if schedule:
                log.info("添加定时任务 {f.__name__} {f.__doc__}".format(f=function))
                self.add_worker(wrapper_pull.worker)
            return wrapper_pull
        return _config

    def push(self, key=None, kv=None, redis=None, url=None, schedule=None):
        # 推送数据
        def _config(function):
            @functools.wraps(function)
            def wrapper_push(*args, **kwargs):
                # 执行该函数
                data = function(*args, **kwargs)
                # log.info(data)
                # 将该函数返回值发送出去
                ret = wrapper_push.worker.push(data)
                return ret
            wrapper_push.worker = Reporter(key=key, kv=kv, redis=redis, url=url, schedule=schedule, wrapper=wrapper_push, cloud=self)
            if schedule:
                log.info("添加定时任务 {f.__name__} {f.__doc__}".format(f=function))
                self.add_worker(wrapper_push.worker)
            return wrapper_push
        return _config

    def run_forever(self):
        """ 持续运行协程池 """
        from gevent.pool import Pool
        from gevent import Greenlet

        self.pool = Pool(len(self.workers))
        for worker in self.workers:
            g = Greenlet(worker)
            g.start()
            self.pool.add(g)
        self.pool.join()
        log.info("任务池所有任务都已退出")
        return
