import shutil
import os
import io
import sys
import re
import string
import numpy
import pandas as pd
from chardet import detect

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def getMessage():
    fatherpath = input('请输入根目录文件路径：')
    fatherpath = fatherpath + '\\'
    ftree = os.listdir(fatherpath)
    flag = 1
    while(flag):
        delname = input('请输入不需要的文件夹名(没有时输入0)：')  # 缺个异常处理
        if delname == '0':
            flag = 0
        else:
            ftree.remove(delname)
    return fatherpath, ftree


def main():
    fatherpath, ftree = getMessage()

    totalNum = len(ftree)
    fList = []
    n = 0

    for i in ftree:
        path = fatherpath + ftree[n] + '\\'
        fileName = path + 'Information.txt'

        with open(fileName, 'rb+') as fp:
            content = fp.read()
            encoding = detect(content)['encoding']
            print(i + ":")
            print(encoding)
            if encoding == 'GB2312':
                    encoding = 'GB18030'
            content = content.decode(encoding).encode('utf8')
            fp.seek(0)
            fp.write(content)
        n = n + 1

if __name__ == '__main__':
    main()
