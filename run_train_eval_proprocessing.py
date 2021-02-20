import os
import sys

dir = sys.argv[1]
files = os.listdir(os.path.join("data", dir))

os.sys("python3 preprocessing.py "+os.path.join(dir))
os.sys("python3 preprocessing.py "+os.path.join(dir+"_train"))
os.sys("python3 run_preprocessing.py "+os.path.join(dir))
