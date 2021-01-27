import sys
import os
import pandas as pd 
import openpyxl
import json
import matplotlib.pyplot as plt
import numpy as np

# alpha: changed manually
# argv[1]: file_name
# argv[2]: sheet_name
# argv[3]: alpha, threshold
# e.g.

file_path = sys.argv[1]
sheet = sys.argv[2]

df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)

binwidth = 0.01
data = df['max'].tolist()
plt.hist(data, density=True, bins=np.arange(min(data), max(data) + binwidth, binwidth))
if not os.path.isdir('outputs/'+file_path.split('/')[1][:-5]+'-hist'):
    os.mkdir('outputs/'+file_path.split('/')[1][:-5]+'-hist')
plt.savefig('outputs/'+file_path.split('/')[1][:-5]+'-hist/'+sheet[:-2]+'-hist.png')



