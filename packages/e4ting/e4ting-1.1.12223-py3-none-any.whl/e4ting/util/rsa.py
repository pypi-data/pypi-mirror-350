#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :e4ting e4ting@gmail.com 2023-12-05 14:44:32
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

from rsa import transform, core, PublicKey

def rsa_decrypt(encrypt_text):
    b_pem_public_key = open("public.pem", 'rb').read()
    key = PublicKey.load_pkcs1_openssl_pem(b_pem_public_key)
    d = key.e
    n = key.n
    num = transform.bytes2int(encrypt_text)
    decrypto = core.decrypt_int(num, d, n)
    out = transform.int2bytes(decrypto)
    sep_idx = out.index(b"\x00", 2)
    out = out[sep_idx + 1:]
    return out.decode('utf-8')