#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting  2023-03-14 16:31:24
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

from e4ting import log
import xmlrpc.client


def client(server="http://localhost:8080"):
    # Create an XML-RPC client
    proxy = xmlrpc.client.ServerProxy(server)
    return proxy


if __name__ == '__main__':
    TEST = client("http://localhost:8080")
    # Call the remote method
    ret = TEST.test('Alice')
    log.info(ret)