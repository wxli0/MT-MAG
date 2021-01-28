
import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import os


file_name = sys.argv[1]


xls = pd.ExcelFile(file_name)
for sheet in xls.sheet_names:
    if sheet.endswith('-p'):
        # os.system("python3 precision_recall_taxon.py " + file_name+ " " +  sheet[:-4])

        os.system("python3 precision_recall_taxon.py " + file_name+ " " +  sheet[:-4] + " > " + file_name[:-5]+'-pr/'+file_name[:-5]+'-'+sheet+'-log.txt')
        print(sheet + " done")

