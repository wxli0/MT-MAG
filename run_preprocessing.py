import os
import sys

dir = sys.argv[1]
files = os.listdir(os.path.join("data", dir))

for file in files:
    os.system("python3 preprocessing.py "+os.path.join("data", dir,file))
    print(file + "done")
