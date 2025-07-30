#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    重载 rpc 建议服务
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent
from functools  import partial

from e4ting import log

from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


class RpcProxy(object):
    """docstring for RpcProxy"""
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def set(self, cls):
        assert not hasattr(cls, "run"), "{cls}不能包含run这个方法".format(cls=cls)
        cls.run = self.run
        self.cls = cls

    def run(self):
        log.info("定义RPC服务", self.cls, self.cls.__doc__, self.host, self.port)
        self.server = ThreadXMLRPCServer((self.host, self.port), allow_none=True)
        self.server.register_instance(self.cls())
        self.server.serve_forever()


def api(host="localhost", port=8080):
    proxy = RpcProxy(host, port)
    def onDecorator(aClass):
        # strace()
        proxy.set(aClass)
        return aClass
    return onDecorator

# @api(host="0.0.0.0", port=8080)
# class TEST():
#     '''测试服务'''
#     def test(self, name):
#         return name

# if __name__ == '__main__':
#     test = TEST()
#     test.run()
