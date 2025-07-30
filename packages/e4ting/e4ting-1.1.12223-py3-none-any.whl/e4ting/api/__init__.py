#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :antiy chendejun@antiy.cn 2023-06-26 23:17:52
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

import importlib
import importlib.util
import pkgutil

from .cas  import CasDoor
from .spug import SPUG,SpugAPI
from .frp  import FRP
from e4ting import log

def find_api_class(module):

    from flask_restful import Resource

    for item_name in dir(module):
        item = getattr(module, item_name)
        if hasattr(item, '__bases__') and Resource in item.__bases__:
            return item
    return None

def file_to_module(fname):
    log.debug(fname)
    spec = importlib.util.spec_from_file_location('module', fname)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def register_resources_from_dir(api, directory, head='/api'):
    for filename in os.listdir(directory):
        mod = os.path.join(directory, filename)
        if os.path.isdir(mod):
            register_resources_from_dir(api, mod, head)
            continue
        if mod.endswith('.py'):
            module = file_to_module(mod)
            item = find_api_class(module)
            if item is None: continue
            url = os.path.join(head, directory, filename[:-3])
            urls = [url, url + '/<string:id>']
            log.info(urls)
            # strace()
            api.add_resource(item, *urls)
