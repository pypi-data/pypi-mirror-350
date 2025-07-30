#!/bin/env python3
# -*- coding:utf-8 -*-

import time
import json
import sys,os
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack

import importlib
import importlib.util
import pkgutil

from e4ting import log,util

from flask_restful import Resource

@util.redef_return(ret=None)
def find_api_class(module):
    for item_name in dir(module):
        item = getattr(module, item_name)
        if hasattr(item, '__bases__') and Resource in item.__bases__:
            return item
    return None

def file_to_module(fname):
    log.info(fname)
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
        if not mod.endswith('.py'):
            continue
        module = file_to_module(mod)
        ClassAPI = find_api_class(module)
        if ClassAPI is None: continue
        url = os.path.join(head, directory, filename[:-3])
        urls = [url, url + '/<string:id>']
        log.info(urls)
        # strace()
        api.add_resource(ClassAPI, *urls)

def main():
    from werkzeug.middleware.proxy_fix import ProxyFix
    from flask_session  import Session
    from flask_cors     import CORS
    from flask          import Flask
    from flask_restful  import Api
    app = Flask(__name__, template_folder='/')
    api = Api(app)
    register_resources_from_dir(api, directory='v1' , head='/api')

    # CORS(app, supports_credentials=True)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
    app.config['SECRET_KEY'] = "e4ting"

    @app.errorhandler(Exception)
    def page_500(error):
        log.info(dumpstack())
        return """{"code":500}""", 500

    app.run(debug=True,
            host='0.0.0.0',
            port=80,
            use_reloader=True)

if __name__ == '__main__':
    main()
