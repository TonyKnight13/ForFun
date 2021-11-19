import pandas as pd
import os

df_train = pd.read_table(
    ".\\dataProcess\\file\\neg_v1.txt", header=None, sep='\t')
df_now = pd.read_table(
    ".\\dataProcess\\file\\1022.txt", header=None, sep='\t')
df_r = pd.read_table(".\\dataProcess\\file\\relation2id.txt",
                     header=None, sep='  ', encoding='utf-8', engine='python')
rlist = df_r[0].tolist()

olist = list()
# nlist = list()
clist = list()

for tup in zip(df_train[0], df_train[1], df_train[2]):
    olist.append(tup)

# for t in olist:
#     for r in rlist:
#         nlist.append((t[0],r,t[2]))

for tup in zip(df_now[0], df_now[1], df_now[2]):
    clist.append(tup)

nlist = list(set(clist) - set(olist) & set(clist))

# nlist = list(set(nlist) - set(olist))

l0 = list()
l1 = list()
l2 = list()

for t in nlist:
    l0.append(t[0])
    l1.append(t[1])
    l2.append(t[2])

data = pd.DataFrame([l0, l1, l2])
data = data.T


data.to_csv('1022_v2.txt', sep='\t', header=None, index=False)
