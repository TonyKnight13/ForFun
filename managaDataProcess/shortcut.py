import sys
import win32com.client
import re
import os


# 注意文件名长度
disk = "G"

fatherPath =  disk + ":\\Comic\\SOLA\\单篇\\系列\\"
ftree = os.listdir(fatherPath)

shell = win32com.client.Dispatch("WScript.Shell")
for folderName in ftree:
    flistpath = fatherPath + folderName + "\\"
    flist = os.listdir(flistpath)
    for f in flist:
        fpath = flistpath + f
        print(fpath)

    shortcut = shell.CreateShortCut(fpath)

    s1 = "D:\\temp\\acg temp\\temp\\本\\"
    s2 = disk + ":\\Comic\\SOLA\\"

    shortcut.Targetpath = shortcut.Targetpath.replace(s1,s2)
    shortcut.save()
# print(shortcut.Targetpath)