from find_single_child import find_single_child
import getpass
import os 
import pandas as pd 
import subprocess
import time

"""
Checks single child taxons in and execute single child MT-MAG classifications \
    in HGR/GTDB-prediction-full-path.csv.

No command line arguments are required.
"""

path1 = "./outputs-GTDB-r202/GTDB-prediction-full-path.csv"
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
i = 0

remove = False
if remove:
    for taxon in single_child_taxons1:
        output_path = "./outputs-GTDB-r202/"+taxon+".xlsx"
        if os.path.exists(os.path.expanduser(output_path)):
            os.remove(os.path.expanduser(output_path))
    for taxon in single_child_taxons2:
        output_path = "./outputs-HGR-r202/"+taxon+".xlsx"
        if os.path.exists(os.path.expanduser(output_path)):
            os.remove(os.path.expanduser(output_path))
print("removed existing single child output files")

user_name = getpass.getuser()
while True:
    print("iteration:", i)
    test_cat = "GTDB"
    for taxon in single_child_taxons1:
        print("processing", taxon)
        running_proc = str(subprocess.check_output("ps aux|grep "+user_name+"|grep "+taxon, shell=True))
        proc_all =  str(subprocess.check_output("screen -ls", shell=True))
        if os.path.exists(os.path.expanduser("./outputs-GTDB-r202/"+taxon+".xlsx")):
            print(taxon, "in GTDB completed")
        elif running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40 \
            and not os.path.exists(os.path.expanduser("./outputs-GTDB-r202/"+taxon+".xlsx")):
                os.system("screen -dm bash -c "+"\"cd ~/MLDSP; bash phase_single.sh "+test_cat+" "+taxon+"\"")
                print("screen -dm bash -c "+"\"cd ~/MLDSP; bash phase_single.sh "+test_cat+" "+taxon+"\"")
        elif proc_all.count('\\n') > 40:
            print('too many processes running')
        elif running_proc.count('\\n') > 2:
            print(taxon, "in GTDB running process")
    test_cat = "HGR"
    for taxon in single_child_taxons2:
        running_proc = str(subprocess.check_output("ps aux|grep "+user_name+"|grep "+taxon, shell=True))
        proc_all =  str(subprocess.check_output("screen -ls", shell=True))
        if os.path.exists(os.path.expanduser(\
            './outputs-HGR-r202/'+taxon+'.xlsx')):
            print(taxon, "in HGR completed")
        elif running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40 \
            and not os.path.exists(os.path.expanduser(\
                './outputs-HGR-r202/'+taxon+'.xlsx')):
            os.system("screen -dm bash -c "+"\"cd ~/MLDSP; bash phase_single.sh "+test_cat+" "+taxon+"\"")     
            print("screen -dm bash -c "+"\"cd ~/MLDSP; bash phase_single.sh "+test_cat+" "+taxon+"\"") 
        elif proc_all.count('\\n') > 40:
            print('too many processes running')
        elif running_proc.count('\\n') > 2:
            print(taxon, "in HGR running process")

            
    print("sleep for 10 min")
    time.sleep(600) # sleep for 10 mins
