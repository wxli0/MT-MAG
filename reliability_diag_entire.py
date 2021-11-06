"""
Send MT-MAG result file to R reliabilitydiag 
:param sys.argv[1]: File path of the result file
:type sys.argv[1]: str

:Example python3 reliability_diag_entire.py outputs-GTDB-r202/o__UBA1407_train.xlsx
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys


def write_to_file(vec, file_name):
    if os.path.exists(file_name):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    file = open(file_name, append_write)
    for e in vec:
        file.write(str(e)+'\n')
    file.close()


data_type = sys.argv[1]
parent = sys.argv[2]
file_name = os.path.join('outputs-'+data_type, parent+'_train.xlsx')
xls = pd.ExcelFile(file_name)
taxons = [x[:-4] for x in xls.sheet_names] # remove '-b-p'
print(taxons)

# read sheets
for taxon in taxons:
    print("reading in sheet:", taxon)
    sheet = taxon + '-b-p'
    df = pd.read_excel(file_name, sheet_name=sheet, index_col=0, header=0)
    file_X = os.path.join('outputs-'+data_type, parent+'-rej-X.txt')
    file_Y = os.path.join('outputs-'+data_type, parent+'-rej-Y.txt')
    write_to_file(df['max'].tolist(), file_X)
    df['positive'] = df.apply(lambda row: int(row['prediction'] == taxon), axis=1)
    write_to_file(df['positive'], file_Y)


os.system("Rscript reliability_diag_single.R '"+data_type+"' "+"'"+parent+"'")

# print("parent is:", parent)
# score_file_path = 'outputs-'+ver+'/'+parent+'-score.txt'
# score_file = open(score_file_path, 'r')
# score_file_lines = score_file.readlines()
 
# print("plotting histogram of scores")
# scores = []
# for line in score_file_lines:
#     scores.append(float(line))
# plt.hist(scores)
# plt.savefig('outputs-'+ver+'/'+parent+'-score.png')







    
    
            
        