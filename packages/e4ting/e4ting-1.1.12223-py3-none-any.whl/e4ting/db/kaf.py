#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    Kafka相关功能
    Add By :e4ting  2023-03-15 11:41:22
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

from e4ting import log
from e4ting import util
from confluent_kafka import Consumer


class Kafka:

    def __init__(self, ignore=True):
        self.ignore = ignore   # 是否忽略pull的报错

    def init(self, topics=[], config={}):
        log.info(topics)
        log.info(config)
        self.consumer = Consumer(config)
        self.consumer.subscribe(topics)

    @util.redef_return(ret=False)
    def pull(self):
        msg = self.consumer.poll(1.0)
        if msg is None: return None
        if msg.error():
            log.error("""Consumer error: { msg.error() }""".format(msg=msg))
            return None
        message = json.loads(str(msg.value(), "utf-8"))
        return message

    @util.redef_return(ret=None)
    def dispatch(self, data, hook):
        hook(data)

    def run(self, hook=print):
        while True:
            data = self.pull()
            if data != False or self.ignore == True:
                self.dispatch(data, hook)
                continue

            log.error("kafka pull 出现致命错误，退出运行")
            break

        log.info("关闭消费者")
        self.consumer.close()

    # def __del__(self):
    #     self.consumer.close()
