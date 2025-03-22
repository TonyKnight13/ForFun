'''
Author: Taony
Date: 2023-04-05 15:07:02
LastEditors: Taony
LastEditTime: 2023-04-06 10:02:35
FilePath: \ForFun\test.py
'''
# path = 'T:\\temp\\acg temp\\幼驯染\\感觉太像了\\test\\02\\Information.txt'
# with open(path, 'a+', encoding = 'utf-8') as fo:
#     fo.seek(0)
#     info = fo.readlines()
#     print(info)
#     fo.write('备注: ')
#     fo.seek(0)
#     info = fo.readlines()
#     print(info)

import os
import re
import time
import requests
from bs4 import BeautifulSoup
links = ('photos-index-aid-15848554.html','photos-index-aid-55654.html')
x = [re.search(r'aid-(\d+)', link).group(1) for link in links]
print(x)