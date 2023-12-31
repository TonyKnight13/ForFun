"""
Author: Taony
Date: 2023-04-05 15:07:02
LastEditors: Taony
LastEditTime: 2023-12-30 18:02:20
FilePath: \ForFun\managaDataProcess\childGetInfo.py
"""
import os
import io
import sys
import re
import string
import numpy as np
import pandas as pd
import argparse

import chardet
import json
import logging
from managaManagementConstants import ManagaManagementConstants
from managaInfo import ManagaInfo
from managaJsonEncoder import ManagaJsonEncoder

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


class ManagaManagement:
    managaManagementConstants = ManagaManagementConstants()

    def __init__(self) -> None:
        self.rootPath = ""
        self.fatherPath = ""
        self.excludedFileName = ""
        self.managaInfosFileName = ""
        self.metaFileName = ""
        self.originMetaFileName = ""

    # 将*.txt转换为*.json，并丰富元信息字段
    def convertMetaTxt2Json(self):
        fTree = os.listdir(self.rootPath)
        if self.excludedFileName:
            fTree.remove(self.excludedFileName)
        if self.managaInfosFileName in fTree:
            fTree.remove(self.managaInfosFileName)

        managaNum = len(fTree)
        try:
            for i in range(managaNum):
                managa = list()
                managaFolderPath = self.rootPath + fTree[i] + "\\"
                managa.append(fTree[i])
                with open(
                    managaFolderPath + self.originMetaFileName, "rb"
                ) as fTxt, open(
                    managaFolderPath + self.metaFileName, "w", encoding="utf-8"
                ) as fJson:
                    managaInfomation = ManagaInfo()
                    fTxt.seek(0)
                    metaInfo = fTxt.readlines()
                    assert len(metaInfo) == 4
                    for subMetaInfo in metaInfo:
                        encoding = chardet.detect(subMetaInfo)["encoding"]
                        if encoding.lower().startswith("utf-8"):
                            subMetaInfo = subMetaInfo.decode("utf-8-sig")
                        metaAttrs = subMetaInfo.strip("\n").split(":")
                        setattr(
                            managaInfomation,
                            self.managaManagementConstants.metaCHN2ENGDict[
                                metaAttrs[0].strip()
                            ],
                            str(metaAttrs[-1].strip()),
                        )
                        managaInfomation.Id = str(i)
                    json.dump(
                        {k: v for k, v in managaInfomation},
                        fp=fJson,
                        cls=ManagaJsonEncoder,
                        ensure_ascii=False,
                    )
        except:
            logging.exception(managaFolderPath + "异常")
        else:
            logging.info("转换完成！")

    def getInfos(self):
        fTree = os.listdir(self.rootPath)
        if self.excludedFileName:
            fTree.remove(self.excludedFileName)
        if self.managaInfosFileName in fTree:
            fTree.remove(self.managaInfosFileName)

        managaNum = len(fTree)
        managaMetaInfos = list()
        try:
            for i in range(managaNum):
                managaFolderPath = self.rootPath + fTree[i] + "\\"
                with open(
                    managaFolderPath + self.metaFileName, "r+", encoding="utf-8"
                ) as f:
                    metaInfoJsonDict = json.load(fp=f)
                    metaInfoDict = {
                        self.managaManagementConstants.metaCHN2ENGDict[k]: v
                        for k, v in metaInfoJsonDict.items()
                    }
                    managaInfo = ManagaInfo(**metaInfoDict)
                    # 数据库记录与对象做映射：...
                    if managaInfo.Id == '':
                        # 新增：如果数据库检索不到作者+作品名，则数据库新增记录；否则抛出异常。
                        pass
                    else:
                        # 修改：如果数据库数据与内存数据不一致，记入日志。
                        pass

                    managaInfo.Path = self.fatherPath + fTree[i] + "\\"
                    if '-r' in fTree[i]:
                        managaInfo.RecommendationLevel = str(1)
                    if '-spr' in fTree[i]:
                        managaInfo.RecommendationLevel = str(2)
                    if '(re)' in fTree[i]:
                        managaInfo.remake = str(1)

                    managaMetaInfos.append(managaInfo.__dict__)
        except:
            logging.exception(managaFolderPath + "异常")
        else:
            managaInfoDataFrame = pd.DataFrame(
                managaMetaInfos, columns=[k for k in managaInfo.__dict__.keys()]
            )
            managaInfoDataFrame.to_csv(
                self.rootPath + self.managaInfosFileName, index=False, sep=","
            )
            logging.info(self.rootPath + self.managaInfosFileName + "录入完成！")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rootPath", type=str, default="T:\\temp\\acg temp\\幼驯染\\", help="根目录文件路径"
    )
    parser.add_argument("--fatherPath", type=str, default=".\\幼驯染\\", help="父目录文件路径")
    parser.add_argument("--excludedFileName", type=str, default="感觉太像了", help="排除的文件夹名")
    parser.add_argument(
        "--managaInfosFileName",
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

    managaManagement = ManagaManagement()
    managaManagement.rootPath = args.rootPath
    managaManagement.fatherPath = args.fatherPath
    managaManagement.excludedFileName = args.excludedFileName
    managaManagement.managaInfosFileName = args.managaInfosFileName
    managaManagement.metaFileName = args.metaFileName
    managaManagement.originMetaFileName = args.originMetaFileName

    # managaManagement.convertMetaTxt2Json()
    managaManagement.getInfos()