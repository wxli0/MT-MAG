# preprocessing output to send it to R reliabilitydiag 

import sys
import numpy as np 
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import shutil
import json 
import platform
import math
import statistics

# python3 reliability_diag_entire.py outputs-r202/o__UBA1407_train.xlsx

def write_to_file(vec, file_name):
    print("file_name is:", file_name)
    if os.path.exists(file_name):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    file = open(file_name, append_write)
    for e in vec:
        file.write(str(e)+'\n')
    file.close()


ver = 'r202'
file_name = sys.argv[1]
parent = file_name.split('/')[1][:-11]
xls = pd.ExcelFile(file_name)
taxons = [x[:-4] for x in xls.sheet_names]
print(taxons)

# read sheets
for taxon in taxons:
    print("reading in sheet:", taxon)
    sheet = taxon + '-b-p'
    df = pd.read_excel(file_name, sheet_name=sheet, index_col=0, header=0)
    for taxon_other in taxons:
        file_X = 'outputs-'+ver+'/'+parent+'-'+taxon_other+'-rej-X.txt'
        file_Y = 'outputs-'+ver+'/'+parent+'-'+taxon_other+'-rej-Y.txt'
        write_to_file(df[taxon_other].tolist(), file_X)
        if taxon_other == taxon:
            write_to_file([1]*df.shape[0], file_Y)
        else:
            write_to_file([0]*df.shape[0], file_Y)

for taxon in taxons:
    print("generating reliablity diagram for", taxon)
    arg = parent+'/'+taxon
    os.system("Rscript reliability_diag_single.R '"+arg+"'")

print("parent is:", parent)
score_file_path = 'outputs-'+ver+'/'+parent+'-score.txt'
score_file = open(score_file_path, 'r')
score_file_lines = score_file.readlines()
 
print("plotting histogram of scores")
scores = []
for line in score_file_lines:
    scores.append(float(line))
plt.hist(scores)
plt.savefig('outputs-'+ver+'/'+parent+'-score.png')







    
    
            
        