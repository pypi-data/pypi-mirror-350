#!/bin/python3
# -*- coding:utf-8 -*-
"""
    隐写术（steganography） 模块
    Add By :陈狍子 e4ting@qq.com 2024-05-25 23:23:32
"""
import sys,os
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from e4ting import util,log

'''
'''

class SM2():
    def __init__(self, key="", pub=""):
        if os.path.exists(key):
            self.key = open(key).read()
        else:
            self.key = key
        if os.path.exists(pub):
            self.pub = open(pub).read()
        else:
            self.pub = pub

    def sign(self, data="", file=""):
        if os.path.exists(file):
            data = open(file).read().encde("utf-8")
        # else:
        #     data = data.encode()

        from gmssl import sm2
        sm2_crypt = sm2.CryptSM2(public_key=self.pub, private_key=self.key)
        # 签名
        # strace()
        signature = sm2_crypt.sign_with_sm3(data)
        # log.info((signature, sm2_crypt.verify_with_sm3(signature, data) , util.md5(data) ))
        return signature

    def verify(self, sign, data=b'', file=""):
        if os.path.exists(file):
            data = open(file).read()
        from gmssl import sm2
        sm2_crypt = sm2.CryptSM2(public_key=self.pub, private_key="")
        return sm2_crypt.verify_with_sm3(sign, data)

class Hidden():
    def __init__(self, inputs, output, attach=None, tool=None):
        self.input  = inputs
        self.output = output
        self.attach = attach
        self.tool   = tool

    def read(self):
        import piexif
        exif_data = piexif.load(self.input)
        # sign = exif_data["0th"].get(piexif.ImageIFD.Artist)
        # if sign:
        #     log.info( sign.decode("utf-8"))
        sign = exif_data["Exif"].get(piexif.ExifIFD.UserComment).decode("utf-8")

        from PIL import Image
        with Image.open(self.input) as img:
            # 尝试从图像信息中获取ICC配置
            icc_profile = img.info.get("icc_profile")
        ret = self.tool.verify(sign, icc_profile)
        log.info( ( "签名校验 : ", ret) )
        return icc_profile

    def write(self):
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS
        assert os.path.exists(self.attach)
        content = open(self.attach, "rb").read()

        with Image.open(self.input) as Img:
            # 确保图片处于RGB模式
            img = Img.convert("RGB")
            # 读取ICC Profile (这个应该是你编辑好的包含隐写数据的Profile)
            # 保存图片，附加ICC Profile
            img.save(self.output, "JPEG", icc_profile=content)
            log.info(f"{self.attach} 已写入 {self.output}")

        import piexif
        # 载入JPEG图片的EXIF数据
        exif_dict = piexif.load(self.output)
        # 将二进制数据存储在EXIF注释字段中
        # exif_dict["Exif"][piexif.ExifIFD.UserComment] = util.md5sum(self.attach).encode("utf-8")
        sign = self.tool.sign(content)
        log.info(f"sign={sign}")
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = sign.encode("utf-8")

        # exif_dict["Exif"][piexif.ExifIFD.Copyright] = "e4ting"
        # exif_dict['0th'][piexif.ImageIFD.Artist] = md5sum("__init__.py")

        # 将修改后的EXIF数据写回图片
        piexif.insert(piexif.dump(exif_dict), self.output)

    def create_one_pixel(self):
        from PIL import Image

        # 创建一个只有1个像素的图像，颜色为白色
        img = Image.new('RGB', (1, 1), color = 'white')

        # 保存图像为JPEG格式
        img.save(self.input, 'JPEG')
        log.info(f"写入 {self.input}")

def argv_parse():
    import argparse
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="jpg隐写"
    )
    parser.add_argument(
        '-c', '--create',
        action='store_true',
        default=False,
        help='创建一张只有一个像素的jpg'
    )
    parser.add_argument(
        '-k', '--key',
        action='store',
        type=str,
        default='',
        help='sm2私钥证书, openssl ecparam -out key.pem -name SM2 -param_enc explicit -genkey'
    )
    parser.add_argument(
        '-p', '--pub',
        action='store',
        type=str,
        default='042d08dfd0674eb85d2cff13c9f755ffd0207b8235abff58231158e7c86d88aacb912034ca0243672450d89973e91756d1105990e544290b12c1b89e5d71457076',
        help='sm2公钥证书, openssl ec -in key.pem -pubout -out pub.pem'
    )
    parser.add_argument(
        '-t', '--target',
        action='store',
        type=str,
        default='test.jpg',
        help='目标图片'
    )
    parser.add_argument(
        '-a', '--attach',
        action='store',
        type=str,
        default=None,
        help='隐写的内容,cluster.tar.gz'
    )
    return parser.parse_args()

if __name__ == '__main__':
    op = argv_parse()

    tool = SM2(key=op.key, pub=op.pub)
    # tool.sign(file=op.target)

    hid = Hidden(inputs=op.target, output=f"{op.target}.jpg", attach=op.attach, tool=tool)
    if op.create:
        hid.create_one_pixel()
    elif op.attach:
        hid.write()
    else:
        data = hid.read()

        log.info(data[:128])

