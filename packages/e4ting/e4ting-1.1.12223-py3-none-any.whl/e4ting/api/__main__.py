#!/bin/python3
# -*- coding:utf-8 -*-
"""
    Rest API Tool
    Add By :陈狍子 e4ting@qq.com 2024-07-19 14:40:52
"""
import sys,os
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from e4ting import util,log

from textwrap import dedent
from jinja2 import Template
import ast

class APITemplate():
    def __init__(self, script, class_name, enable):
        self.script      = script
        self.class_name  = class_name
        self.enable      = enable
        self.imports     = script[:-3].replace("/", ".")
        self.restapi     = [ script[:-3] , script[:-3] + '/<string:id>' ]

    def __repr__(self):
        return dedent("""
        from {self.imports} import {self.class_name}
        """).format(self=self).strip()

def make_service(template="service_api.tmpl", apis=[]):
    template = open(template).read()
    return Template(template).render(apis=apis)

def walk(directory):
    files = []
    for filename in os.listdir(directory):
        mod = os.path.join(directory, filename)
        if os.path.isdir(mod):
            files += walk(mod)
        if mod.endswith('.py'):
            files.append(mod)
    return files

def parse_api(script):
    tree = ast.parse(open(script).read())
    enable = True
    class_name = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                # 变量
                if not isinstance(target, ast.Name): continue
                # 全局变量
                if node.col_offset != 0: continue
                # enbale变量
                if target.id != 'enable': continue
                enable = node.value.value
                # print("变量定义", node, (target.id, enable))
        elif isinstance(node, ast.ClassDef):
            base_classes = [base.id for base in node.bases]
            if "Resource" not in base_classes: continue
            class_name = node.name
            # print("类定义", node, (class_name, base_classes))
    log.info(f"{script}.enable = {enable} -> {class_name}")
    # if not enable:
    #     return ""
    return APITemplate(script, class_name, enable)

def argv_parse():
    import argparse
    parser = argparse.ArgumentParser(
        prog="python3 -m e4ting.api",
        description="Rest API Tool"
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='调试模式'
    )
    parser.add_argument(
        '-t', '--template',
        action='store',
        type=str,
        default="service_api.tmpl",
        help='默认： service_api.tmpl'
    )
    parser.add_argument(
        '-d', '--dir',
        action='store',
        type=str,
        default='',
        help='默认： v2'
    )
    return parser.parse_args()

def main():
    op = argv_parse()

    pys = walk(op.dir)
    # log.info( '\n'.join(pys) )

    apis = [parse_api(f) for f in pys]
    for api in apis:
        log.info(api)
    output = f"service_api_{op.dir.strip('/')}.py"
    code = make_service(op.template, apis)
    open(output, "w+").write(code)
    log.info(f"微服务代码输出到 {output}")

if __name__ == '__main__':
    main()
