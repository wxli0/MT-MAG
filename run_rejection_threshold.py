
import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import os
import json

# e.g. python3 run_rejection.py outputs/fft-o__Bacteroidales.xlsx rejection_threshold/

file_name = sys.argv[1]


xls = pd.ExcelFile(file_name)
for sheet in xls.sheet_names:
    if sheet.endswith('-t'):
        alpha = json.load(open(sys.argv[2]))[sheet[:-2]]
        os.system("python3 add_rejection.py  "+ file_name+" " +sheet + " "+alpha)
        print(sheet + " done")

