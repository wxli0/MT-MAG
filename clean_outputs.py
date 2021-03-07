import os 
import sys 
import platform

base_path = "/Users/wanxinli/Desktop/project/BlindKameris-new/outputs/"
if platform.platform()[:5] == 'Linux':
    base_path = "/home/w328li/BlindKameris-new/outputs/"

for file in os.listdir(base_path):
    if file.endswith('-pr.png') or file.endswith('-pr-log.txt'):
        print("file is:", file)
        dest_folder = file.split("_train",1)[0]+"_eval"
        if not os.path.isdir(base_path+dest_folder):
            os.mkdir(base_path+dest_folder)
        src = base_path+file
        dest = base_path+dest_folder+"/"+file
        os.rename(src, dest)

