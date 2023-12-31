"""
Author: Taony
Date: 2023-04-05 15:07:02
LastEditors: Taony
LastEditTime: 2023-12-30 18:02:20
FilePath: \ForFun\managaDataProcess\childGetInfo.py
"""
import shutil
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
        self.excludedFileName = ""
        self.managaInfosFileName = ""
        self.metaFileName = ""
        self.originMetaFileName = ""

    # def getInfos(self):
    #     fTree = os.listdir(self.rootPath)
    #     if(self.excludedFileName):
    #         fTree.remove(self.excludedFileName)
    #     if(self.managaInfosFileName in fTree):
    #         fTree.remove(self.managaInfosFileName)

    #     managaNum = len(fTree)
    #     managas = list()

    #     for i in range(managaNum):
    #         managa = list()
    #         managaFolderPath = self.rootPath + fTree[i] + '\\'
    #         managa.append(fTree[i])
    #         with open( managaFolderPath + self.metaFileName, 'a+', encoding='utf-8') as f:
    #             f.seek(0)
    #             metaInfo = f.readline()

    def metaTxt2JsonConvert(self):
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
                        encoding = chardet.detect(subMetaInfo)['encoding']
                        if encoding.lower().startswith('utf-8'):
                            subMetaInfo = subMetaInfo.decode('utf-8-sig')
                        metaAttrs = subMetaInfo.strip("\n").split(":")
                        setattr(
                            managaInfomation,
                            self.managaManagementConstants.metaCHN2ENGDict[metaAttrs[0].strip(
                            )],
                            str(metaAttrs[-1].strip()),
                        )
                        managaInfomation.Id = str(i)
                    json.dump({k:v for k,v in managaInfomation}, fp=fJson,
                            cls=ManagaJsonEncoder, ensure_ascii=False)
        except:
            logging.exception(managaFolderPath + "异常")
        else:
            logging.info('转换完成！')


# def main():
    # fatherpath, fTree = getMessage()
    # itemNum = len(fTree)
    # items = list()

    # for i in range(itemNum):
    #     item = list()
    #     path = fatherpath + fTree[i] + "\\"
    #     item.append(fTree[i])
    #     with open(path + "Information.txt", "a+", encoding="utf-8") as fo:
    #         fo.seek(0)
    #         info = fo.readlines()
    #         if len(info) == 3:
    #             if info[-1][-1:] == "\n":
    #                 fo.write("备注: ")
    #             else:
    #                 fo.write("\n备注:")
    #             info.append("")
    #         for subInfo in info:
    #             item.append(subInfo.strip("\n").split(":")[-1].strip())

    #     items.append(item)

    # item_df = pd.DataFrame(items)
    # headerName = ["文件夹名", "名称", "作者", "是否有修", "备注"]
    # writer = pd.ExcelWriter(fatherpath + "Informations.xlsx")
    # item_df.to_excel(writer, header=headerName, index=False)
    # writer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rootPath", type=str, default="T:\\temp\\acg temp\\幼驯染\\", help="根目录文件路径"
    )
    parser.add_argument(
        "--excludedFileName", type=str, default="感觉太像了", help="排除的文件夹名"
    )
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
    managaManagement.excludedFileName = args.excludedFileName
    managaManagement.managaInfosFileName = args.managaInfosFileName
    managaManagement.metaFileName = args.metaFileName
    managaManagement.originMetaFileName = args.originMetaFileName

    managaManagement.metaTxt2JsonConvert()
