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

a_probs = []
b_probs = []
mag_ids = []
for index, row in df.iterrows():
    x = row['d__Archaea-d__Bacteria']
    a_probs.append(1/(1+exp(-x)))
    b_probs.append( 1-1/(1+exp(-x)))
    mag_ids.append(index)

df_probs = pd.DataFrame()
df_probs['d__Archaea'] = a_probs
df_probs['d__Bacteria'] = b_probs
df_probs['MAG'] = mag_ids
df_probs = df_probs.set_index('MAG')


df_probs['max'] = np.max(df_probs, axis=1)
df_probs['prediction'] = pred


with pd.ExcelWriter(file_path, engine="openpyxl", mode='a') as writer:  
    df_probs.to_excel(writer, sheet_name = sheet+'-p', index=True)
writer.save()
writer.close()



