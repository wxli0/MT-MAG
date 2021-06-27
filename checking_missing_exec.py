import pandas as pd 
import os 
import sys
import platform
import subprocess

# check missing predictions in HGR/MLDSP-prediction-full-path.csv

def check_missing(path, ranks):
    df = pd.read_csv(path, index_col=0, header=0, dtype = str)

    # init missing_ranks
    missing_ranks = {}
    for r in ranks:
        missing_ranks[r] = []

    for index, row in df.iterrows():
        pre_pred = 'root'
        for r in ranks:
            cur_pred = str(df.loc[index][r])
            if 'reject' in cur_pred:
                break
            if cur_pred == 'nan':
                # print(index, row)
                if pre_pred not in missing_ranks[r]:
                    missing_ranks[r].append(pre_pred)
                break
            pre_pred = cur_pred

    return missing_ranks

base_path = "/Users/wanxinli/Desktop/project.nosync/"
if platform.platform()[:5] == 'Linux':
    base_path = "/home/w328li/"

exec = False
if len(sys.argv) == 2:
    exec = sys.argv[1]

# execute the commands
path1 = base_path+"BlindKameris-new/outputs-r202/MLDSP-prediction-full-path.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
mrs1 = check_missing(path1, ranks1)
print("GTDB missing ranks are:", mrs1)

path2 = base_path+"BlindKameris-new/outputs-HGR-r202/HGR-prediction-full-path.csv"
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
mrs2 = check_missing(path2, ranks2)
print("HGR missing ranks are:", mrs2)
if exec:
    for k in mrs2:
        classes = mrs2[k]
        if len(classes) != 0:
            for c in classes:
                running_proc = str(subprocess.check_output("ps aux|grep w328li|grep "+c, shell=True))
                proc_all =  str(subprocess.check_output("screen -ls", shell=True))
                if running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40:
                    os.system('screen -dm bash -c "cd ~/MLDSP; bash phase_HGR.sh "'+c)
                    print('enter screen -dm bash -c "cd ~/MLDSP; bash phase_HGR.sh "'+c)
                elif proc_all.count('\\n') > 40:
                    print('too many processes running')
                else:
                    print(c, "in running process")

