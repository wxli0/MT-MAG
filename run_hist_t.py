
import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import os

# e.g. python3 run_rejection_f.py outputs/fft-p__Bacteroidota.xlsx rejection_threshold/p__Bacteroidota.json 
file_name = sys.argv[1]


xls = pd.ExcelFile(file_name)
for sheet in xls.sheet_names:
    if sheet.endswith('-t'):
        os.system("python3 add_hist.py  "+ file_name+" " +sheet)
        print(sheet + " done")

