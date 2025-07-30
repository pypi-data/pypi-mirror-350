#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    网卡相关操作
    Add By :e4ting  2023-03-15 11:41:22
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

from e4ting import log
from e4ting import util

def cat(fname):
    return open(fname).read().strip()

class IFace():
    """网卡列表原生操作，不依赖第三方库"""
    def __init__(self, name):
        self.name = name
        self.is_phy = self.is_physic()

    @util.redef_return(ret="down")
    def status(self):
        return cat("/sys/class/net/{self.name}/operstate".format(self=self))

    @util.redef_return(ret=0)
    def speed(self):
        return int(cat("/sys/class/net/{self.name}/speed".format(self=self)))

    def mac(self):
        return cat("/sys/class/net/{self.name}/address".format(self=self))

    def is_physic(self):
        return 'pci' in os.path.realpath("/sys/class/net/{self.name}".format(self=self))

    def mark(self):
        ret = 0
        data = [ord(c)*((i+1)*10) for i,c in enumerate(self.name)]
        return sum(data)

    def __repr__(self):
        return 'IFace([{self.is_phy}] {self.name})'.format(self=self)

    @classmethod
    def load_all(cls):
        ifs = os.listdir("/sys/class/net/")
        return [ IFace(name) for name in ifs ]





