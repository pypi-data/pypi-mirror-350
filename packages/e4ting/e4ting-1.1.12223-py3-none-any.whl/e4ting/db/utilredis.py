#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By  e4ting 2023-05-18 14:34:21
"""
import json
from redis  import Redis
# from e4ting import util

class RedisDB:
    def __init__(self, db=0, ip="redis", port=6379):
        self.ip = ip
        self.port = int(port)
        self.db = db
        self.r = Redis(host=self.ip, port=self.port, db=self.db, decode_responses=True)

    # @util.redef_return(ret=None)
    def set(self, key, msg):
        return self.r.set(key, msg)

    # @util.redef_return(ret=False)
    def delete(self, key):
        return self.r.delete(key)

    # @util.redef_return(ret=None)
    def get(self, key):
        return self.r.get(key)

    # @util.redef_return(ret=None)
    def hget(self,key, data):
        return self.r.hget(key, data)

    # @util.redef_return(ret=False)
    def sadd(self,key, data):
        return self.r.sadd(key, data)

    # @util.redef_return(ret=False)
    def sismember(self,key, data):
        return self.r.sismember(key, data)

    def keys(self, v="*", start=0, limit=0):
        return self.r.keys(v)

    def expire(self, key, ex=60):
        return self.r.expire(key, ex)

    def __contains__(self, key):
        return self.r.exists(key)

rds0 = RedisDB()

class INRC():
    def __init__(self, attr, key="api:ids"):
        self.key  = key
        self.attr = attr

    def __get__(self, instance, owner):
        # log(self.key, instance, owner)
        return rds0.sadd(self.key, self.attr)

class MapListRedis(RedisDB):

    def pop(self, key, timeout=1):
        ret = self.r.brpop(key, timeout)
        if ret:
            return ret[1]
        return ret

    def push(self, key, value, timeout=300):
        ret = self.r.lpush(key, json.dumps(value))
        self.r.expire(key, timeout)
        return True

class MapDictRedis(RedisDB):

    def add(self, key, field, v=1):
        return self.r.hincrby(key, field, v)

    def getkey(self, key, name):
        return self.r.hget(key, name)

    def format_v(self, v):
        if v == None:
            return ""
        if type(v) == bool:
            return int(v)
        if type(v) in [ dict, list]:
            return json.dumps(v, ensure_ascii=False)
        return v

    def delitem(self, key, *item):
        if not item:
            return True
        # if type(item) is list:
        #     return self.r.hdel(key, *item)
        # else:
        #     return self.r.hdel(key, item)
        return self.r.hdel(key, *item)

    def __getitem__(self, key):
        data = self.r.hgetall(key)
        return data

    def __setitem__(self, key, value):
        if not key:
            return None
        value = { k:self.format_v(v) for k,v in value.items()}
        self.r.hmset(key, value)