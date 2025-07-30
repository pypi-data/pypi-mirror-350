#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting  2023-03-15 17:06:07
"""
import os,sys
import json

import collections
import functools
from functools  import partial
from cmd import Cmd
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
import base64
import threading
# from db.psql import pgsql as DB
import contextlib
import logging,logging.handlers
import datetime,time
import traceback
# import redis
import ctypes

try:
    from urllib.request   import urlopen
    from urllib.request   import Request
    from urllib.parse     import quote,urlencode,urlparse
except:
    from urllib2    import urlopen
    from urllib2    import Request
    from urllib     import quote,urlencode
    from urlparse   import urlparse
import binascii

import subprocess

from e4ting import log

class Single(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Single, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# 如果异常，重新定义返回值
def redef_return(ret=None):
    """
        捕获所有异常。
    """
    import functools
    def _config(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try :
                return function(*args, **kwargs)
            except Exception as e:
                log.info(dumpstack())
                return wrapper.ret
        # for k,v in options.items():
        #     setattr(wrapper, k, v)
        wrapper.ret = ret
        return wrapper
    return _config

def run_count():
    import functools
    def wraps(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            wrapper.count += 1
            log.info("{wrapper.promot} {wrapper.count}".format(wrapper=wrapper))
            return res
        wrapper.count  = 0
        wrapper.promot = func.__doc__.strip() if func.__doc__ else func.__name__
        return wrapper
    return wraps

def try_decode(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        code,ret = function(*args, **kwargs)
        try :
            return code,ret.decode()
        except:
            log.error(dumpstack())
            return code,ret
    return wrapper

@try_decode
def run_cmd(cmd):
    """执行命令行"""
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    if err or p.returncode != 0:
        log.error("{cmd},{p.returncode}, {err}".format(cmd=cmd, p=p, err=err))
    return p.returncode,out

def system(cmd):
    log.info(cmd)
    code,out = run_cmd(cmd)
    log.info(out)
    return out

def execute(cmd):
    log.info(cmd)
    code,out = run_cmd(cmd)
    return code

# class HTTP(object):
#     def __init__(self, **kwargs):
#         self.level = 'info'
#         [ setattr(self, k, v) for k,v in kwargs.items() ]

#     def suit(self, url):
#         ret = urlparse(url)
#         path = quote(ret.path)
#         return url.replace(ret.path, path)

#     def get(self, _url, data=None, _json=False, headers={}):
#         url = self.suit(_url)
#         _ = lambda x : quote(json.dumps(x) if not type(x) is str else x)
#         if data:
#             url = """{}?{}""".format(
#                 url,
#                 "&".join([ "=".join([k, _(v)]) for k,v in data.items()]) )
#         log.info(_url)
#         if headers:
#             ret = urlopen(Request(url, headers=headers))
#         else:
#             ret = urlopen(url)
#         return json.loads(ret.read().decode()) if _json else ret.read()

#     def put(self, _url, data=None, headers={"Content-Type": "application/json; charset=UTF-8"}):

#         url = self.suit(_url)
#         log.info("{url}, {data}".format(url=url, data=data))
#         import requests
#         req = requests.put(url, headers=headers, data=json.dumps(data), json={})
#         return req.json()

#     def post(self, _url, data=None, headers={"Content-Type": "application/json; charset=UTF-8"}):
#         url = self.suit(_url)

#         # import requests
#         # req = requests.post(url, headers=headers, data=json.dumps(data), json={})
#         # ret = json.loads(ret.decode())
#         # return req.text
#         # strace()
#         log.info("{url}, {data}".format(url=url, data=data))
#         if "json" in headers.get("Content-Type", ""):
#             ret = urlopen(Request(url, data = json.dumps(data).encode(), headers=headers), timeout=30).read()
#         elif "x-www-form-urlencoded" in headers.get("Content-Type", "x-www-form-urlencoded"):
#             # Content-Type:application/x-www-form-urlencoded
#             if type(data) is dict:
#                 # log.info(_url, urlencode(data))
#                 ret = urlopen(Request(url, data = urlencode(data).encode(), headers=headers), timeout=30).read()
#             else:
#                 ret = urlopen(Request(url, data = data.encode(), headers=headers), timeout=30).read()
#         else:
#             raise Exception("不支持的Content-Type： {} ".format(headers.get("Content-Type", "")))
#         ret = json.loads(ret.decode())
#         return ret

def printf(data=[], title=""):
    from prettytable import PrettyTable,MARKDOWN,MSWORD_FRIENDLY,ALL
    import shutil

    if not data:
        log.info("Nothing found")
        return

    width, _ = shutil.get_terminal_size()
    width = int(width * 0.5)

    x = PrettyTable()
    x.field_names = list(data[0].keys())
    [
        x.add_row(list( [ info.get(_, "") for _ in x.field_names ] ))
        for info in data
    ]
    x.align = 'l'
    # x.set_style(MSWORD_FRIENDLY)
    log.info("{title}\n{x}".format(title=title, x=x.get_string(max_width=width, vrules=ALL) ))
    return True

def progress(callback, iterable, desc="正在处理", key=lambda x:""):
    """ 处理进度条 """
    from tqdm import tqdm
    # ret = []
    pbar = tqdm(iterable, ncols=125)
    # 这个函数性能极差，将近150倍的样子 Add By cdj 2020-10-16 15:42:12
    pbar.set_description("{}".format(desc))
    ret = list(map(callback, pbar))
    return ret

def proxy_func(params):
    import sys
    path, args, kwargs = params
    for _ in path:
        sys.path.append(_)
    ret = sys.otherfunc(*args, **kwargs)
    return ret

def get_root(name, python):
    cmd = """docker inspect -f "/proc/{{.State.Pid}}/root" %(name)s""" % dict(name=name)
    root = system(cmd).strip()

    cmd = """chroot %(root)s %(python)s -c 'import sys,json;print(json.dumps(sys.path))'""" % dict(root=root, python=python)
    path = json.loads(system(cmd))

    return [ os.path.join(root, _.strip('/')) for _ in path]

def init_process(function):
    import sys
    # function, args, kwargs = params
    sys.otherfunc = function
    # sys.otherargs = [args, kwargs]

def run_at_docker(name='r-spc', python="/opt/rh/rh-python38/root/usr/bin/python3.8"):
    """ 以docker容器所在的环境运行函数 """
    import functools,multiprocessing,json
    def _config(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            from multiprocessing import Pool
            path = get_root(wrapper.docker, wrapper.python)
            # 用子进程隔离sys.path.append带来的影响
            with Pool(1, initializer=init_process, initargs=([function])) as pool:
                # with chroot(path):
                ret = pool.map(proxy_func, [(path, args, kwargs)])
                # p = multiprocessing.Process(target=function, executable=wrapper.python, args=args)
            # log.info(ret[0])
            return ret[0]
        wrapper.python = python
        wrapper.docker = name
        return wrapper
    return _config

def get_ip_local(ip):
    # url = "http://ip-api.com/json/?lang=zh-CN"
    url = "http://ip-api.com/json/{}?lang=zh-CN".format(ip)
    try:
        ret = HTTP().get(url, _json=True)
        if ret:
            return ret["country"], ret["regionName"], ret["city"]
    except:
        pass
    return None,None,None

class Timer():
    def __init__(self, *args, **kwargs):
        self.args   = args
        self.kwargs = kwargs

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *p):
        self.tick = time.time() - self.start
        log.info(f"{self} 用时 : {self.tick}s")
        return

    def __repr__(self):
        args,kwargs = "",""
        if self.args:
            args = ", ".join([str(_) for _ in self.args])
        if self.kwargs:
            data = [f"{k}={v}" for k,v in self.kwargs.items()]
            kwargs = ", ".join(data)
        return ",".join([args,kwargs])

class AttrUtil(object):
    def __init__(self, **kwargs):
        for attr,value in kwargs.items():
            super().__setattr__(attr, value)

    def __getattr__(self, attr):
        # raise NotImplementedError("不重载__getattr__不要继承这个类")
        return super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        raise NotImplementedError("不重载__setattr__不要继承这个类")

    # def __repr__(self):
    #     return

# def __getattr__(func):
#     from .common import util
#     return getattr(util, func)
