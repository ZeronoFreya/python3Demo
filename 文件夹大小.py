#!/usr/bin/env python27
import os
from os.path import join, getsize


def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return size


if __name__ == '__main__':
    dirname = 'c:\\Temp'
    maxsize = 50  # 何文件夹于50M删除
    filesize = getdirsize(dirname)
    _mb = round((filesize / float(1024 * 1024)),2)
    print('%s MB' % _mb)
    # if filesize / 1024 / 1024 > maxsize:
    #     os.popen('rm -rf ' + dirname)
    
