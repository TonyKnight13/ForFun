'''
题目描述

外星人有自己的语言。虽然他们使用的字母表和英文相同，但是字母的顺序不同。
现在你获得了一部外星人的字典，字典中单词的顺序按照外星人的字母表顺序排列。
通过字典分析出外星人的字母顺序。

Example：

[
  "wrt",
  "wrf",
  "er",
  "ett",
  "rftt"
]
正确顺序是”wertf”。
注释：
1.所有字母均为小写字母
2.如果没有合法的顺序序列，输出空串
3.如果有多个合法的顺序序列，输出任意一个即可
'''

def GuessDic(wordList):
    len = len(wordList)
    indexList = []
    for i in range(len):
        for j in range(len[i]):
            
        
