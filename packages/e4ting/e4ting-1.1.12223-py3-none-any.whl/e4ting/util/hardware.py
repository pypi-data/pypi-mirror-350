#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :cdj test@qq.com 2023-07-09 15:00:36
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

from e4ting import util,log
# from e4ting

class Hardware():
    def __init__(self):
        pass

    def calc_real_use(self):
        """ CPU实时占用率 """
        import psutil
        return psutil.cpu_percent(interval=0.1)

    def cpu(self):
        import psutil
        core   = psutil.cpu_count()
        hz     = psutil.cpu_freq().current
        use    = psutil.cpu_percent()
        load1  = 0
        load5  = 0
        load15 = 0
        return dict(core=core, hz=hz, use=use, load1=load1, load5=load5, load15=load15)

# metaclass=util.Single
class Statistics():
    def __init__(self, _id="jusha", name=""):
        self._id      = _id
        self.name     = name
        self.cpu_core = 0
        self.memory   = 0
        self.maxbw    = 0
        self.bw       = 0
        self.dev_num  = 0
        self.online   = 0
        self.offline  = 0

    def calc_number(self):
        self.dev_num += 1

    def calc_online(self):
        self.online += 1

    def calc_offline(self):
        self.offline += 1

    def calc_status(self, status="1", **data):
        return status == "1"

    def calc_cpu(self, cpuCore=0, **data):
        self.cpu_core += cpuCore

    def calc_memory(self, memory=0, **data):
        self.memory += memory

    def calc_bw(self, tx=0, **data):
        self.bw += tx

    def calc_maxbw(self, maxBandwidth=0, **data):
        self.maxbw += maxBandwidth

    def add_js(self, data):
        self.calc_number()
        self.calc_maxbw(**data)

        if not self.calc_status(**data):
            self.calc_offline()
            return True

        self.calc_cpu(**data)
        self.calc_memory(**data)
        self.calc_online()
        self.calc_bw(**data)
        return True

    def show(self):
        log.info(self)

    def __repr__(self):
        return "{self.name} : dev={self.dev_num}(在线{self.online} / 离线{self.offline}), CPU={self.cpu_core}核, mem={self.memory} G, up={self.maxbw} Mbps, real={self.bw:.02f} Mbps".format(self=self)

    def json(self):
        return {
            "name"     : self.name,
            "cpu_core" : self.cpu_core,
            "memory"   : self.memory,
            "maxbw"    : self.maxbw,
            "bw"       : self.bw,
            "dev_num"  : self.dev_num,
            "online"   : self.online,
            "offline"  : self.offline,
        }

    def save(self):
        from common.mongo         import DB
        DB.statistics[self._id] = self.json()
        return True

    def load(self):
        from common.mongo         import DB
        data = DB.statistics[self._id]
        [ setattr(self, k, v) for k,v in data.items()]
        return data

    @classmethod
    def loads_all(cls):
        from common.mongo         import DB
        items = [ cls(_) for _ in DB.statistics.keys()]
        [ _.load() for _ in items]
        return items


