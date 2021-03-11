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

# python3 precision_recall_b.py outputs/fft-o__Oscillospirales.xlsx

gap = 0.01
alphas = np.arange(0, 1+gap, gap).tolist()
file_name = sys.argv[1]

xls = pd.ExcelFile(file_name)
precision = []
recall = []
weighted = []

excel_alpha_info = {}
alpha_num = (1+gap)/gap+1

taxons = [x[:-4] for x in xls.sheet_names]

# calculating excel_alpha_info
for sheet in xls.sheet_names:
    print("sheet is:", sheet)
    if sheet.endswith('-p'):
        df = pd.read_excel(file_name, sheet_name=sheet, index_col=0, header=0)
        sheet_alpha_info = []
        for index, row in df.iterrows():
            print("index adding is:", index)
            round_down_max = math.floor(row['max']*100)/100.0
            pred_num = round_down_max/gap
            true_half = [True]*(int(pred_num))
            true_half.extend([False]*int((alpha_num-pred_num)))
            print("here:", true_half.extend([False]*int((alpha_num-pred_num))))
            excel_alpha_info[index] =  true_half

# seperating dataframes
right_dfs = []
wrong_dfs = []
for i in range(len(xls.sheet_names)):
    wrong_df = pd.DataFrame()
    for j in range(len(xls.sheet_names)):
        cur_df = pd.read_excel(file_name, sheet_name=sheet, index_col=0, header=0)
        if i == j:
            right_dfs.append(cur_df)
        else:
            wrong_df = pd.concat([wrong_df, cur_df], axis=0)
    wrong_dfs.append(wrong_df)

for alpha in alphas:
    reads = [0]*len(xls.sheet_names)
    corrects = [0]*len(xls.sheet_names)
    unassigned = [0]*len(xls.sheet_names)
    for i in range(len(xls.sheet_names)):
        sheet = xls.sheet_names[i]
        right_df = right_dfs[i]
        wrong_df = wrong_dfs[i]
        if right_df.shape[0] == 0 and wrong_df.shape[0] == 0:
            continue
        reads[i] = right_df.loc[df['prediction'] == taxon].shape[0]\
            +wrong_df.loc[df['prediction']].shape[0]
        corrects[i] = 

