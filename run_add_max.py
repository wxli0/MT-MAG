import os
import sys
import pandas as pd

file_name = sys.argv[1]
xls = pd.ExcelFile(file_name)
print(xls.sheet_names)
for sheet in xls.sheet_names:
    if sheet.endswith('-b-p') or sheet.endswith('-t-p'):
        print("in run_add_max, sheet is:", sheet)
        os.system("python3 add_max.py "+file_name+" "+ '"' +sheet+ '"')
        print(sheet + " done")

