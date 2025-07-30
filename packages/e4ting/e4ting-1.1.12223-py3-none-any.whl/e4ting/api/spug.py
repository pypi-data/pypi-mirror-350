#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting e4ting@gmail.com 2022-10-10 16:22:59
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack

from e4ting import util,log

class SpugAPI():
    def __init__(self, host="", user="", passwd="", token=None):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.token = token
        # self.login()

    def login(self, ip=""):
        url = f"""{self.host}/api/account/login/"""
        payload = {"username":self.user,"password":self.passwd,"type":"default"}
        if ip:
            ret = util.HTTP().post(url, payload, headers={"Content-Type": "application/json; charset=UTF-8", "X-Real-Ip" : ip})
        else:
            ret = util.HTTP().post(url, payload)
        assert not ret["error"],ret["error"]
        self.token = ret["data"]["access_token"]
        return ret

    # @util.redef_http(code=403)
    def http_get(self, url):
        ret = util.HTTP().get(url, headers={"X-Token":self.token})
        return json.loads(ret)

    # @util.redef_http(code=403)
    def http_post(self, url, data={}):
        ret = util.HTTP().post(url, data=data, headers={"X-Token":self.token, "Content-Type": "application/json"})
        return ret

    def http_put(self, url, data={}):
        ret = util.HTTP().put(url, data=data, headers={"X-Token":self.token, "Content-Type": "application/json"})
        return ret

    def http_patch(self, url, data={}):
        ret = util.HTTP().patch(url, data=data, headers={"X-Token":self.token, "Content-Type": "application/json"})
        return ret
    
    def http_delete(self, url, data={}):
        ret = util.HTTP().delete(url, data=data, headers={"X-Token":self.token, "Content-Type": "application/json"})
        return ret

    def list_group(self):
        url = f"""{self.host}/api/host/group/"""
        ret = self.http_get(url)
        # log.info(json.dumps(ret))
        return ret

    def edit_user(self, _id, phone, name, role_ids=[4]):
        url = f"""{self.host}/api/account/user/"""
        data = {
            "id":_id,
            "username":phone,
            "nickname":name,
            "password":"******",
            "role_ids":role_ids,
            "wx_token":None
            }
        ret = self.http_post(url, data)
        return ret

    def create_user(self, phone, name, passwd, role):
        url = f"""{self.host}/api/account/user/"""
        data = {"username":phone,"nickname":name,"password":passwd,"role_ids":[role]}
        ret = self.http_post(url, data)
        return ret

    def create_group(self, name, parent_id=2):
        url = f"""{self.host}/api/host/group/"""
        data = {"parent_id":parent_id,"name":os.path.basename(name)}
        ret = self.http_post(url, data)
        # 这个函数几乎就不会失败
        return not ret["error"]

    def list_host(self):

        url = f"""{self.host}/api/host/"""
        ret = self.http_get(url)
        # log.info(ret["data"])
        return ret["data"]
        
    def delete_host(self, hid):
        url = f"""{self.host}/api/host/?id={hid}"""
        ret = self.http_delete(url)
        return ret

    def create_host(self, name, hostname="frps", port=7520, user="root", passwd="WanRong@cloud.cn", group=1):
        url = f"""{self.host}/api/host/"""
        payload = {
            "group_ids":[group],
            "name":name,
            "username":user,
            "hostname":hostname,
            "port":str(port)
        }
        ret = self.http_post(url, payload)
        return ret

    def move_host(self, hid, to_gid, old_gid):
        url = f"""{self.host}/api/host/"""
        payload = {
            "host_ids"   : [hid],
            "s_group_id" : old_gid,
            "t_group_id" : to_gid,
            "is_copy"    : False
            }
        ret = self.http_patch(url, payload)
        return ret

    def set_passwd(self, user_id, password):
        url = f"""{self.host}/api/account/user/"""
        payload = {"id": user_id, "password": password}
        ret = self.http_patch(url, payload)
        return ret

    def verify_host(self, hid):
        url = f"""{self.host}/api/host/"""
        payload = {
            "id":hid
        }
        ret = self.http_put(url, payload)
        return ret

    def execute(self, cmd, host_ids= []):
        # 暂时还不行，不开ws搞不定
        url = f"""{self.host}/api/exec/do/"""
        payload = {"interpreter":"sh","host_ids":host_ids,"command":cmd}
        ret = self.http_post(url, payload)
        return ret

    def notify(self):
        url = f"""{self.host}/api/notify/"""
        ret = self.http_get(url)
        return ret["data"]

    def list_user(self):
        url = f"""{self.host}/api/account/user/"""
        ret = self.http_get(url)
        return ret["data"]

    def list_role(self):
        url = f"""{self.host}/api/account/role/"""
        ret = self.http_get(url)
        return ret["data"]

