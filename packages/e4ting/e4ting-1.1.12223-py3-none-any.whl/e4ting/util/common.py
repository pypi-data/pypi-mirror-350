#!/bin/env python3
# -*- coding:utf-8 -*-

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
# import logging,logging.handlers
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

from e4ting.log import info
log = info

def am_pm():
    return datetime.datetime.now().strftime('%p')

def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def now_str(s='_'):
    return datetime.datetime.now().strftime('%Y{flag}%m{flag}%d{flag}%H{flag}%M{flag}%S'.format(flag=s))

def now_hour(s='_'):
    return datetime.datetime.now().strftime('%Y{flag}%m{flag}%d{flag}%H'.format(flag=s))

def day_N(N = 1):
    return (datetime.datetime.now() - datetime.timedelta(days=N)).strftime('%Y-%m-%d')

def month_N(N = 1):
    import arrow
    return arrow.now().shift(months=-N).format("M")

def second_2_str(tick):
    # 秒数 转时分秒
    from datetime import timedelta
    return str(timedelta(seconds=int(time.time() - tick)))

def yestoday():
    return day_N(1)

def today():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def crc(*kargs):
    crc = binascii.crc32("".join(kargs).encode())
    return crc & 0xFFFFFFFF

def cwd():
    import os
    return os.getcwd()

def get_chart():
    import string
    import random
    return "".join(random. sample ( string.ascii_lowercase + string.ascii_uppercase + string.digits, 8))

def progress(callback, iterable, desc="正在处理", key=lambda x:""):
    """ 处理进度条 """
    from tqdm import tqdm
    # ret = []
    pbar = tqdm(iterable, ncols=125)
    # 这个函数性能极差，将近150倍的样子 Add By cdj 2020-10-16 15:42:12
    pbar.set_description("{}".format(desc))
    ret = list(map(callback, pbar))
    return ret

def b64decode(data):
    return base64.b64decode(data)

def b64encode(data):
    return base64.b64encode(data).decode()

def gzdecode(data):
    from io   import StringIO
    from gzip import GzipFile
    data = GzipFile(fileobj=StringIO(data)).read()
    return data

def md5(data):
    import hashlib
    if type(data) is bytes:
        return hashlib.md5(data).hexdigest()
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()

def md5sum(filename):
    with open(filename, "rb") as fp:
        data = fp.read()

    import hashlib
    return hashlib.md5(data).hexdigest()

def baseconvert(number, fromdigit=10, todigit=62):
    # if str(number)[0] == '-':
    #     number = str(number)[1:]
    #     neg = 1
    # else:
    #     neg = 0
    # make an integer out of the number
    import string
    smap = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" + string.punctuation
    assert fromdigit <= len(smap)
    assert todigit   <= len(smap)

    fromdigits = smap[:fromdigit]
    todigits   = smap[:todigit]

    x = 0
    from_len = len(fromdigits)
    for digit in str(number):
        x = x * from_len + fromdigits.index(digit)
    # create the result in base 'len(todigits)'
    res = ""
    to_lenght = len(todigits)
    while x > 0:
        digit = x % to_lenght
        res = todigits[digit] + res
        x //= to_lenght
    # if neg:
    #     res = "-"+res
    return res

def compare_time(timestamp, second = 60):
    # 判断当前时间是否处在  [timestamp, timestamp + second ] 区间内
    return timestamp - second <= time.time() <= timestamp + second

day_seconds = 24 * 60 * 60

html_path = "/.sysroot/home/nginx/html/APP"

