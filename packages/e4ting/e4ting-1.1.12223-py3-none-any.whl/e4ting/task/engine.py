#!/bin/python3
# -*- coding:utf-8 -*-
"""
    事件驱动库
    By :陈狍子 e4ting@qq.com 2025-05-25 11:57:23
"""
import sys,os
from traceback  import format_exc as dumpstack

from multiprocessing.pool import ThreadPool
from multiprocessing      import cpu_count
from queue import Queue,Empty
import time

from e4ting import util,log

class Event():
    def __init__(self, payload, cb, timeout=5):
        self.payload  = payload
        self.callback = cb
        self.timeout  = timeout
        self.result   = Queue()

    def run(self):
        # 执行事件
        try:
            ret = self.callback(self.payload)
        except Exception as e:
            log.error(dumpstack())
            ret = None
        self.result.put(ret)

    def wait(self):
        # 等待事件结果
        ret = self.result.get(timeout=self.timeout)
        return ret

    def __repr__(self):
        return f"{self.callback}({self.payload})"

class Worker():
    """ 工人 """
    def __init__(self, tid, queue):
        self.tid   = tid
        self.queue = queue
        self.event = None
        self.total = 0  # 共处理了多少个任务

    def get_event(self):
        return self.queue.get()

    def exec_event(self, event):
        return self.event.run()

    def __call__(self, *args, **kwargs):
        while True:
            event = self.get_event()
            if not event:
                continue
            self.event = event
            self.total += 1
            self.exec_event(event)
            self.event = None

    def webdump(self):
        return dict(
                tid = self.tid,
                total = self.total,
                event = str(self.event),
            )

class Engine():
    def __init__(self, number=0):
        self.start_time = time.time()
        self.t_num = number or cpu_count() << 2
        self.total = 0
        self.queue = Queue()

    def init(self):
        self.pool = ThreadPool(processes=self.t_num)
        self.workers = [ Worker(i, self.queue) for i in range(self.t_num) ]

    def start(self):
        for task in self.workers:
            self.pool.apply_async(task, args=())

    def push(self, event):
        self.total += 1
        self.queue.put(event)

    def webdump(self):
        return dict(
                t_num = self.t_num,
                total = self.total,
                qsize = self.queue.qsize(),
                howlong = int(time.time() - self.start_time),
                tasks = [ w.webdump() for w in self.workers ]
            )
