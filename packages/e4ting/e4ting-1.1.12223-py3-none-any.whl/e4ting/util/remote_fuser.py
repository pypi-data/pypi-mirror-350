#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    挂载设备文件系统
    Add By : cdj <e4ting@qq.com> 2021-01-22 19:09:05
"""

from __future__ import with_statement

import os
import sys
import errno
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack

from fuse import FUSE, FuseOSError, Operations

from e4ting import util,log

class AntiyNode(Operations):
    def __init__(self, uid):
        self.uid = uid
        self.dev = Device(uid=uid)

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(str(self.uid), partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        util.log(path, mode)
        # if not os.access(full_path, mode):
        if not self.dev.fuse("access", path, mode):
            raise FuseOSError(errno.EACCES)
        # return self.dev.fuse("access", path, mode)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        util.log(path, mode)
        # return os.chmod(full_path, mode)
        return self.dev.fuse("chmod", path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        util.log(path, uid, gid)
        # return os.chown(full_path, uid, gid)
        return self.dev.fuse("chown", path, uid, gid)

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        util.log(path, fh)
        # if self.dev.fuse("access", path, 1):
        #   raise FuseOSError(errno.EACCES)
        # st = os.lstat(full_path)
        # return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
        #            'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        ret = self.dev.fuse("getattr", path, fh)
        if "errno" in ret:
            raise OSError(ret["errno"], ret["strerror"], ret["filename"])
        return ret

    def readdir(self, path, fh):
        full_path = self._full_path(path)
        util.log(full_path)
        # dirents = ['.', '..']
        # if os.path.isdir(full_path):
        #   dirents.extend(os.listdir(full_path))
        dirents = self.dev.fuse("readdir", path, fh)
        for r in dirents:
            yield r
        # return self.dev.fuse("readdir", path, fh)

    def readlink(self, path):
        util.log(path)
        # pathname = os.readlink(self._full_path(path))
        # if pathname.startswith("/"):
        #   # Path name is absolute, sanitize it.
        #   return os.path.relpath(pathname, self.root)
        # else:
        #   return pathname
        return self.dev.fuse("readlink", path)

    def mknod(self, path, mode, dev):
        # return os.mknod(self._full_path(path), mode, dev)
        return self.dev.fuse("mknod", path, mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        util.log(full_path)
        # return os.rmdir(full_path)
        return self.dev.fuse("rmdir", path)

    def mkdir(self, path, mode):
        util.log(path, mode)
        # return os.mkdir(self._full_path(path), mode)
        return self.dev.fuse("mkdir", path, mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        # stv = os.statvfs(full_path)
        util.log(full_path)
        # return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
        #   'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
        #   'f_frsize', 'f_namemax'))
        if self.dev["status"] == 'online':
            return self.dev.fuse("statfs", path)
        else:
            raise OSError(2, "dev [{}] is offline".format(self.uid))

    def unlink(self, path):
        util.log(path)
        # return os.unlink(self._full_path(path))
        return self.dev.fuse("unlink", path)

    def symlink(self, name, target):
        util.log(target, name, "<===>", self._full_path(target), self._full_path(name))
        # return os.symlink(self._full_path(target), self._full_path(name))
        return self.dev.fuse("symlink", name, target)

    def rename(self, old, new):
        util.log(old, new)
        # return os.rename(self._full_path(old), self._full_path(new))
        return self.dev.fuse("rename", old, new)

    def link(self, target, name):
        util.log(target, name)
        # return os.link(self._full_path(target), self._full_path(name))
        return self.dev.fuse("link", target, name)

    def utimens(self, path, times=None):
        util.log(path, times)
        # return os.utime(self._full_path(path), times)
        return self.dev.fuse("utimens", path, times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        util.log(full_path)
        # return os.open(full_path, flags)
        return self.dev.fuse("open", path, flags)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        util.log(full_path)
        # return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)
        return self.dev.fuse("create", path, mode, fi)

    def read(self, path, length, offset, fh):
        util.log(path, length, offset, fh)
        # os.lseek(fh, offset, os.SEEK_SET)
        # return os.read(fh, length)
        data = self.dev.fuse("read", path, length, offset, fh)
        ret = util.b64decode(data)
        # strace()
        return ret

    def write(self, path, buf, offset, fh):
        # os.lseek(fh, offset, os.SEEK_SET)
        util.log(path, buf[0:10], offset, fh)
        # return os.write(fh, buf)
        return self.dev.fuse("write", path, util.b64encode(buf), offset, fh)

    def truncate(self, path, length, fh=None):
        # full_path = self._full_path(path)
        # util.log(full_path)
        # with open(full_path, 'r+') as f:
        #   f.truncate(length)
        return self.dev.fuse("truncate", path, length, fh)

    def flush(self, path, fh):
        util.log(path, fh)
        # return os.fsync(fh)
        ret = self.dev.fuse("flush", path, fh)
        if ret and "errno" in ret:
            raise OSError(ret["errno"], ret["strerror"], ret["filename"])
        return ret

    def release(self, path, fh):
        util.log(path, fh)
        # return os.close(fh)
        return self.dev.fuse("release", path, fh)

    def fsync(self, path, fdatasync, fh):
        util.log(path, fdatasync, fh)
        # return self.flush(path, fh)
        return self.dev.fuse("fsync", path, fdatasync, fh)

# def main(mountpoint, root):
#   FUSE(Passthrough(root), mountpoint, foreground=True)

def save_pid(uid):
    pid = os.getpid()
    open("/var/run/{}".format(uid), "w+").write(str(pid))

def main(mountpoint, uid, foreground):
    util.log("将 {} 挂载到 {}".format(uid, mountpoint))
    FUSE(Passthrough(uid), mountpoint, foreground=foreground)
    save_pid()
    util.log("已挂载")

if __name__ == '__main__':
    util.log(sys.argv)
    option = argv_parse()
    mount = option.mount or "/mnt/{}".format(option.uid)
    util.mkdir(mount)
    main(mount, option.uid, option.foreground)