class FuncStatus(object):
    """ 函数状态 """
    def __init__(self, function=None):
        self.file      = function. __globals__["__file__"]          #   os.path.abspath(function. __globals__["__file__"])
        self.mod       = function.__module__
        self.func_name = "{}.{}".format(self.mod, str(function).split()[1])
        self.call_num  = 0
        self.doc       = function.__doc__.strip()
        self.record( time.time())
        # self.name      = function.__name__

    def __add__(self, data):
        ''' 调用次数加 1 '''
        self.call_num += 1
        return self

    def __iadd__(self, data):
        ''' 调用次数加 1 '''
        return self + 1

    def dumps(self):
        return {
            "file" : self.file,
            "doc"  : self.doc,
            "mod" : self.mod,
            "name" : self.func_name,
            "call_num" : self.call_num,
            "use_time" : self.use_time * 1000,
        }

    # @property
    # def use_time(self):
    #     if "_use_time" not in self.__dict__:
    #         return 0
    #     return self._use_time * 1000

    # @use_time.setter
    def record(self, last_tick):
        ''' 记录函数用时 '''
        self.use_time = time.time()  - last_tick
        log("{obj}  用时 {time:.4f} s ".format(obj=self, time=self.use_time))

    def __repr__(self):
        return "[{file}] - {mod} {func}()".format(file=self.file, mod=self.mod, func=self.func_name)

def init_title():
    import setproctitle
    globals()["__title__"] = setproctitle.getproctitle()
    return globals()["__title__"]

def set_title(title):
    import setproctitle
    # if "__title__" not in globals() or not globals()["__title__"]
    if not globals().get("__title__", None):
        init_title()
    setproctitle.setproctitle("{} {}".format(globals()["__title__"], title))

