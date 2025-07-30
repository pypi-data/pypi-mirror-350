#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting  2023-05-11 15:57:13
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent
import consul
import json

class Worker:
    def __init__(self, consul_host, consul_port, task_prefix, sn = str(uuid.uuid4())):
        self.consul_client = consul.Consul(host=consul_host, port=consul_port, token="")
        self.task_prefix = task_prefix
        self.index = None

    def init(self):
        tasks = self.consul_client.kv.get(self.task_prefix, index=self.index)
        self.index = tasks[0]

    def run(self):
        self.init()
        while True:
            task_id, task_data = self.get_task()
            if task_id is not None and task_data is not None:
                task_func = task_data['func']
                task_args = task_data['args']
                task_result = task_func(*task_args)
                self.put_result(task_id, task_result)

    def get_task(self):
        # strace()
        tasks = self.consul_client.kv.get(self.task_prefix, index=self.index)
        self.index = tasks[0]
        for task in tasks:
            task_id = task['Key'].split('/')[-1]
            task_data = json.loads(task['Value'])
            if task_data['status'] == 'pending':
                task_data['status'] = 'running'
                task_key = f'{self.task_prefix}/{task_id}'
                self.consul_client.kv.put(task_key, json.dumps(task_data))
                return task_id, task_data
        return None, None

    def put_result(self, task_id, task_result):
        task_key = f'{self.task_prefix}/{task_id}'
        task_data = self.consul_client.kv.get(task_key)[1]
        task_data = json.loads(task_data['Value'])
        task_data['status'] = 'complete'
        task_data['result'] = task_result
        self.consul_client.kv.put(task_key, json.dumps(task_data))

