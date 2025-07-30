#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :cdj test@qq.com 2023-07-26 23:23:00
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

from jinja2 import Template

from consul import Consul

from e4ting.cache           import UUIDCache,FrpCache
from e4ting.cluster         import Cloud
from e4ting                 import log

class FRP():
    def __init__(self, uuid):
        self.uuid = uuid
        self.token = os.environ.get("FRP_TOKEN")

    def create(self):
        template = open("/code/etc/frpc_temp.yaml").read()
        return Template(template).render(etc=self, frp=FrpCache(self.uuid))

    def exists(self):
        api = Consul(host="consul.e4ting.cn", port=80, scheme="http", token=os.environ.get("CONSUL_TOEKN"), verify=False)
        index,data0 = api.kv.get("e4ting/nodes/{self.uuid}/etc/frpc.yaml".format(self=self))
        # log.info((index,data0))
        if not data0:
            return False
        return bool(data0["Value"])

    def push(self, force=False):
        # if not FrpCache(self.uuid).exists() and force == False:
        if not FrpCache(self.uuid).exists():
            log.error(f" {self.uuid} frp配置不存在".format(self=self))
            return True
        if self.exists() and force == False:
            return True
        log.info(f" {self.uuid} 开始推送配置".format(self=self))
        cloud = Cloud(remote="consul.e4ting.cn")
        @cloud.push(kv="{self.uuid}/etc/frpc.yaml".format(self=self))
        def frp_etc():
            return self.create()
        return frp_etc()

    @classmethod
    def force_push_all(cls):
        # from web.v2.cluster.frp import WebFRP
        for uuid in UUIDCache("*").keys():
            if not uuid.startswith("E4"): continue
            # log.info(f"强制推送 {uuid}")
            # FRP(uuid).push(force=True)
            # log.info(WebFRP().get_or_alloc(uuid))
            FRP(uuid).push()

if __name__ == '__main__':
    FRP.force_push_all()



