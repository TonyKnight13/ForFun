import pandas as pd
import numpy as np


df = pd.read_csv('C:\\Users\\Administrator\\Desktop\\1.csv')
print(df)

numad = []


tlast = 1949
ti = 12
tdone = 12
months = np.arange(12)
months += 1 
for d in df.values:
    if d[0] != tlast:  
        if ti != 12:
            tdone = 0  
        tlast = tlast + 1   
        for i in months:
            if tdone:
                ti = i
                if d[1] != i:
                    numad.append([d[0], i, 0])
                else:
                    numad.append(d)                
                    break
            else:
                for j in np.arange(12- ti) + ti +1:
                    numad.append([tlast, j, 0])
                i = 1
                ti = 12

    else:
        for i in np.arange(12- ti) + ti + 1:
            ti = i
            if d[1] != i:
                numad.append([d[0], i, 0])
            else:
                numad.append(d)
                break   
    if ti == 12 :
        tdone = 1

print(numad)