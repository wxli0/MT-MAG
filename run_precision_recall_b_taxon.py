
import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import os
import platform


file_name = sys.argv[1]

BK_path = ""
print("node is:", platform.node())
if platform.node() == 'q.vector.local' or platform.node().startswith('guppy'):
    BK_path = "/h/wanxinli/BlindKameris-new/"

xls = pd.ExcelFile(file_name)
for sheet in xls.sheet_names:
    if sheet.endswith('-p'):
        print(BK_path+"precision_recall_taxon.py ")
        print(BK_path+file_name)
        print("before python3 "+BK_path+"precision_recall_taxon.py " + file_name+ " " +  '"'+sheet[:-4] +'"'+ " > " + file_name[:-5]+'-'+sheet[:-4]+'-pr-log.txt')

        os.system("python3 "+BK_path+"precision_recall_taxon.py " + file_name+ " " +  '"'+sheet[:-4] +'"'+ " > " + file_name[:-5]+'-'+sheet[:-4]+'-pr-log.txt')
        print(sheet + " done")

