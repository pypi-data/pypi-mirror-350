#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :antiy chendejun@antiy.cn 2023-06-26 22:31:33
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent
import requests

from e4ting       import log,util
from e4ting.cache import TokenCache

# from casdoor import CasdoorSDK

class CasDoor():
    def __init__(self, casdoor_host="", client_id="", client_secret="", grant_type="authorization_code"):
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.casdoor_host = casdoor_host
        # self.client_ip = client_ip

    @property
    def login_url(self):
        return "{self.casdoor_host}/login/oauth/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.refer}&scope=read&state=casdoor".format(self=self)

    def goto_login(self):
        payload = dict(code=302, url=self.login_url)
        return payload

    def code_swap_token(self, code):
        # 用code交换token
        return TokenCache(code).access_token

    @util.redef_return(ret=False)
    def check_code(self, code, refer="", client_ip=""):
        if not code:
            return False

        if TokenCache(code).exists():
            return True

        payload = dict(
            grant_type=self.grant_type,
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code,
            redirect_uri=refer,
        )
        url = "{self.casdoor_host}/api/login/oauth/access_token".format(self=self)
        TokenCache.login_id
        # ret = util.HTTP().post(url, payload, headers={"Content-Type": "x-www-form-urlencoded"})
        res = requests.post(url, payload)
        ret = res.json()
        # log.info(ret)
        if not "access_token" in ret:
            return False
        token = ret["access_token"]
        TokenCache(token).set(client_ip=client_ip, uptime=util.now(), **ret, **payload)
        TokenCache(code).set(client_ip=client_ip, uptime=util.now(), **ret, **payload)
        # from e4ting.task import Async
        # Async().get_user_detail(self.token, code)
        return True

    @util.redef_return(ret=False)
    def check_token(self, token):
        if not token:
            return False
        # log.debug(token)

        userinfo = self.get_userinfo(token)
        return bool(userinfo)

    # @util.redef_return(ret={})
    # def userinfo(self):
    #     info = self.sdk.parse_jwt_token(self.token)
    #     log.info(info)
    #     return {
    #         "uid" : info["name"],
    #         "username" : info["displayName"],
    #         "phone" : info["phone"],
    #         "email" : info["email"],
    #         "avatar" : info["avatar"],
    #         "type" : info["type"],
    #     }

    def get_userinfo(self, token):
        url = "{self.casdoor_host}/api/userinfo".format(self=self)
        ret = util.HTTP().get(url, _json=True, headers={"Authorization": "Bearer {token}".format(token=token)})
        log.debug(ret)
        if not ret:
            return False
        if ret.get("status", '') == 'error':
            return False
        return ret

    def get_user(self, token):
        # 这个接口并没有想象中的那么卡
        url = "{self.casdoor_host}/api/get-account".format(self=self)
        ret = util.HTTP().get(url, _json=True, headers={"Authorization": "Bearer {token}".format(token=token)})
        # log.info(ret)
        if not ret:
            return False
        return ret

if __name__ == "__main__":
    sdk = CasdoorSDK(
        endpoint='https://mycas.e4ting.cn',
        client_id='XXX',
        client_secret='XXXXXX',
        certificate=certificate,
        org_name='paozi',
        application_name='XXX',
    )
    # code = "addad03e6e30132f4df4"
    # token = TokenCache(code)
    payload = sdk.parse_jwt_token(token.access_token)
    util.log(payload)
    # strace()
    # sdk.get_oauth_token(code)
