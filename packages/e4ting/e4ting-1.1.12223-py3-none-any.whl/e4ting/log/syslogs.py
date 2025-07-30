#!/bin/python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    By :陈狍子 e4ting@qq.com 2025-03-15 13:21:38
"""

from . import logger
import logging,os,socket
from logging.handlers import SysLogHandler

import msgpack

class E4Syslog(SysLogHandler):
    def dump(self, record):
        return msgpack.dumps([record.asctime, record.funcName, record.levelname, record.message])

    def emit(self, record):
        try:
            msg = self.dump(record)
            if self.unixsocket:
                try:
                    self.socket.send(msg)
                except OSError:
                    self.socket.close()
                    self._connect_unixsocket(self.address)
                    self.socket.send(msg)
            elif self.socktype == socket.SOCK_DGRAM:
                self.socket.sendto(msg, self.address)
            else:
                self.socket.sendall(msg)
        except Exception:
            self.handleError(record)

host = os.environ.get("SYSLOG", "")
if host:
    hander = E4Syslog((host, 514), SysLogHandler.LOG_AUTH)
    hander.setLevel(logging.ERROR)
    logger.addHandler(hander)
    # logging.basicConfig(level=logging.INFO,
    #     format="[%(asctime)s][%(funcName)s %(levelname)s] %(message)s",
    #     datefmt='%Y-%m-%d %H:%M:%S',
    #     handlers=[logging.StreamHandler(), KySyslog((host, 514), SysLogHandler.LOG_AUTH)]
    #     )