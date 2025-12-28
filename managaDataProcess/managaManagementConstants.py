'''
Author: Taony
Date: 2023-12-31 18:11:38
LastEditors: Taony
LastEditTime: 2024-02-07 23:02:30
FilePath: \ForFun\managaDataProcess\managaManagementConstants.py
'''
"""
Author: Taony
Date: 2023-12-31 16:42:40
LastEditors: Taony
LastEditTime: 2023-12-31 16:55:04
FilePath: \ForFun\managaDataProcess\ManagaManagementConstants.py
"""


class ManagaManagementConstants:
    metaENG2CHNDict = {
        "Id": "序列号",
        "Name": "名称",
        "Author": "作者",
        "Uncorrected": "有无修正",
        "Name": "名称",
        "RecommendationLevel": "推荐等级",
        "Notes": "备注",
    }
    metaCHN2ENGDict = {
        "序列号": "Id",
        "名称": "Name",
        "作者": "Author",
        "有无修正": "Uncorrected",
        "名称": "Name",
        "推荐等级": "RecommendationLevel",
        "备注": "Notes",
    }
    recommendationLevelNum2StrDict = {"0": "无", "1": "推荐", "2": "强烈推荐"}
    recommendationLevelStr2NumDict = {"无": "0", "推荐": "1", "强烈推荐": "2"}
    remakeNum2StrDict = {"0": "无重制计划", "1": "有重制计划"}
    remakeStr2NumDict = {"无重制计划": "0", "有重制计划": "1"}
    uncorrectedNum2StrDict = {"0": "无", "1": "半", "2": "有"}
    uncorrectedStr2NumDict = {"无": "0", "半": "1", "有": "2"}
    excludeTypeDict = {"文件夹": "folders", "文件": "files", "文件类型": "extension"}

    RECOMMEND = recommendationLevelStr2NumDict["推荐"]
    HIGHLY_RECOMMEND = recommendationLevelStr2NumDict["强烈推荐"]
    REMAKE_PLAN = remakeStr2NumDict["有重制计划"]
