'''
Author: Taony
Date: 2023-12-30 00:51:43
LastEditors: Taony
LastEditTime: 2024-06-21 01:08:50
FilePath: \ForFun\t.py
'''
import json

a = "{\"folders\":[\"a\"],\"files\":[\"b\"]}"
x = json.loads(a)
print(x["folders"][0])
print(json.loads(a))

a = dict()
a['a'] = [1,2,3]

b = a.copy()
b['a'] = [5,6]
c = a.copy()
d = b.copy()
d['a'].append(0)

print(a)
print(b)
print(c)
print(d)