'''
Author: Taony
Date: 2023-04-05 15:07:02
LastEditors: Taony
LastEditTime: 2023-04-06 10:01:18
FilePath: \ForFun\managaDataProcess\childGetInfo.py
'''
import shutil
import os
import io
import sys
import re
import string
import numpy as np
import pandas as pd

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
    itemNum = len(ftree)
    items = list()
    
    for i in range(itemNum):
        item = list()
        path = fatherpath + ftree[i] + '\\'
        item.append(ftree[i])
        with open(path + 'Information.txt', 'a+', encoding = 'utf-8') as fo:
            fo.seek(0)
            info = fo.readlines()
            if len(info) == 3 :
                if info[-1][-1:] == '\n':
                    fo.write('备注: ')
                else:
                    fo.write('\n备注:')
                info.append('')
            for subInfo in info:
                item.append(subInfo.strip('\n').split(':')[-1].strip())
        
        items.append(item)

    item_df = pd.DataFrame(items)
    headerName = ['文件夹名','名称','作者','是否有修','备注']    
    writer = pd.ExcelWriter(fatherpath + 'Informations.xlsx')
    item_df.to_excel(writer, header=headerName, index=False )
    writer.close()            


if __name__ == '__main__':
    main()
