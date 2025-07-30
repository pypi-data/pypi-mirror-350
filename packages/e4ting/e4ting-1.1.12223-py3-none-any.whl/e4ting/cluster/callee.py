#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting e4ting@gmail.com 2023-11-06 17:07:51
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent
import functools
import base64
import errno
import asyncio
from autobahn.asyncio.wamp  import ApplicationSession, ApplicationRunner

from e4ting import util,log
from e4ting.etc import Setting

class AppWorker(ApplicationSession, metaclass=util.Single):
    app = {}
    subs = {}
    nodeid = ""
    async def onDisconnect(self):
        log.info("Disconnected from router.")
        loop = asyncio.get_event_loop()
        loop.stop()

    def onConnectFailure(self, reason):
        log.info("Connection failed:", reason.getErrorMessage())

    async def onJoin(self, details):
        log.info("上线成功")
        # log.info(details)
        for name,function in self.app.items():
            api = 'e4ting.{self.nodeid}.{name}'.format(self=self, name=name, f=function)
            log.info("注册SDK {api} {f.__doc__}".format(api=api, f=function))
            await self.register(function, api)

        for name,function in self.subs.items():
            log.info("订阅 {api} {f.__doc__}".format(api=name, f=function))
            await self.subscribe(function, name)

        # def subscribe(self, name):
        # ret = self.client.subscribe(f'{self.preuri}.{name}')
        # return ret

    @classmethod
    def init_ssl(cls):
        import ssl
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        return ssl_ctx

    @classmethod
    def _init(cls, url=None, realm=None):
        url   = url   or Setting().wampserver
        realm = realm or Setting().realm
        return ApplicationRunner(url=url, realm=realm, ssl=False)

    @classmethod
    def sdk_run(cls):
        runner = cls._init()
        runner.run(cls)

    @classmethod
    def sdk(cls, enable=True):
        # 注册函数
        def _config(function):
            @functools.wraps(function)
            def wrapper(**kwargs):
                return function(**kwargs)
            if enable:
                log.info("待定SDK {f.__name__} {f.__doc__}".format(f=function))
                cls.app[function.__name__] = function
            return wrapper
        return _config

    @classmethod
    def sub(cls, enable=True, name=""):
        # 订阅函数
        def _config(function):
            @functools.wraps(function)
            def wrapper(**kwargs):
                return function(**kwargs)
            if enable:
                log.info("订阅 {name} {f.__doc__}".format(f=function, name=name))
                cls.subs[name] = function
            return wrapper
        return _config

    @classmethod
    def mount(cls, path="/"):
        # 反射文件系统
        from .fuse import FUSE

        FUSE.ROOT = path
        cls.app["access"]   = FUSE.access
        cls.app["chmod"]    = FUSE.chmod
        cls.app["chown"]    = FUSE.chown
        cls.app["getattr"]  = FUSE.getattr
        cls.app["readdir"]  = FUSE.readdir
        cls.app["readlink"] = FUSE.readlink
        cls.app["mknod"]    = FUSE.mknod
        cls.app["rmdir"]    = FUSE.rmdir
        cls.app["mkdir"]    = FUSE.mkdir
        cls.app["statfs"]   = FUSE.statfs
        cls.app["unlink"]   = FUSE.unlink
        cls.app["symlink"]  = FUSE.symlink
        cls.app["rename"]   = FUSE.rename
        cls.app["link"]     = FUSE.link
        cls.app["utimens"]  = FUSE.utimens
        cls.app["open"]     = FUSE.open
        cls.app["create"]   = FUSE.create
        cls.app["read"]     = FUSE.read
        cls.app["write"]    = FUSE.write
        cls.app["truncate"] = FUSE.truncate
        cls.app["flush"]    = FUSE.flush
        cls.app["release"]  = FUSE.release
        cls.app["fsync"]    = FUSE.fsync
