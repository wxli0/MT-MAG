
import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import os

# e.g. python3 run_rejection.py outputs/fft-o__Bacteroidales.xlsx 0.84

file_name = sys.argv[1]
alpha = sys.argv[2]


xls = pd.ExcelFile(file_name)
for sheet in xls.sheet_names:
    if sheet.endswith('-t'):
        os.system("python3 add_rejection.py  "+ file_name+" " +sheet + " "+alpha)
        print(sheet + " done")

