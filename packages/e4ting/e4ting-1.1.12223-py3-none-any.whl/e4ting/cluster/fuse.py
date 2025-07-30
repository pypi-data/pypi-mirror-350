#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting e4ting@gmail.com 2023-11-06 17:07:51
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent
import functools
import base64
import errno

from e4ting import log

def redef_oserror(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            log.debug(function.__name__)
            ret = function(*args, **kwargs)
            # log.info((function.__name__, str(ret)[:100]))
            return ret
        except KeyboardInterrupt as e:
            # 响应 Ctrl + C 中断
            raise e
        except OSError as e:
            log.info(dumpstack())
            return dict(errno=e.errno, strerror=e.strerror, filename=e.filename)
        except Exception as e:
            log.info(dumpstack())
            return dict(errno=errno.EINVAL, strerror=str(e), filename="xxx")
    return wrapper

class FUSE():
    ROOT = "/tmp"

    @staticmethod
    def full_path(partial):
        # log.debug(partial)
        if partial.startswith("/~"):
            partial = partial[1:]
            partial = os.path.expanduser(partial)
            # partial = partial[1:]
            return partial
        elif partial.startswith("~"):
            partial = os.path.expanduser(partial)
            # partial = partial[1:]
            return partial
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(FUSE.ROOT, partial)
        return path

    # Filesystem methods
    # ==================
    @staticmethod
    @redef_oserror
    def access(path, mode):
        """ fuse.access() """
        full_path = FUSE.full_path(path)
        log.debug((full_path))
        # if not os.access(full_path, mode):
        #   raise FuseOSError(errno.EACCES)
        return os.access(full_path, mode)

    @staticmethod
    @redef_oserror
    def chmod(path, mode):
        """ fuse.chmod() """
        full_path = FUSE.full_path(path)
        log.debug((full_path, mode))
        return os.chmod(full_path, mode)

    @staticmethod
    @redef_oserror
    def chown(path, uid, gid):
        """ fuse.chown() """
        full_path = FUSE.full_path(path)
        log.debug((full_path))
        if hasattr(os, "chown"):
            return os.chown(full_path, uid, gid)
        return None

    @staticmethod
    @redef_oserror
    def getattr(path, fh=None):
        """ fuse.getattr() """
        full_path = FUSE.full_path(path)
        log.debug(full_path)
        if not os.path.exists(full_path):
            # return dict(Errno=2, path=path)
            raise OSError(2, "No such file or directory", path)
        st = os.lstat(full_path)
        # return {
        #     key:getattr(st, key)
        #         for key in ("st_mode", "st_ino", "st_dev", "st_nlink", "st_uid", "st_gid", "st_size", "st_atime", "st_mtime", "st_ctime") if hasattr(st, key)
        # }
        # log.debug(dir(st))
        ret = dict((key, getattr(st, key))
                   for key in [_ for _ in dir(st) if not _.startswith('_')])
        ret = {k: v for k, v in ret.items() if not hasattr(v, "__call__")}
        # log.debug(ret)
        return ret

    @staticmethod
    @redef_oserror
    def readdir(path, fh):
        """ fuse.readdir() """
        full_path = FUSE.full_path(path)
        log.debug((full_path))
        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        return dirents

    @staticmethod
    @redef_oserror
    def readlink(path):
        """ fuse.readlink() """
        # if path in [ '~', '/~' ]:
        #   if
        #   return os.path.relpath(os.path.expanduser('~')[2:], ROOT)
        pathname = os.readlink(FUSE.full_path(path))
        log.debug((pathname))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, FUSE.ROOT)
        else:
            return pathname

    @staticmethod
    @redef_oserror
    def mknod(path, mode, dev):
        """ fuse.mknod() """
        return os.mknod(FUSE.full_path(path), mode, dev)

    @staticmethod
    @redef_oserror
    def rmdir(path):
        """ fuse.rmdir() """
        full_path = FUSE.full_path(path)
        log.debug((full_path))
        return os.rmdir(full_path)

    @staticmethod
    @redef_oserror
    def mkdir(path, mode):
        """ fuse.mkdir() """
        log.debug((path))
        return os.mkdir(FUSE.full_path(path), mode)

    @staticmethod
    @redef_oserror
    def statfs(path):
        """ fuse.statfs() """
        full_path = FUSE.full_path(path)
        stv = os.statvfs(full_path)
        log.debug((full_path))
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree', 'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag', 'f_frsize', 'f_namemax'))

    @staticmethod
    @redef_oserror
    def unlink(path):
        """ fuse.unlink() """
        log.debug((path))
        return os.unlink(FUSE.full_path(path))

    @staticmethod
    @redef_oserror
    def symlink(name, target):
        """ fuse.symlink() """
        log.debug(("{} {}".format(name, target)))
        # return os.symlink(FUSE.full_path(target), FUSE.full_path(name))
        return os.symlink(target, name)

    @staticmethod
    @redef_oserror
    def rename(old, new):
        """ fuse.rename() """
        log.debug(("{} {}".format(old, new)))
        return os.rename(FUSE.full_path(old), FUSE.full_path(new))

    @staticmethod
    @redef_oserror
    def link(target, name):
        """ fuse.link() """
        log.debug(("{} {}".format(target, name)))
        return os.link(FUSE.full_path(target), FUSE.full_path(name))

    @staticmethod
    @redef_oserror
    def utimens(path, times=None):
        """ fuse.utimens() """
        if times:
            times = (int(times[0]), int(times[1]))
        log.debug(("{} {}".format(path, times)))
        return os.utime(FUSE.full_path(path), times)

    # File methods
    # ============
    @staticmethod
    @redef_oserror
    def open(path, flags):
        """ fuse.open() """
        full_path = FUSE.full_path(path)
        log.debug((full_path, flags))
        return os.open(full_path, flags)

    @staticmethod
    @redef_oserror
    def create(path, mode, fi=None):
        """ fuse.create() """
        full_path = FUSE.full_path(path)
        log.debug((full_path))
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    @staticmethod
    @redef_oserror
    def read(path, length, offset, fh):
        """ fuse.read() """
        # log.debug("{} {} {} {}".format(path, length, offset, fh))
        os.lseek(fh, offset, os.SEEK_SET)
        ret = os.read(fh, length)
        # log.debug((len(ret), ret))
        return base64.b64encode(ret).decode()

    @staticmethod
    @redef_oserror
    def write(path, buf, offset, fh):
        """ fuse.write() """
        buf = base64.b64decode(buf)
        os.lseek(fh, offset, os.SEEK_SET)
        # log.debug(("{} {} {} {}".format(path, buf, offset, fh)))
        # windows下 os.write 会自动把 \n 转成 \r\n，你特么倒是提供个关闭的接口啊， 傻逼玩意，操蛋！！！！！ 不知道该怎么解决才好，md5不一样了啊，混蛋
        # https://stackoverflow.com/questions/1223289/how-to-write-native-newline-character-to-a-file-descriptor-in-python
        return os.write(fh, buf)

    @staticmethod
    @redef_oserror
    def truncate(path, length, fh=None):
        """ fuse.truncate() """
        full_path = FUSE.full_path(path)
        log.debug((full_path))
        with open(full_path, 'r+') as f:
            f.truncate(length)
        return ""

    @staticmethod
    @redef_oserror
    def flush(path, fh):
        """ fuse.flush() """
        log.debug("{} {}".format(path, fh))
        try:
            return os.fsync(fh)
        except:
            return ""

    @staticmethod
    @redef_oserror
    def release(path, fh):
        """ fuse.release() """
        log.debug("{} {}".format(path, fh))
        return os.close(fh)

    @staticmethod
    @redef_oserror
    def fsync(path, fdatasync, fh):
        """ fuse.fsync() """
        log.debug("{} {} {}".format(path, fdatasync, fh))
        # return flush(path, fh)
        try:
            return os.fsync(fh)
        except:
            return ""

