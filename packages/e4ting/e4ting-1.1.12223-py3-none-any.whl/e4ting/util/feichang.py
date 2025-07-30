#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    肥肠专用库
    Add By :e4ting 2023-06-12 10:36:09
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

class DataEther():
    def __init__(self, payload=[]):
        self.data = {_.get("inteface", ""):[] for _ in payload}
        self.init(payload)

    def merge(self, infos=[]):
        if not infos:
            return {}
        key   = infos[0].keys()
        value = zip(*[_.values() for _ in infos])
        value = [ list(_) for _ in value]
        return dict(zip(key, value))

    def init(self, payload=[]):
        for item in payload:
            self.data[ item.get("inteface", "") ].append(item)
        self.data = { eth:self.merge(data) for eth,data in self.data.items()}

    def dumps(self):
        return self.data

def merge_eths(payload):
    data = DataEther(payload)
    return data.dumps()

if __name__ == '__main__':
    a = [{'dst_ip': '114.114.114.114', 'src_ip': '218.28.203.103', 'loss': '0', 'rtt_min': '13.616', 'rtt_avg': '13.797', 'rtt_max': '14.240', 'rtt_mdev': '0.185', 'seq': 34, 'time_stamp': '23-06-09 18:39:16', 'inteface': 'eth3'},{'dst_ip': '114.114.114.114', 'src_ip': '218.28.203.103', 'loss': '0', 'rtt_min': '13.616', 'rtt_avg': '13.797', 'rtt_max': '14.240', 'rtt_mdev': '0.185', 'seq': 34, 'time_stamp': '23-06-09 18:39:16', 'inteface': 'eth2'},{'dst_ip': '114.114.114.114', 'src_ip': '218.28.203.103', 'loss': '0', 'rtt_min': '13.616', 'rtt_avg': '13.797', 'rtt_max': '14.240', 'rtt_mdev': '0.185', 'seq': 34, 'time_stamp': '23-06-09 18:39:16', 'inteface': 'eth3'},{'dst_ip': '114.114.114.114', 'src_ip': '218.28.203.103', 'loss': '0', 'rtt_min': '13.616', 'rtt_avg': '13.797', 'rtt_max': '14.240', 'rtt_mdev': '0.185', 'seq': 34, 'time_stamp': '23-06-09 18:39:16', 'inteface': 'eth2'}]
    from e4ting.util import util
    util.printf(a)
    data = merge_eths(a)
    print(json.dumps(data))
