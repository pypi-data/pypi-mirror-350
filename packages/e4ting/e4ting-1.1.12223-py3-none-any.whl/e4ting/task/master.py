#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting  2023-05-11 16:11:48
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

import consul
import uuid
import json

from e4ting import log

class Scheduler:
    def __init__(self, consul_host, consul_port, task_prefix):
        self.consul_client = consul.Consul(host=consul_host, port=consul_port, token="")
        self.task_prefix = task_prefix

    def submit_task(self, task_func, task_args, task_id = str(uuid.uuid4())):
        task_data = {
            'func': task_func.__name__,
            'args': task_args,
            'status': 'pending'
        }
        task_key = f'{self.task_prefix}/{task_id}'
        self.consul_client.kv.put(task_key, json.dumps(task_data))
        return task_id

    def get_task_result(self, task_id):
        task_key = f'{self.task_prefix}/{task_id}'
        index = None

        while True:
            _, task_data = self.consul_client.kv.get(task_key, index=index)
            log.info(_, task_data)
            if task_data is not None:
                task_data = json.loads(task_data['Value'])
                if task_data['status'] == 'complete':
                    return task_data['result']
                index = task_data['ModifyIndex']
            else:
                index = None


