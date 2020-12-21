import sys
import os
import pandas as pd 

file_path = sys.argv[1]
sheet = sys.argv[2]
alpha = float(sys.argv[2])

df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)
df['rejection'] = df.apply(lambda row: 'reject' if row['max'] < alpha else row['prediction'], axis=1)
df.to_csv(file_path)



