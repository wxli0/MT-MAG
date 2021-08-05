from find_single_child import find_single_child
import os 
import pandas as pd 
import subprocess
import time

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
i = 0

remove = False
if remove:
    for taxon in single_child_taxons1:
        if os.path.exists(os.path.expanduser("~/MLDSP/outputs-r202/test-"+taxon+".xlsx")):
            os.remove(os.path.expanduser("~/MLDSP/outputs-r202/test-"+taxon+".xlsx"))
    for taxon in single_child_taxons2:
         if os.path.exists(os.path.expanduser(\
            '~/MLDSP/outputs-HGR-r202/test-'+taxon+'_split_pruned.xlsx')):
            os.remove(os.path.expanduser(\
            '~/MLDSP/outputs-HGR-r202/test-'+taxon+'_split_pruned.xlsx'))
print("removed existing single child output files")

while True:
    print("iteration:", i)
    test_cat = "GTDB"
    for taxon in single_child_taxons1:
        print("processing", taxon)
        running_proc = str(subprocess.check_output("ps aux|grep w328li|grep "+taxon, shell=True))
        proc_all =  str(subprocess.check_output("screen -ls", shell=True))
        if os.path.exists(os.path.expanduser("~/MLDSP/outputs-r202/test-"+taxon+".xlsx")):
            print(taxon, "in GTDB completed")
        elif running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40 \
            and not os.path.exists(os.path.expanduser("~/MLDSP/outputs-r202/test-"+taxon+".xlsx")):
                os.system("screen -dm bash -c "+"\"cd ~/MLDSP; bash phase_classify.sh "+test_cat+" "+taxon+"\"")
                print("screen -dm bash -c "+"\"cd ~/MLDSP; bash phase_classify.sh "+test_cat+" "+taxon+"\"")
        elif proc_all.count('\\n') > 40:
            print('too many processes running')
        elif running_proc.count('\\n') > 2:
            print(taxon, "in GTDB running process")
    test_cat = "HGR"
    for taxon in single_child_taxons2:
        running_proc = str(subprocess.check_output("ps aux|grep w328li|grep "+taxon, shell=True))
        proc_all =  str(subprocess.check_output("screen -ls", shell=True))
        if os.path.exists(os.path.expanduser(\
            '~/MLDSP/outputs-HGR-r202/test-'+taxon+'_split_pruned.xlsx')):
            print(taxon, "in HGR completed")
        elif running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40 \
            and not os.path.exists(os.path.expanduser(\
                '~/MLDSP/outputs-HGR-r202/test-'+taxon+'_split_pruned.xlsx')):
            os.system("screen -dm bash -c "+"\"cd ~/MLDSP; bash phase_classify.sh "+test_cat+" "+taxon+"\"")     
            print("screen -dm bash -c "+"\"cd ~/MLDSP; bash phase_classify.sh "+test_cat+" "+taxon+"\"") 
        elif proc_all.count('\\n') > 40:
            print('too many processes running')
        elif running_proc.count('\\n') > 2:
            print(taxon, "in HGR running process")

            
    print("sleep for 10 min")
    time.sleep(600) # sleep for 10 mins