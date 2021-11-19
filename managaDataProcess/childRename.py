import shutil
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
    ftree.remove('Informations.xlsx')
    return fatherpath, ftree


def main():
    fatherpath, ftree = getMessage()

    n = 0

    for i in ftree:
        path = fatherpath + ftree[n] + '\\'
        f = os.listdir(path)
        f.remove('Information.txt')
        for k in f.copy():
            matchObj = re.match('E', k)
            if matchObj:
                f.remove(k)
        m = 0
        count = 0
        for j in f:
            count = count + 1
            oldname = path + f[m]
            filename, ftype = os.path.splitext(oldname)
            newname = path + str(count).zfill(3) + ftype
            os.rename(oldname, newname)

            m = m + 1

        n = n + 1


if __name__ == '__main__':
    main()
