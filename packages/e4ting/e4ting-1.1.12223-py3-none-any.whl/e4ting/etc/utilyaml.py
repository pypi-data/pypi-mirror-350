#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting  2023-03-31 14:19:09
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

import yaml

class yamlManage(object):
    def __init__(self, yaml_path, ):
        self.yaml_path = yaml_path
        with open(self.yaml_path, 'r', encoding='utf-8') as f:
            self.content = yaml.load(f, Loader=yaml.Loader)

    def get_section(self, section):
        return self.content.get(section, {})

    def get_value(self, section, key):
        return self.content.get(section, {}).get(key, None)

    def keys(self):
        return list(self.content.keys())

    def save(self):
        bak_file = "_".join([self.yaml_path, str(time.time())])
        yaml.dump(self.content, open(bak_file, 'w', encoding='utf-8'), encoding="utf-8",allow_unicode=True)
        os.rename(bak_file, self.yaml_path)

    def set_value(self, section, key, value):
        old_content = self.content
        with open(self.yaml_path, 'w', encoding='utf-8') as f:
            try:
                self.content[section][key] = value
                yaml.dump(self.content, f, Dumper = yaml.RoundTripDumper, encoding="utf-8",allow_unicode=True)
                return True
            except Exception as err:
                print(err)
                yaml.dump(old_content, f, Dumper = yaml.RoundTripDumper, encoding="utf-8",allow_unicode=True)
                return False

    def __repr__(self):
        return "yaml({self.yaml_path})".format(self=self)

class Section(object):
    def __init__(self, etc=None, yaml_path=None, section=""):
        # 为了执行这行代码而做的处理，为了适配 __setattr__ 重载
        # self.etc = etc or yamlManage(yaml_path)
        super().__setattr__("etc",     etc or yamlManage(yaml_path) )
        super().__setattr__("section", section )
        super().__setattr__("sec",     self.etc.get_section(section) )

    def keys(self):
        return list(self.sec.keys())

    def get(self, attr=None, default=None):
        """default: 如果获取的值为None，则返回default"""
        if not attr:
            return self.sec

        # 增加一个默认值
        ret = self.sec.get(attr)
        if ret == None:
            return default

        return ret

    def __getattr__(self, attr):
        return self.sec.get(attr)

    def __setattr__(self, attr, value):
        from e4ting import log
        log.info("{self.etc} [{self.section}] {attr} = {value}".format(self=self, attr=attr, value=value))
        self.sec.update({attr : value})
        self.etc.content.update({self.section : self.sec})
        self.etc.save()

    def __repr__(self):
        return "[{self.etc.yaml_path}]-[{self.section}]:{keys}".format(self=self,keys=self.keys())
