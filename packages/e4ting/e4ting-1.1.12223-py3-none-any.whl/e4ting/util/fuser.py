import os
import sys
import errno

from traceback  import format_exc as dumpstack

from e4ting import log

class Fuse():
    def __init__(self, root):
        self.root = root
        os.linesep = ""
        self.win  = os.name == 'nt'

    # Helpers
    # =======

    def _full_path(self, partial):
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
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        log.info((full_path))
        # if not os.access(full_path, mode):
        #   raise FuseOSError(errno.EACCES)
        return os.access(full_path, mode)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        log.info((full_path))
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        log.info((full_path))
        if hasattr(os, "chown"):
            return os.chown(full_path, uid, gid)
        return None

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        log.info((full_path))
        st = os.lstat(full_path)
        # return {
        #     key:getattr(st, key)
        #         for key in ('n_fields', 'n_sequence_fields', 'n_unnamed_fields',
        #            'st_atime', 'st_atime_ns', 'st_ctime', 'st_ctime_ns', 'st_dev',
        #            'st_file_attributes', 'st_gid', 'st_ino', 'st_mode',
        #            'st_mtime', 'st_mtime_ns', 'st_nlink', 'st_size', 'st_uid','st_rdev','st_blocks','st_blksize') if hasattr(st, key)
        # }
        ret = dict((key, getattr(st, key)) for key in [_ for _ in dir(st) if not _.startswith('_')])
        ret = {k:v for k,v in ret.items() if not hasattr(v, "__call__")}
        return ret

    def readdir(self, path, fh):
        full_path = self._full_path(path)
        log.info((full_path))
        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        return dirents

    def readlink(self, path):
        # if path in [ '~', '/~' ]:
        #   if
        #   return os.path.relpath(os.path.expanduser('~')[2:], self.root)
        pathname = os.readlink(self._full_path(path))
        log.info((pathname))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        log.info((full_path))
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        log.info((path))
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        log.info((full_path))
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree','f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag','f_frsize', 'f_namemax'))

    def unlink(self, path):
        log.info((path))
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        log.info(("{} {}".format(name, target)))
        # return os.symlink(self._full_path(target), self._full_path(name))
        return os.symlink(target, name)

    def rename(self, old, new):
        log.info(("{} {}".format(old, new)))
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        log.info(("{} {}".format(target, name)))
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        log.info(("{} {}".format(path, times)))
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        log.info((full_path))
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        log.info((full_path))
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        # log.info(("{} {} {} {}".format(path, length, offset, fh)))
        os.lseek(fh, offset, os.SEEK_SET)
        return util.b64encode(os.read(fh, length))

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        buf = util.b64decode(buf)
        # log.info(("{} {} {} {}".format(path, buf, offset, fh)))
        # windows下 os.write 会自动把 \n 转成 \r\n，你特么倒是提供个关闭的接口啊， 傻逼玩意，操蛋！！！！！ 不知道该怎么解决才好，md5不一样了啊，混蛋
        # https://stackoverflow.com/questions/1223289/how-to-write-native-newline-character-to-a-file-descriptor-in-python
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        log.info((full_path))
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        log.info(("{} {}".format(path, fh)))
        try:
            return os.fsync(fh)
        except:
            return

    def release(self, path, fh):
        log.info(("{} {}".format(path, fh)))
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        log.info(("{} {} {}".format(path, fdatasync, fh)))
        return self.flush(path, fh)

    # def __getitem__(self, func):
    #     return getattr(self, func)