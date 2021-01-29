
import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import os


sheet_name = sys.argv[1]
taxon = sys.argv[2]



os.system("python3 add_softmax.py outputs/glv_test.xlsx "+" " +sheet_name)
print("add_softmax.py done")
print("python3 add_rejection_f.py outputs/glv_test.xlsx "+sheet_name+"-p"+" " + "rejection_threshold/"+sheet_name[:-2]+"_glv.json")
os.system("python3 add_rejection_f.py outputs/glv_test.xlsx "+sheet_name+"-p"+" " + "rejection_threshold/"+sheet_name[:-2]+"_glv.json")
print("add_rejection_f.py done")
print("python3 add_true_prediction.py outputs/glv_test.xlsx "+sheet_name+"-p " + taxon)
os.system("python3 add_true_prediction.py outputs/glv_test.xlsx "+sheet_name+"-p " + taxon)
print("add_true_prediction.py done")

