import argparse
import itertools
import json
import os
import logging
import zipfile

from mangaDataProcess.osananajimi.mangaManagementConstants import mangaManagementConstants


class mangaManagement:
    def __init__(self) -> None:
        self.rootPath = ""
        self.excludedFileNames = ""

    def getFtree(self):
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
            logging.exception(self.excludedFileNames + "异常")
        return fTree

    def collectImgGroup(self):
        fTree = self.getFtree()
        groupDict = dict()
        for key, group in itertools.groupby(fTree, lambda x: x.split('_')[0]):
            groupDict[key.split('_')[0]] = list(group)
        return groupDict

    def zip(self):
        groupDict = self.collectImgGroup()
        for k, v in groupDict.items():
            with zipfile.ZipFile(os.path.join(self.rootPath, k + '.zip'), 'w') as zipObj:
                for f in v:
                    zipObj.write(os.path.join(self.rootPath, f), f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rootPath", type=str, default="D:\\Comic\\SOLA\\han\\纯情女攻略计划\\", help="根目录文件路径"
    )
    parser.add_argument("--excludedFileNames", type=str,
                        default="{\"folders\":[],\"files\":[\"cover.jpg\"],\"extension\":[\".zip\"]}",
                        help="排除的文件、文件夹名")

    args = parser.parse_args()
    mangaManagement = mangaManagement()
    mangaManagement.rootPath = args.rootPath
    mangaManagement.excludedFileNames = args.excludedFileNames
    mangaManagement.zip()
