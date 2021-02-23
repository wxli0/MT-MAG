import os
import sys

# e.g. python3 run_train_eval_preprocessing.py everything
dir = sys.argv[1]

os.system("python3 preprocessing.py "+dir)
os.system("python3 preprocessing.py "+dir+"_train")
os.system("python3 run_preprocessing.py "+dir+"_eval")
