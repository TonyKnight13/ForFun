'''
Author: Taony
Date: 2023-12-30 16:45:46
LastEditors: Taony
LastEditTime: 2023-12-31 13:20:01
FilePath: \ForFun\managaDataProcess\managaInfo.py
'''
import json
from managaManagementConstants import ManagaManagementConstants


class ManagaInfo:
    managaManagementConstants = ManagaManagementConstants()
    def __init__(self) -> None:
        self.Id = ''
        self.Name = ''
        self.Author = ''
        self.Uncorrected = '0'
        self.RecommendationLevel = '0'
        self.Notes = ''

    def __iter__(self):
        yield from {
            k:getattr(self, v) for k,v in self.managaManagementConstants.metaCHN2ENGDict.items()
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()
