import pandas as pd 
import os 
import sys
import platform
import subprocess
from find_single_child import find_single_child

# check single child taxons and exec single child classifications
path1 = "./outputs-r202/MLDSP-prediction-full-path.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus']
dir1 = '/mnt/sda/MLDSP-samples-r202/'
single_child_taxons1 = find_single_child(path1, ranks1, dir1)
print("single_child taxons for GTDB are:", single_child_taxons1)

path2 = "./outputs-HGR-r202/HGR-prediction-full-path.csv"
ranks2 = ['phylum', 'class', 'order', 'family', 'genus']
dir2 = '/mnt/sda/DeepMicrobes-data/labeled_genome-r202/'
suffix2 = "_split_pruned"
single_child_taxons2 = find_single_child(path2, ranks2, dir2, suffix=suffix2)
print("single_child taxons for HGR are:", single_child_taxons2)


for taxon in single_child_taxons1:
    running_proc = str(subprocess.check_output("ps aux|grep w328li|grep "+taxon, shell=True))
    proc_all =  str(subprocess.check_output("screen -ls", shell=True))
    if running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40 \
        and not os.path.exists('outputs-r202/test-c__Methanobacteria.xlsx'):
            os.system("screen -dm bash -c "+"cd ~/MLDSP; matlab -r "+"'run \
                addme;stackedMain("+"'GTDB'"+", '"+taxon+"', 'rumen_mags/"+taxon+"');exit")
            print("enter screen -dm bash -c "+"cd ~/MLDSP; matlab -r "+"'run \
                addme;stackedMain("+"'GTDB'"+", '"+taxon+"', 'rumen_mags/"+taxon+"');exit")
    elif proc_all.count('\\n') > 40:
        print('too many processes running')
    elif running_proc.count('\\n') > 2:
        print(taxon, "in GTDB running process")
    else:
        print(taxon, "GTDB completed")

for taxon in single_child_taxons2:
    running_proc = str(subprocess.check_output("ps aux|grep w328li|grep "+taxon, shell=True))
    proc_all =  str(subprocess.check_output("screen -ls", shell=True))
    if running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40 \
        and not os.path.exists('outputs-r202/test-c__Methanobacteria.xlsx'):
            os.system("screen -dm bash -c "+"cd ~/MLDSP; matlab -r "+"'run \
                addme;stackedMain("+"'HGR'"+", '"+taxon+"', 'hgr_mags/"+taxon+"');exit")
            print("enter screen -dm bash -c "+"cd ~/MLDSP; matlab -r "+"'run \
                addme;stackedMain("+"'HGR'"+", '"+taxon+"', 'hgr_mags/"+taxon+"');exit")
    elif proc_all.count('\\n') > 40:
        print('too many processes running')
    elif running_proc.count('\\n') > 2:
        print(taxon, "in HGR running process")
    else:
        print(taxon, "HGR completed")