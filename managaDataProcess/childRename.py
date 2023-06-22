'''
Author: Taony
Date: 2023-04-05 15:07:02
LastEditors: Taony
LastEditTime: 2023-04-06 09:47:10
FilePath: \ForFun\managaDataProcess\childRename.py
'''
import os
import io
import sys
import re

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
    if 'Informations.xlsx' in ftree:
        ftree.remove('Informations.xlsx')
    return fatherpath, ftree


def main():
    fatherpath, ftree = getMessage()

    for i in range(len(ftree)):
        path = fatherpath + ftree[i] + '\\'
        f = os.listdir(path)
        f.remove('Information.txt')
        for k in f.copy():
            matchObj = re.match('E', k)
            if matchObj:
                f.remove(k)
        count = 0
        for j in range(len(f)):
            count += 1
            oldname = path + f[j]
            filename, ftype = os.path.splitext(oldname)
            newname = path + str(count).zfill(3) + ftype
            os.rename(oldname, newname)

if __name__ == '__main__':
    main()
