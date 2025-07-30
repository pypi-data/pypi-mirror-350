#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting e4ting@gmail.com 2023-07-13 14:01:45
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent
import functools
from functools import partial

from swampyer import WAMPClient,WAMPClientTicket

from e4ting                 import util,log
from e4ting.etc             import Setting

class WAMP(WAMPClientTicket, metaclass=util.Single):
    def __init__(self, *args, **kwargs):
        # strace()
        super(WAMP, self).__init__(*args, **kwargs)
        self.start()

    def __del__(self):
        log.debug("wamp 退出 {self.url}, {self.realm}".format(self=self))
        if not self.is_disconnected():
            self.disconnect()
        self.shutdown()

class WAMP1(WAMPClient, metaclass=util.Single):
    def __init__(self, *args, **kwargs):
        # strace()
        super(WAMP1, self).__init__(*args, **kwargs)
        self.start()

    def __del__(self):
        log.debug("wamp 退出 {self.url}, {self.realm}".format(self=self))
        if not self.is_disconnected():
            self.disconnect()
        self.shutdown()

class NodeControl():
    def __init__(self, nodeid=None):
        self.nodeid = nodeid   #    nodeid.lower()
        if Setting().authid:
            self.client = WAMP(url=Setting().wampserver,
                             realm=Setting().realm,
                          username=Setting().authid,
                          password=Setting().ticket,
                           timeout=Setting().timeout)
        else:
            self.client = WAMP1(url=Setting().wampserver,
                             realm=Setting().realm,
                           timeout=Setting().timeout)
        # log.info(f"已连接 {self.nodeid}")

    def callback(self, func_name="", *args, **kwargs):
        uri = ".".join(["e4ting", str(self.nodeid), func_name])
        log.info(uri)
        log.info(args)
        return self.client.call(uri, *args, **kwargs)

    def publish(self, name, *data):
        log.info(f'[{name}] ==> {data}')
        ret = self.client.publish(name, {'acknowledge':False}, args=data)
        return ret

    def subscribe(self, name):
        ret = self.client.subscribe(f'{self.preuri}.{name}')
        return ret

    def register(self, name, func):
        uri = ".".join(["e4ting", str(self.nodeid), name])
        log.info(("register : ", uri))
        ret = self.client.register(uri, func)
        return ret

    # def nodes(self):
    #     return self.client.not_me(self.call('wamp.session.list'))

    def get(self, _id):
        res = self.client.call('wamp.registration.get', _id)
        return res

    def list(self):
        # strace()
        res = self.client.call('wamp.registration.list')
        return res

    def list_callees(self, _id):
        return self.client.call('wamp.registration.list_callees', _id)

    def lookup(self, _id):
        return self.client.call('wamp.registration.match', str(_id))

    def list_rpc(self):
        # strace()
        return [ self.get(_) for _ in self.list()["exact"] ]

    def list_uri(self):
        return [ _["uri"] for _ in self.list_rpc() ]

    def list_fuse(self):
        return [ _.split('.')[1] for _ in self.list_uri() if _.endswith("fuse")]

    def run(self):
        self.client.join()

    # def __getattr__(self, func):
    #     return partial(self.callback, func)
