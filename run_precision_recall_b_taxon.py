
import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import os
import platform


file_name = sys.argv[1]

BK_path = ""
if platform.node() == 'q.vector.local':
    BK_path = "/h/wanxinli/BlindKameris-new/"

xls = pd.ExcelFile(file_name)
for sheet in xls.sheet_names:
    if sheet.endswith('-p'):
        print(BK_path+"precision_recall_taxon.py ")
        print("before python3 "+BK_path+"precision_recall_taxon.py " + BK_path+file_name+ " " +  '"'+sheet[:-4] +'"'+ " > " + BK_path+file_name[:-5]+'-'+sheet[:-4]+'-pr-log.txt')
        # os.system("python3 precision_recall_taxon.py " + file_name+ " " +  sheet[:-4])

        os.system("python3 "+BK_path+"precision_recall_taxon.py " + BK_path+file_name+ " " +  '"'+sheet[:-4] +'"'+ " > " + BK_path+file_name[:-5]+'-'+sheet[:-4]+'-pr-log.txt')
        print(sheet + " done")

