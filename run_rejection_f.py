"""
Wrapper script to call add_rejection_f.py for all sheet in a file

Command line arguments:
:param sys.argv[1]: file_name. Excel file path
:type sys.argv[1]: str
:param sys.argv[2]: thresholds. A json file containing A dictionary of \
    (class, stopping threshold) pairs for taxons in file_name
:type sys.argv[2]: str

Example: python3 run_rejection_f.py outputs/fft-p__Bacteroidota.xlsx rejection_threshold/p__Bacteroidota.json
"""

import os
import pandas as pd
import sys

file_name = sys.argv[1]
thresholds = sys.argv[2]


xls = pd.ExcelFile(file_name)
for sheet in xls.sheet_names:
    if sheet.endswith('-p'):
        os.system("python3 add_rejection_f.py  "+ file_name+" " +sheet + " " +thresholds)
        print(sheet + " done")

