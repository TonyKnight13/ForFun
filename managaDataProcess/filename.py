import shutil
import os
import io
import sys
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def getMessage():
    fatherpath = input('请输入根目录文件路径(结尾加上\)：')
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

    n = 0

    for i in ftree:
        path = fatherpath + ftree[n] + '\\'
        f = os.listdir(path)

        for k in f:
            matchObj = re.match('E', k)
            if matchObj:
                f.remove(k)

        m = 0
        count = 0

        for j in f:
            matchObj = re.match('E', j)
            if matchObj:
                None
            else:
                count = count + 1
                oldname = path + f[m]
                filename, ftype = os.path.splitext(oldname)
                newname = path + str(count).zfill(3) + ftype
                os.rename(oldname,newname)
            m = m + 1

        n = n + 1


if __name__ == '__main__':
    main()

























# fatherpath = "E:\\temp\\幼驯染\\"

# ftree = os.listdir(fatherpath)

# ftree.remove('感觉太像了')

# n = 0

# for i in ftree:
#     path = fatherpath + ftree[n] + '\\'
#     f = os.listdir(path)

#     for k in f:
#         matchObj = re.match('E', k)
#         if matchObj:
#             f.remove(k)

#     m = 0
#     count = 0

#     for j in f:
#         matchObj = re.match('E', j)
#         if matchObj:
#             None
#         else:
#             count = count + 1
#             oldname = path + f[m]
#             filename, ftype = os.path.splitext(oldname)
#             newname = path + str(count).zfill(3) + ftype
#             os.rename(oldname,newname)
#         m = m + 1

#     n = n + 1
#     # print(path)
# print("--------------------------------------------------")
