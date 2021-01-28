import os
import sys
import pandas as pd

file_name = sys.argv[1]
xls = pd.ExcelFile(file_name)
for sheet in xls.sheet_names:
    if sheet.endswith('-b') or sheet.endswith('-t'):
        os.system("python3 add_softmax.py "+file_name+" "+sheet)
        print(sheet + " done")

