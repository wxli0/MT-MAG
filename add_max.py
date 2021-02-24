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



df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)
pred = df['prediction']
if 'max' in df.columns:
    del df['max']
if 'prediction' in df.columns:
    del df['prediction']
if 'rejection' in df.columns:
    del df['rejection']
if 'actual' in df.columns:
    del df['actual']

df_softmax = pd.DataFrame(df.to_numpy(), columns=df.columns)
df_softmax['max'] = np.max(df_softmax, axis=1)
df_softmax.index = df.index
df_softmax['prediction'] = pred
print(df_softmax)


with pd.ExcelWriter(file_path, engine="openpyxl", mode='a') as writer:  
    df_softmax.to_excel(writer, sheet_name = sheet, index=True)
writer.save()
writer.close()



