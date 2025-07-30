
#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting 2022-10-15 18:18:31
"""
import sys,os
import functools
import time,json
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack

from e4ting.db import MapDictRedis
from e4ting    import util

redis_temp_running = MapDictRedis()

class INRC():
    def __init__(self, key="api:ids", attr="attr"):
        self.key = key
        self.attr = attr

    def __get__(self, instance, owner):
        return redis_temp_running.add(self.key, self.attr)

class StringID(INRC):
    def __get__(self, instance, owner):
        return str(redis_temp_running.add(self.key, self.attr))

class RedisCache(object):
    # 运行状态信息
    attr = {"__uid__", "__key__", "__flush__", "__expire__"}
    # key  = INRC(attr="common")
    def __init__(self, mod="", uid=0):
        self.__uid__ = uid
        self.__key__ = f"cache:{mod}:{str(uid)}"
        self.__flush__ = False

    def refresh(self):
        self._time_ = time.time()
        self._date_ = now()

    def set(self, **kwargs):
        redis_temp_running[self.__key__] = dict(kwargs, __time__=util.now())
        self.__flush__ = True
        # self.refresh() # Add By cdj 2021-09-28 08:48:13 绝对不可以调
        return True

    def get(self, k=None):
        if not k:
            # 默认读取所有配置
            return redis_temp_running[self.__key__]

        return redis_temp_running.getkey(self.__key__, k)

    def pushd(self, data):
        if not data is str:
            data = json.dumps(data, ensure_ascii=False)
        redis_temp_running.rc.lpush(self.__key__, data)

    def popd(self, timeout=0.1):
        data = redis_temp_running.rc.brpop(self.__key__, timeout) or "{}"
        if data:
            data = data[1]
        return json.loads(data)

    def change(self, **kwargs):
        for k,v in kwargs.items():
            return self.incr(k, v)

    def incr(self, attr, number=1):
        self.__flush__ = True
        return redis_temp_running.add(self.__key__, attr, number)

    def delete(self, *attrs):
        return redis_temp_running.delitem(self.__key__, *attrs)

    def keys(self):
        # key = self.__key__.replace(self.__uid__, "*")
        keys = redis_temp_running.keys(self.__key__)
        pos = len(self.__key__) - 1
        return [ _[pos:] for _ in keys ]

    def exists(self):
        # 配置项是否存在
        return self.__key__ in redis_temp_running

    def __setattr__(self, k, v):
        # 极其危险
        # strace()
        if k in RedisCache.attr:
            super().__getattribute__("__dict__")[k] = v
            return

        return self.set(**{k:v})

    def __getattr__(self, k):
        return self.get(k)

    def __repr__(self):
        return f"{self.__uid__}"

    def timeout(self, howlong=31536000):
        # 默认超时一年
        if self.__flush__:
            redis_temp_running.expire(self.__key__, howlong)

    def __del__(self):
        self.timeout()

class UploadCache(RedisCache):
    # 用于统计系统总共上传过多个文件
    file_id = INRC(attr="upload_num")
    def __init__(self, md5):
        super().__init__("upload", md5)

    def __del__(self):
        # 有效期为3650天
        self.timeout(315360000)

class TokenCache(RedisCache):
    # 用于记录系统总共处理的请求数量, 每执行一次 TokenCache.login_id 将自动 +1
    login_id = INRC(attr="login_num")

    def __init__(self, token, timeout=604800):
        super().__init__("token", token)
        self.__expire__ = timeout

    def __del__(self):
        # 默认保留 1 day
        self.timeout(self.__expire__)

class DeviceCache(RedisCache):

    dev_id = INRC(attr="device_num")

    def __init__(self, uid):
        super().__init__("device", uid)

    def __del__(self):
        # 默认保留 30 day
        self.timeout(30*24*60*60)

class TaskCache(RedisCache):

    task_id = INRC(attr="task_num")

    def __init__(self, uid):
        super().__init__("task", uid)

    def __del__(self):
        # 默认保留 30 day
        self.timeout(30*24*60*60)

class OnlineCache(RedisCache):
    def __init__(self, uid):
        super().__init__("online", uid)

    def __del__(self):
        # 5min存活期
        self.timeout(300)

class UUIDCache(RedisCache):
    _id = INRC(attr="ws")

    def __init__(self, uuid, timeout=365*24*60*60):
        super().__init__("uuid", uuid)
        self.__expire__ = timeout

    @classmethod
    def cache(cls, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _uuid_ = kwargs.get("uuid") or args[-1]
            temp = UUIDCache(_uuid_)
            if temp.exists():
                return temp.key
            ret = func(*args, **kwargs)
            if not ret:
                return ret

            temp.set(key=ret, uuid=_uuid_, uptime=util.now(), call=func.__name__, desc=func.__doc__)

            temp0 = UUIDCache(ret)
            temp0.set(key=ret, uuid=_uuid_, uptime=util.now(), desc=func.__doc__)

            return ret
        return wrapper

    def __del__(self):
        # 默认保留 1 day
        self.timeout(self.__expire__)

class FrpCache(RedisCache):

    frp_port = INRC(attr="frp_port")

    def __init__(self, uuid):
        super().__init__("frp", uuid)

    def __del__(self):
        # 保留 180 day
        self.timeout(15552000)

class HistoryCache(RedisCache):
    gpt_seq = StringID(attr="chatgpt")
    def __init__(self, uuid):
        super().__init__("chatgpt", uuid)

    def __del__(self):
        # 保留5天
        self.timeout(432000)

class WXChatCache(RedisCache):
    def __init__(self, uuid):
        super().__init__("wxmsg", uuid)

    def __del__(self):
        # 保留50天
        self.timeout(4320000)

class IPCache(RedisCache):
    def __init__(self, ip):
        super().__init__("location", ip)

    @classmethod
    def cache(cls, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            uuid = kwargs.get("uuid") or args[-1]
            temp = cls(uuid)
            if temp.exists():
                return temp.key
            ret = func(*args, **kwargs)
            if not ret:
                return ret

            temp.set(key=ret, uuid=uuid, uptime=util.now(), call=func.__name__, desc=func.__doc__)

            temp0 = cls(ret)
            temp0.set(key=ret, uuid=uuid, uptime=util.now(), desc=func.__doc__)

            return ret
        return wrapper

    def __del__(self):
        # 保留5天
        self.timeout(432000)

class TemplateCache(RedisCache):
    key  = StringID(attr="template")
    def __init__(self, id):
        super().__init__("template", id)

    def __del__(self):
        # 保留1个月
        self.timeout(3600*24*365)
