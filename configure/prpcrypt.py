#!usr/bin/env python
# -*- coding:utf-8 -*-

'''
modity_time = 12-21-2017
加密模块，实例化对象prpcrypt()
传入_key（16bit）进行标定，默认_key为:roamarroundworld
- encrypt 加密函数：传入文本，返回加密文本（过程为二进制）
- decrypt 解密函数：传入加密文本，返回源文本
- write_file 套装写入文件函数，传入文本text，路径path，文件名filename
- read_file 套装读取文本函数，传入路径path，文件名filename

- 直接调用：
    - 含参数则调用write_file写为默认路径文件名加密文件
    - 无参数调用read_file查看默认路径文件名加密文件

加密方式为：AES 16位
'''

import os
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class prpcrypt():
    def __init__(self, _key="roamarroundworld"):
        self._key = _key
        self._mode = AES.MODE_CBC

    def __encrypt(self, text):    # 加密
        '''
        传入文本，返回加密内容
        '''
        cryptor = AES.new(self._key, self._mode, self._key)
        length = 16     # 16位加密方式
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)      # 长度补零
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext).decode("utf-8")

    def __decrypt(self, text):    # 解码
        '''
        传入加密文本，返回源码
        '''
        cryptor = AES.new(self._key, self._mode, self._key)
        plain_text = cryptor.decrypt(a2b_hex(text)).decode('utf-8').rstrip("\0")
        return plain_text

    def write_file(self, text="", path="", filename="default.txt"):
        '''
        传入并加密，生成文本，默认路径为本地，默认文件名为default.txt
        '''
        if path:
            path += os.path.sep
        if text:
            with open(path + filename, "w") as f:
                f.write(self.__encrypt(text))

    def read_file(self, path="", filename="default.txt"):
        '''
        读取加密文本，默认路径为本地，默认文件名为default.txt
        '''
        if path:
            path += os.path.sep
        if os.path.isfile(path + filename):
            with open(path + filename, "r") as f:
                return self.__decrypt(f.read())
        else:
            return "There's no file exists."

if __name__ == '__main__':
    import sys
    argv = {}
    try:
        argv = sys.argv[1]
    except:
        pass
    prp = prpcrypt()
    if argv:
        prp.write_file(text=argv)
    else:
        print(prp.read_file())
