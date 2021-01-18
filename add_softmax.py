import sys
import os
import pandas as pd 
import openpyxl
import numpy as np
from math import exp

# argv[1]: file_name
# argv[2]: sheet_name
# e.g.

file_path = sys.argv[1]
sheet = sys.argv[2]



def custom_softmax(f_x):
    alpha = 1
    ret = np.zeros(f_x.shape)
    for j in range(f_x.shape[0]):
        r = f_x[j]
        # print("r is:", r)
        nor_r = np.zeros(f_x.shape[1])
        for i in range(len(r)):
            nor_r[i] = alpha*exp(r[i])
            if r[i] > 0:
                nor_r[i] = exp(r[i])
        nor_r /= np.sum(nor_r)
        # print("nor_r is:", nor_r)
        ret[j] = nor_r
    return ret

df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)
pred = df['prediction']
if 'max' in df.columns:
    del df['max']
if 'prediction' in df.columns:
    del df['prediction']
if 'rejection' in df.columns:
    del df['rejection']

df_softmax = pd.DataFrame(custom_softmax(df.to_numpy()), columns=df.columns)
df_softmax['max'] = np.max(df_softmax, axis=1)
df_softmax.index = df.index
df_softmax['prediction'] = pred
print(df_softmax)

wb = openpyxl.load_workbook(file_path)
del wb[sheet]
wb.save(file_path)

with pd.ExcelWriter(file_path, engine="openpyxl", mode='a') as writer:  
    df_softmax.to_excel(writer, sheet_name = sheet, index=True)
writer.save()
writer.close()