class HOST():
    def __init__(self, api=None, conf={}):
        self.api  = api
        self.conf = conf

    @property
    def name(self):
        return self.conf["name"]

    @property
    def _id(self):
        return self.conf["id"]

    @property
    def cpu(self):
        return self.conf["cpu"]

    @property
    def memory(self):
        return self.conf["memory"]

    @property
    def disk(self):
        return self.conf["disk"]

    @property
    def os_type(self):
        return self.conf["os_type"]

    @property
    def username(self):
        return self.conf["username"]

    @property
    def hostname(self):
        return self.conf["hostname"]

    @property
    def port(self):
        return self.conf["port"]

    @property
    def gid(self):
        return self.conf["group_ids"][0]

    @property
    def desc(self):
        return self.conf["desc"]

    def move_to(self, gid):
        self.api.move_host(self._id, gid, self.gid)

    def execute(self, cmd):
        ret = self.api.execute(cmd, [self._id])
        return ret

    def dumps(self):
        '''{
                "id": 7,
                "name": "185d3c9cb52930716705ed08a38a7789",
                "hostname": "frps",
                "port": 7540,
                "username": "root",
                "pkey": null,
                "desc": null,
                "is_verified": true,
                "created_at": "2022-10-11 17:53:27",
                "created_by_id": 1,
                "host_id": 7,
                "instance_id": null,
                "zone_id": null,
                "cpu": 4,
                "memory": 8.0,
                "disk": [ 477, 224 ],
                "os_name": "CentOS Linux 7 (Core)",
                "os_type": "centos",
                "private_ip_address": [ "192.168.10.52" ],
                "public_ip_address": [],
                "instance_charge_type": "",
                "internet_charge_type": "",
                "created_time": null,
                "expired_time": null,
                "updated_at": "2022-10-11 17:53:28",
                "instance_charge_type_alias": "",
                "internet_charge_type_alisa": "",
                "group_ids": [ 7 ]
            }'''
        keys = ["name", "cpu", "memory", "disk", "os_type", "private_ip_address", "public_ip_address", "os_name", "created_at", "updated_at"]
        return { _:self.conf.get(_, "") for _ in keys}

    def __repr__(self):
        return f"""[{self._id} {self.name}] {self.username}@{self.hostname}:{self.port} ({self.cpu}核{self.memory}G)"""

def get_all_dirs(data):
    info = { data["name"] : data["key"] }
    if not "children" in data:
        return info
    for i in data["children"]:
        ret = get_all_dirs(i)
        info.update(ret)
    return info

class SPUG():
    def __init__(self, host="", user="", passwd="", token=None):
        self.api = SpugAPI(host=host, user=user, passwd=passwd, token=token)
        if not token:
            ret = self.api.login()
            log.info(ret)

    def check_token(self):
        try:
            ret = self.api.notify()
            # log.info("token校验通过")
        except:
            log.info("token已过期")
            # log.info(dumpstack())
            return False
        return True

    def lshost(self):
        # strace()
        infos = self.api.list_host()
        hosts = [ HOST(self.api, _) for _ in infos ]
        return hosts

    def lsgroup(self):
        data = self.api.list_group()
        info = {}
        for _ in data["data"]["treeData"]:
            ret = get_all_dirs(_)
            info.update(ret)
        return info

    def gexists(self, path="test"):
        # 找到group，则返回gid
        gnames = self.lsgroup()
        return gnames.get(path, None)

    def hexists(self, hostname="test"):
        # 找到host，则返回 host

        hosts = self.lshost()
        host_maps = { _.name:_ for _ in hosts}
        return host_maps.get(hostname, None)

    def mkgroup(self, path="CDN/test"):
        gid = self.gexists(path)
        if gid != None:
            return gid
        father = os.path.dirname(path)
        if not father:
            father_id = 0
        else:
            father_id = self.gexists(father)
            if father_id == None:
                father_id = self.mkgroup(father)
        ret = self.api.create_group(path, father_id)
        # log.info(ret)
        return self.gexists(path)

    def getgid(self, gname):
        # 找不到就创建，并返回gid
        gid = self.gexists(gname)
        if gid:
            return gid
        ret = self.mkgroup(gname)
        return ret

    def lsuser(self):
        ret = self.api.list_user()
        return ret

    def lsrole(self):
        ret = self.api.list_role()
        return ret

    def create_host(self, name, hostname="", port=7520, user="root", passwd="", group=""):
        host = self.hexists(name)
        if host:
            return host

        gid = self.getgid(group)
        ret = self.api.create_host(name, hostname, port, user, passwd, gid)
        self.api.verify_host(ret["data"]["id"])
        return ret["data"]["id"]
        
    def delete_host(self, name):
        host = self.hexists(name)
        if not host:
            return True
        ret = self.api.delete_host(host._id)
        return True if not ret['error'] else False

def get_spug_admin():
    token = api_get("api")
    if token:
        return SPUG(token=token)
    else:
        admin = SPUG()
        api_save(admin.api.user, admin.api.token)
        return admin


