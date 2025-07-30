#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting  2023-03-31 10:24:14
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent
import logging
import contextlib
from casbin import Enforcer

import copy

from e4ting import util,log

# python3.6 有bug，deepcopy不可用
@contextlib.contextmanager
def python36m_copy():
    if sys.version_info.major == 3 and sys.version_info.minor == 6:
        python36m_copy.deepcopy = copy.deepcopy
        copy.deepcopy = copy.copy
    yield
    if sys.version_info.major == 3 and sys.version_info.minor == 6:
        copy.deepcopy = python36m_copy.deepcopy

class ACL(metaclass=util.Single):
    '''
        应当全局初始化
    '''
    def __init__(self, policy=None):
        self.policy = policy
        # with python36m_copy():
        self.init()
        log.info("ACL初始化完成")
    # def get_folder(self, folder):
    #     [  os.listdir(folder)]
    #     return

    def init(self):
        # self.load_
        model_text = os.path.join(os.path.dirname(__file__), "models", "admin.model")
        policy_text = self.policy or os.path.join(os.path.dirname(__file__), "models", "admin.policy")
        # strace()
        self.role_admin = Enforcer(model=model_text, adapter=policy_text, enable_log=True)
        self.role_admin.logger.setLevel(logging.CRITICAL)

    # @classmethod
    def check(self, role="test", api="/v1/api/", method="GET"):
        # 检查角色是否 对API有权限
        return self.role_admin.enforce(role, api, method)

    def free(self, api="/v1/api/", method="GET"):
        # 未登录用户对此API是否有权限
        return self.check('guest', api, method)

if __name__ == '__main__':
    acl = ACL()
    # 检查alice是否有读取data1的权限
    allowed = acl.check('admin', 'data1', 'POST')
    print(allowed)  # True

    # 检查bob是否有读取data1的权限
    allowed = acl.check('admin', '/v1/api/test', 'PUT')
    print(allowed)  # False

    # 没登录的用户检查权限
    allowed = acl.check('', '/user/sign', 'PUT')
    print(allowed)  # False

    # # 检查bob是否在group2中
    # in_group = acl.role_admin.enforce('bob', 'group2', 'member')
    # print(in_group)  # True

