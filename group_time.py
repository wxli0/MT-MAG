"""
Add MT-MAG classification time into corresponding time file

:param sys.argv[1]: dir_cat. The directory of the time files.
:type sys.argv[1]: str

:Example: python3 group_time.py outputs-r202
:Example python3 group_time.py outputs-HGR-r202
"""

import numpy as np
import os
import pandas as pd
import sys


dir_cat = sys.argv[1]
# df = pd.DataFrame(columns = ['taxon', 'train_time', 'test_time', 'rej_time', 'post_time'])
# df = pd.DataFrame(columns = ['taxon', 'test_time'])
df = pd.read_csv(dir_cat+"/time.csv", header=0, index_col=0)
# df = df.set_index('taxon')
time_cats = ['test_time']
print(df.columns)
for time_cat in time_cats:
    time_file = time_cat+'.txt'
    file_path = '/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/'+dir_cat+'/'+time_file
    if not os.path.exists(file_path):
        file_path = '/Users/wanxinli/Desktop/project.nosync/MLDSP-desktop/'+dir_cat+'/'+time_file

    file = open(file_path, 'r')
    lines = file.readlines()
    for line in lines:
        taxon = line.split()[0]
        time_length = int(line.split()[1])
        if taxon not in df.index:
            df.loc[taxon] = {'train_time': np.nan, 'test_time': np.nan, \
                'rej_time': np.nan, 'post_time': np.nan}
        df.at[taxon, time_cat] = time_length

df = df.sort_index()
df.to_csv(dir_cat+"/time.csv")