#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting e4ting@qq.com 2024-04-07 22:03:12
"""
import sys,os
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack

from .e4ting_pb2_grpc import E4tingStub
from .e4ting_pb2      import *
import grpc

from e4ting import util,log

class Recorder(metaclass=util.Single):
    def __init__(self):
        channel = grpc.insecure_channel('spc:8080')
        self.stub = E4tingStub(channel)

    def create_type(self, typename, detail, force=True):
        TYPE = self.stub.NewType(NewTypeReq(name=typename, detail=detail))
        if  TYPE.code == 200:
            return TYPE.data
        test = self.stub.GetType(ID(name=typename))
        if test.code == 200:
            return test.data
        return None

    def create_user(self, username, uuid, detail, TYPE, force=True):
        res = self.stub.NewAccount(NewAccountReq(name=username, detail=detail, typeID=TYPE.id, uuid=uuid))
        if  res.code == 200:
            return res.data
        test = self.stub.GetAccount(ID(name=username))
        if test.code == 200:
            return test.data
        return None

    def record(self, user, detail, weight=1):
        res = self.stub.AccountIn(BillingReq(money=weight, detail=detail, accountID=user.id))
        if  res.code == 200:
            return res.data
        log.error(res.err)
        return None

