"""
Author: Taony
Date: 2023-04-05 15:07:02
LastEditors: Taony
LastEditTime: 2023-12-30 18:02:20
FilePath: \ForFun\mangaDataProcess\childGetInfo.py
"""
import os
import io
import sys
import pandas as pd
import argparse
import json
import logging
import re

import chardet
from natsort import os_sorted

from mangaDataProcess.osananajimi.mangaManagementConstants import mangaManagementConstants
from mangaDataProcess.osananajimi.logProcessor import LogProcessor
from mangaInfo import mangaInfo
from mangaJsonEncoder import mangaJsonEncoder

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

class mangaManagement:
    mangaManagementConstants = mangaManagementConstants()

    def __init__(self) -> None:
        self.rootPath = None
        self.fatherPath = None
        self.excludedFileNames = None
        self.mangaInfosFileName = None
        self.metaFileName = None
        self.originMetaFileName = None

    def getFTree(self):
        fTree = os.listdir(self.rootPath)
        toBeExcludedItems = list()  # 记录被排除的元素
        excludedFolders = json.loads(self.excludedFileNames)[mangaManagementConstants.excludeTypeDict["文件夹"]]
        excludedFiles = json.loads(self.excludedFileNames)[mangaManagementConstants.excludeTypeDict["文件"]]
        excludedExtensions = json.loads(self.excludedFileNames)[mangaManagementConstants.excludeTypeDict["文件类型"]]
        try:
            toBeExcludedItems.extend(excludedFolders)
            toBeExcludedItems.extend(excludedFiles)
            for extension in excludedExtensions:
                for file in fTree:
                    if file.endswith(extension):
                        toBeExcludedItems.append(file)
            for toBeExcludedItem in toBeExcludedItems:
                while toBeExcludedItem in fTree:
                    fTree.remove(toBeExcludedItem)
        except:
            log_processor.exception(self.excludedFileNames + "异常")
        return fTree

    # 将*.txt转换为*.json，并丰富元信息字段
    def convertMetaTxt2Json(self):
        fTree = self.getFTree()

        mangaNum = len(fTree)
        try:
            for i in range(mangaNum):
                manga = list()
                mangaFolderPath = self.rootPath + fTree[i] + "\\"
                manga.append(fTree[i])
                with open(
                    mangaFolderPath + self.originMetaFileName, "rb"
                ) as fTxt, open(
                    mangaFolderPath + self.metaFileName, "w", encoding="utf-8"
                ) as fJson:
                    mangaInfomation = mangaInfo()
                    fTxt.seek(0)
                    metaInfo = fTxt.readlines()
                    assert len(metaInfo) == 4
                    for subMetaInfo in metaInfo:
                        encoding = chardet.detect(subMetaInfo)["encoding"]
                        if encoding.lower().startswith("utf-8"):
                            subMetaInfo = subMetaInfo.decode("utf-8-sig")
                        metaAttrs = subMetaInfo.strip("\n").split(":")
                        setattr(
                            mangaInfomation,
                            self.mangaManagementConstants.metaCHN2ENGDict[
                                metaAttrs[0].strip()
                            ],
                            str(metaAttrs[-1].strip()),
                        )
                        mangaInfomation.Id = str(i)
                    json.dump(
                        {k: v for k, v in mangaInfomation},
                        fp=fJson,
                        cls=mangaJsonEncoder,
                        ensure_ascii=False,
                    )
        except:
            log_processor.exception(mangaFolderPath + "异常")
        else:
            log_processor.info("转换完成！")

    def getInfos(self):
        fTree = self.getFTree()

        mangaNum = len(fTree)
        mangaMetaInfos = list()
        try:
            for i in range(mangaNum):
                mangaFolderPath = self.rootPath + fTree[i] + "\\"
                with open(
                    mangaFolderPath + self.metaFileName, "r+", encoding="utf-8"
                ) as f:
                    metaInfoJsonDict = json.load(fp=f)
                    metaInfoDict = {
                        self.mangaManagementConstants.metaCHN2ENGDict[k]: v
                        for k, v in metaInfoJsonDict.items()
                    }
                    mangaInfomation = mangaInfo(**metaInfoDict)

                    # 数据库记录与对象做映射：...
                    if mangaInfomation.Id == "":
                        # 新增：如果数据库检索不到作者+作品名，则数据库新增记录；否则抛出异常。
                        pass
                    else:
                        # 修改：如果数据库数据与内存数据不一致，记入日志。
                        pass

                    mangaInfomation.Path = self.fatherPath + fTree[i] + "\\"
                    if "-r" in fTree[i]:
                        mangaInfomation.RecommendationLevel = (
                            self.mangaManagementConstants.RECOMMEND
                        )
                    if "-spr" in fTree[i]:
                        mangaInfomation.RecommendationLevel = (
                            self.mangaManagementConstants.HIGHLY_RECOMMEND
                        )
                    if "(re)" in fTree[i]:
                        mangaInfomation.remake = (
                            self.mangaManagementConstants.REMAKE_PLAN
                        )

                    mangaMetaInfos.append(mangaInfomation.__dict__)
        except:
            log_processor.exception(mangaFolderPath + "异常")
        else:
            mangaInfoDataFrame = pd.DataFrame(
                mangaMetaInfos, columns=[k for k in mangaInfomation.__dict__.keys()]
            )
            mangaInfoDataFrame.to_csv(
                self.rootPath + self.mangaInfosFileName, index=False, sep=","
            )
            log_processor.info(self.rootPath + self.mangaInfosFileName + "录入完成！")

    def batchRename(self):
        fTree = self.getFTree()

        mangaNum = len(fTree)

        try:
            for i in range(mangaNum):
                mangaFolderPath = self.rootPath + fTree[i] + "\\"
                fileList = os.listdir(mangaFolderPath)
                fileList.remove(self.metaFileName)
                for pic in fileList.copy():
                    matchObj = re.match("E", pic)
                    if matchObj:
                        fileList.remove(pic)

                # 按操作系统的排序算法进行排序
                fileList = os_sorted(fileList)

                for idx in range(len(fileList)):
                    originFilePath = mangaFolderPath + fileList[idx]
                    _, fileType = os.path.splitext(originFilePath)
                    fileName = str(idx + 1).zfill(3) + fileType
                    filePath = mangaFolderPath + fileName
                    # 将已存在的文件名进行修改，改为临时命名
                    if fileName in fileList:
                        existIdx = fileList.index(fileName)
                        if existIdx == idx:
                            continue
                        tempFileName = 'tempForRename' + fileName
                        tempFilePath = mangaFolderPath + tempFileName
                        os.rename(filePath, tempFilePath)
                        fileList[existIdx] = tempFileName

                    os.rename(originFilePath, filePath)
                    log_processor.info(mangaFolderPath + "重命名完成！" + originFilePath + "->" + filePath)
                    fileList[idx] = fileName
        except:
            log_processor.exception(mangaFolderPath + "异常")
        else:
            log_processor.info(self.rootPath + "重命名完成！")

    def rename(self, process_path):
        fileList = os.listdir(process_path)
        if self.metaFileName in fileList:
            fileList.remove(self.metaFileName)
        for pic in fileList.copy():
            matchObj = re.match("E", pic)
            if matchObj:
                fileList.remove(pic)
        # 按操作系统的排序算法进行排序
        fileList = os_sorted(fileList)
        for idx in range(len(fileList)):
            originFilePath = process_path + fileList[idx]
            _, fileType = os.path.splitext(originFilePath)
            processedFileName = str(idx + 1).zfill(3) + fileType
            processedFilePath = process_path + processedFileName
            # 将已存在的文件名进行修改，改为临时命名
            if processedFileName in fileList:
                existIdx = fileList.index(processedFileName)
                if existIdx == idx:
                    continue
                tempFileName = 'tempForRename' + processedFileName
                tempFilePath = process_path + tempFileName
                os.rename(processedFilePath, tempFilePath)
                fileList[existIdx] = tempFileName
            os.rename(originFilePath, processedFilePath)
            log_processor.info(process_path + "重命名完成！" + originFilePath + "->" + processedFilePath)
            fileList[idx] = processedFileName


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rootPath", type=str, default="D:\\Comic\\SOLA\\幼驯染\\", help="根目录文件路径"
    )
    parser.add_argument("--fatherPath", type=str, default=".\\幼驯染\\", help="父目录文件路径")
    parser.add_argument("--excludedFileNames", type=str, default="{\"folders\":[\"感觉太像了\"],\"files\":[\"sync.ffs_db\", \"Informations.csv\"],\"extension\":[\".zip\"]}", help="排除的文件、文件夹名")
    parser.add_argument("--logPath", type=str,
                        default=os.path.dirname(__file__) + "/logs/",
                        help="日志路径")

    parser.add_argument(
        "--mangaInfosFileName",
        type=str,
        default="Informations.csv",
        help="漫画信息CSV表名",
    )
    parser.add_argument(
        "--metaFileName", type=str, default="Information.json", help="漫画元信息文件名"
    )
    parser.add_argument(
        "--originMetaFileName", type=str, default="Information.txt", help="原漫画元信息文件名"
    )

    args = parser.parse_args()

    log_processor = LogProcessor(
        log_name=args.logPath + "info.log",
        encoding="utf-8",
        log_level=logging.INFO
    )

    mangaManagement = mangaManagement()
    mangaManagement.rootPath = args.rootPath
    mangaManagement.fatherPath = args.fatherPath
    mangaManagement.excludedFileNames = args.excludedFileNames
    mangaManagement.mangaInfosFileName = args.mangaInfosFileName
    mangaManagement.metaFileName = args.metaFileName
    mangaManagement.originMetaFileName = args.originMetaFileName

    # mangaManagement.convertMetaTxt2Json()
    mangaManagement.getInfos()
    mangaManagement.rename()