def timered(*arg, **options):
    """
        定时执行函数
    """
    import functools
    from random    import randint

    def _config(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            # log(function, wrapper.tick, wrapper.interval, compare_time(wrapper.tick, wrapper.interval))
            if compare_time(wrapper.tick, wrapper.interval):
                return None
            # log(function)
            # 记录运行时间点
            wrapper.tick = time.time()
            return function(*args, **kwargs)
        for k,v in options.items():
            setattr(wrapper, k, v)
        # log(function, "set tick")
        setattr(wrapper, "tick", time.time() - randint(0, 60))
        return wrapper
    return _config

def time_count(function):
    """
        修饰器，用来统计函数调用耗时
    """
    f = FuncStatus(function = function)
    print("{} 将被计时".format(f))
    if "func_status" not in globals():
        globals()["func_status"] = {}
    globals()["func_status"][f.func_name] = f
    def wrapper(*args, **kwargs):
        tick = time.time()
        ret = function(*args, **kwargs)
        f.call_num += 1
        f.record( tick)
        return ret
    return wrapper

def save_request(doc):
    from flask import request,session
    import datetime

    from mongo import db_requests

    record = {}

    record["doc"] = doc
    record["user"] = session.get("UUID")
    record["uri"] = request.path
    record["ip"]  = request.headers["X-Real-Ip"]
    record["act"] = request.method
    record["data"] = request.json

    record["second"] = now()

    db_requests[time.time()] = record

def record_action(function):
    import werkzeug
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            # log("记录网络请求")
            save_request(function.__doc__.strip())
        except werkzeug.exceptions.BadRequest:
            pass
        except:
            log(dumpstack())
        return function(*args, **kwargs)
    return wrapper

def allow(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        from permission import check_req_permission
        from flask         import redirect,request
        if check_req_permission():
            return function(*args, **kwargs)
        return { "code" : 302,
                 "data" : "权限不允许",
                 "location" : "/apply?api={}".format(request.path)
            }
    return wrapper

def random_weight(weight_data, key=lambda x: x):

    from random    import randint
    from itertools import accumulate
    from bisect    import bisect_right

    # 累积和
    weights = list(accumulate([ key(_) for _ in weight_data]))
    log(weights)
    # 二分法找随机值位置
    index   = bisect_right(weights, randint(0, weights[-1] - 1))
    return weight_data[index]

def argv_parse():
    import argparse
    import datetime
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="蜂群系统"
    )
    parser.add_argument(
        '-m', '--mac',
        action='store',
        type=str,
        default='',
        help='MAC 前缀 如： F041/ACDB/3C24F0A00137'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        # dest='bool_arg',
        # type=bool,
        default=False,
        help='调试模式'
    )
    parser.add_argument(
        '--db',
        action='store',
        type=str,
        default='JP',
        help='默认： JP'
    )
    parser.add_argument(
        '--day',
        action='store',
        type=int,
        default=0,
        help='默认： 0'
    )
    parser.add_argument(
        '-f', '--frame',
        action='store',
        type=int,
        default=50,
        help='帧数： 0'
    )
    parser.add_argument(
        '--file',
        action='store',
        type=str,
        default='test.xlsx',
        help='默认： test.xlsx'
    )
    parser.add_argument(
        '--table',
        action='store',
        type=str,
        default='YF_USER',
        help='默认： YF_USER'
    )
    parser.add_argument(
        '-i', '--input',
        action='store',
        type=str,
        default='.doc',
        help='默认： .doc'
    )
    parser.add_argument(
        '--tag',
        action='store',
        type=str,
        default='',
        help='追加值'
    )
    parser.add_argument(
        '--url',
        action='store',
        type=str,
        default='http://www.bing.com',
        help='默认： http://www.bing.com'
    )
    parser.add_argument(
        '--version',
        action='store',
        type=str,
        default='v2',
        help='指定API版本，默认： v2'
    )
    parser.add_argument(
        '-o', '--output',
        action='store',
        type=str,
        default='test.xlsx',
        help='test.pdf / test.xlsx 默认： test.xlsx'
    )
    parser.add_argument(
        '--thread',
        action='store',
        type=int,
        default=1,
        help='并发CPU倍数，默认为： 1'
    )
    from multiprocessing         import cpu_count
    parser.add_argument(
        '--cpu',
        action='store',
        type=int,
        default=cpu_count(),
        help='CPU数，默认为： cpu_count()'
    )

    return parser.parse_args()

class DES(object):
    def __init__(self, **kwargs):
        self.KEY = 'ZmUxMzk2NTJiNjU4NzlkMzBhY2QzYjNjZGQ2YjVhNmEK'
        [ setattr(self, k, v) for k,v in kwargs.items() ]

    def encode(self, s):
        """
        DES 加密
        :param s: 原始字符串
        :return: 加密后字符串，16进制
        """
        from pyDes import des, CBC, PAD_PKCS5
        import binascii
        secret_key = self.KEY[:8]
        iv = secret_key
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        en = k.encrypt(s, padmode=PAD_PKCS5)
        return binascii.b2a_hex(en).decode()

    def decode(self, s):
        """
        DES 解密
        :param s: 加密后的字符串，16进制
        :return:  解密后的字符串
        """
        from pyDes import des, CBC, PAD_PKCS5
        import binascii
        secret_key = self.KEY[:8]
        iv = secret_key
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
        return de.decode()

class MapInfoTemp(object):
    """docstring for MapInfoTemp"""
    def __init__(self, *kargs, **kwargs):
        # self.devs = {}
        self.file = 'test.json'
        self.data = {}
        self.flag = True
        self.lock = alloc_lock()
        [ setattr(self, k, v) for k,v in kwargs.items() ]
        self.load()

    def __getitem__(self, key):
        if not key in self.data:
            # raise StopIteration
            return None
        return self.data[key]

    def __setitem__(self, key, value):
        if not key:
            return None

        log("修改 {} {}".format(key, value), level="debug")
        if key in self.data and type(self.data[key]) is dict:
            self.data[key].update(value)
        else:
            self.data[key] = value
        self.dump()

    def __delitem__(self, key):
        if not key:
            return None
        log("删除 {}".format(key))
        del self.data[key]
        self.dump()

    def __enter__(self):
        self.lock.acquire()
        self.flag = False

    def __exit__(self, type, value, trace):
        self.flag = True
        try:
            self.dump()
        except Exception as e:
            log(str(e), level='error')
        self.lock.release()

    def load(self):
        if os.path.exists(self.file):
            log("加载 {}".format(self.file))
            self.data = json.load(open(self.file))

    def dump(self):
        if not self.flag:
            return True
        log("保存 {}".format(self.file))
        open(self.file, "+w").write(json.dumps(self.data, indent=4))

def filters(_args, *kargs, **kwargs):

    args = { k:v for k,v in _args.items() if v }
    default_args = { 'page' : 1, 'limit' : 20}
    default_args.update(args)
    args = default_args
    args['offset'] = (int(args.get("page", 1)) - 1) * int(args['limit'])
    del args['page']
    return args

# 如果异常，重新定义返回值
def redef_return(*arg, **options):
    """
        捕获所有异常。
    """
    import functools
    def _config(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try :
                return function(*args, **kwargs)
            except:
                log(dumpstack())
                return wrapper.ret
        for k,v in options.items():
            setattr(wrapper, k, v)
        return wrapper
    return _config

def fatal(*args):
    msg = " ".join([str(_) for _ in args])
    logger.critical(msg)

def alloc_lock():
    return threading.Lock()

@contextlib.contextmanager
def lock_run(lock):
    # 加锁运行
    lock.acquire()
    yield
    lock.release()

@contextlib.contextmanager
def pwd_doing():
    # 保证当前目录运行 Add By cdj 2020-12-07 18:17:39
    pwd = os.getcwd()
    yield
    os.chdir(pwd)

@contextlib.contextmanager
def chroot(path="/.sysroot"):
    import os
    pwd = os.getcwd()
    # with pwd_doing():
    real_root = os.open("/", os.O_RDONLY)
    if os.path.exists(path):
        os.chroot(path)

    yield

    os.fchdir(real_root)
    os.chroot(".")
    os.close(real_root)
    os.chdir(pwd)
    log(os.getcwd())

def session_check(*arg, **options):
    """

    """
    import functools
    from flask import session,request
    def _config(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            log(session.get('BINDID'))
            log(request.headers["X-Real-Ip"])
            return function(*args, **kwargs)
            # try :
            #     return function(*args, **kwargs)
            # except:
            #     return wrapper.ret
        for k,v in options.items():
            setattr(wrapper, k, v)
        return wrapper
    return _config

def login_required(function):
    import functools
    from flask import redirect,request,make_response,session
    import login.login

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        ret = login.login.session_is_login()
        if ret == True:
            return function(*args, **kwargs)
        else:
            return ret
    return wrapper

def valid_check(value):
    import re
    if not value :
        return False
    ret = re.match("([A-Fa-f0-9]{2}:){5}[A-Fa-f0-9]{2}", value)
    return bool(ret)

def parse_win_cmd(data):
    return [ _.strip() for _ in data.strip().split('\r\n') if _.strip()]

def parse_linux_cmd(data):
    return [ _.strip() for _ in data.strip().split('\n') if _.strip()]

def processed(function):
    import multiprocessing
    @functools.wraps(function)
    def _processed(*args, **kwargs):
        thread_or_process = multiprocessing.Process(target=function, args=args, kwargs=kwargs)
        thread_or_process.daemon = True
        thread_or_process.start()
        return thread_or_process
    return _processed

def pclose(thread_or_process, kill=False):
    # kill代表是否强行杀掉
    if kill and thread_or_process.is_alive():
        thread_or_process.terminate()
    thread_or_process.join()

def threaded(function):
    @functools.wraps(function)
    def _threaded(*args, **kwargs):
        # kwargs["event"] = threading.Event()
        thread_or_process = threading.Thread(target=function, args=args, kwargs=kwargs)
        thread_or_process.setName(function.__name__ + str(time.time()))
        # thread_or_process.event = kwargs["event"]
        thread_or_process.daemon = True
        thread_or_process.start()
        return thread_or_process
    return _threaded

def tclose(thread_or_process, kill=False):
    if kill and thread_or_process.is_alive():
        # util.log()
        # strace()
        # threading.Thread._stop(thread_or_process)
        ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_or_process.ident, ctypes.py_object(SystemExit))
    thread_or_process.join(0.1)

def aton(ip):

    # import socket
    # # 仅 python3 能用
    # return int.from_bytes(socket.inet_aton(ip), "big")

    import socket,struct
    if is_ip(ip):
        return socket.ntohl(struct.unpack("I",socket.inet_aton(ip))[0])

    if sys.version_info.major == 2:
        # 仅 python2 能用
        return int( ip.encode('hex'), 16)
    else:
        # 仅 python3 能用
        return int.from_bytes( ip.encode() , "big")

def post(url="", data={}):

    # log(url, json.dumps(data))
    ret = urlopen(Request(url, data = json.dumps(data).encode(), headers={"Content-Type":"application/json"})).read()
    ret = json.loads(ret.decode())
    return ret

class HTTP(object):
    def __init__(self, **kwargs):
        self.level = 'info'
        [ setattr(self, k, v) for k,v in kwargs.items() ]

    def suit(self, url):
        ret = urlparse(url)
        path = quote(ret.path)
        return url.replace(ret.path, path)

    def get(self, _url, data=None, _json=False, headers={"Content-Type": "application/json; charset=UTF-8"}):
        url = self.suit(_url)
        _ = lambda x : quote(json.dumps(x) if not type(x) is str else x)
        if data:
            url = """{}?{}""".format(
                url,
                "&".join([ "=".join([k, _(v)]) for k,v in data.items()]) )
        log(_url)
        ret = urlopen(Request(url, headers=headers))
        data = ret.read()
        # log(data)
        return json.loads(data.decode()) if _json else ret.read()

    def put(self, _url, data=None, headers={"Content-Type": "application/json; charset=UTF-8"}):

        url = self.suit(_url)
        log((_url, data))
        import requests
        req = requests.put(url, headers=headers, data=json.dumps(data), json={})
        return req.json()

    def post(self, _url, data=None, headers={"Content-Type": "application/json; charset=UTF-8"}):
        url = self.suit(_url)

        # import requests
        # req = requests.post(url, headers=headers, data=json.dumps(data), json={})
        # ret = json.loads(ret.decode())
        # return req.text
        # strace()
        log((_url, data))
        if "json" in headers.get("Content-Type", ""):
            ret = urlopen(Request(url, data = json.dumps(data).encode(), headers=headers), timeout=30).read()
        elif "x-www-form-urlencoded" in headers.get("Content-Type", ""):
            # Content-Type:application/x-www-form-urlencoded
            if type(data) is dict:
                # log(_url, urlencode(data))
                ret = urlopen(Request(url, data = urlencode(data).encode(), headers=headers), timeout=30).read()
            else:
                ret = urlopen(Request(url, data = data.encode(), headers=headers), timeout=30).read()
        else:
            raise Exception("不支持的Content-Type： {} ".format(headers.get("Content-Type", "")))
        ret = json.loads(ret.decode())
        return ret

def is_ip(inputs):
    """ 是否为合法IP地址 """
    import socket
    if not inputs:
        return False
    try:
        socket.inet_aton(inputs)
        return True
    except OSError:
        return False

def notify_by_api(title="", text="", mod="火眼"):
    return HTTP().post("http://notify.e4ting.cn/api/v1/socket/notify/{}".format(quote(mod)),
        data = {
            "title": title,
            "text" : text,
        })

# def get_ip_local(ip):
#     # url = "http://ip-api.com/json/?lang=zh-CN"
#     url = "http://ip-api.com/json/{}?lang=zh-CN".format(ip)
#     try:
#         ret = HTTP().get(url, _json=True)
#         if ret["status"] == "success":
#             del ret["status"]
#             del ret["query"]
#             return ret
#     except:
#         pass
#     return None

# def ip_local(ip):
#     from mongo import db_IPs
#     if ip in db_IPs:
#         return db_IPs[ip]
#     ret = get_ip_local(ip)
#     if ret:
#         db_IPs[ip] = ret
#         return ret
#     return None
def get_app_dir(app="test"):
    path = os.path.join(os.getenv("APPDATA") or os.path.abspath("."), app)
    mkdir(path)
    return path

def mkdir(path):
    if os.path.exists(path) == False:
        try:
            os.makedirs(path)
        except:
            return False

class CLI(Cmd):
    """
    help
        这是doc
    """
    def __init__(self, env=None):
        Cmd.__init__(self)
        self.prompt = " -> "
        self.intro = "已进入控制台，敲回车 [enter] 激活"
        self.env = env

    def do_exit(self, arg):
        return True  # 返回True，直接输入exit命令将会退出

    def do_strace(self, arg):
        strace()

    def default(self, line):
        # self.last_code,ret = self.dev.shell(line)
        eval(line)
        # print(ret, end='')

    def do_EOF(self, line):
        print('')
        return True

    def emptyline(self):  # 当输入空行的时候
        pass

# @threaded
def init_cli(env):
    CLI(env).cmdloop()
