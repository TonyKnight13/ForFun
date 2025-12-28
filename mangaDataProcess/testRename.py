'''
Author: Taony
Date: 2024-01-01 00:57:10
LastEditors: Taony
LastEditTime: 2024-01-01 02:03:54
FilePath: \ForFun\mangaDataProcess\testRename.py
'''
import os
import re
from natsort import os_sorted


if __name__ == "__main__":
    mangaFolderPath = 'D:\\Comic\\SOLA\\幼驯染\\415\\'
    fileList = os.listdir(mangaFolderPath)
    fileList.remove('Information.json')
    for pic in fileList.copy():
        matchObj = re.match("E", pic)
        if matchObj:
            fileList.remove(pic)
    
    fileList = os_sorted(fileList)
    for idx in range(len(fileList)):
        originFilePath = mangaFolderPath + fileList[idx]
        _, fileType = os.path.splitext(originFilePath)
        fileName = str(idx + 1).zfill(3) + fileType
        filePath = mangaFolderPath + fileName
        if fileName in fileList:
            existIdx = fileList.index(fileName)
            tempFileName = 'tempForRename' + fileName
            tempFilePath = mangaFolderPath + tempFileName
            os.rename(filePath, tempFilePath)
            fileList[existIdx] = tempFileName
            
        os.rename(originFilePath, filePath)
        fileList[idx] = fileName
