#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import win32api
from pyDes import des,CBC,PAD_PKCS5
import base64

#获取C盘卷序列号
#使用C盘卷序列号的优点是长度短，方便操作，比如1513085707，但是对C盘进行格式化或重装电脑等操作会影响C盘卷序列号。
#win32api.GetVolumeInformation(Volume Name, Volume Serial Number, Maximum Component Length of a file name, Sys Flags, File System Name)
#return('', 1513085707, 255, 65470719, 'NTFS'),volume serial number is  1513085707.
def getCVolumeSerialNumber():
    CVolumeSerialNumber=win32api.GetVolumeInformation("C:\\")[1]
    #print chardet.detect(str(CVolumeSerialNumber))
    if CVolumeSerialNumber:
        return str(CVolumeSerialNumber) #number is long type，has to be changed to str for comparing to content after.
    else:
        return 0

# 必须8位字符
Des_IV = str.encode( getCVolumeSerialNumber()[0:8].zfill(8) )

# Des CBC
# 自定IV向量
# Des_IV = b"\xef\xab\x56\x78\x90\x34\xcd\x12"

def DesEncrypt(str,key):
    # str 明文password
    # key uid
    Des_Key = (key+"0000")[0:8]
    k = des(Des_Key, CBC, Des_IV, pad=None, padmode=PAD_PKCS5)
    EncryptStr = k.encrypt(str)
    return base64.b64encode(EncryptStr) #转base64编码返回

def DesDecrypt(str,key):
    # str 密文password
    # key uid
    Des_Key = (key+"0000")[0:8]
    EncryptStr = base64.b64decode(str)
    # print(EncryptStr)
    k = des(Des_Key, CBC, Des_IV, pad=None, padmode=PAD_PKCS5)
    DecryptStr = k.decrypt(EncryptStr)
    return DecryptStr


print(getCVolumeSerialNumber()[0:8].zfill(8))
# 加密
print(DesEncrypt('1234','xxxxxxxx'))

# 解密
print(DesDecrypt('aiSE6s6OGPQ=','xxxxxxxx'))
