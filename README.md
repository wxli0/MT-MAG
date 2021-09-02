# Requirements

Python 3.7.9

Matlab 

Bash 

# Installation

git clone https://github.com/wxli0/MLDSP.git

git clone https://github.com/wxli0/MT-MAG.git

Modify the paths in MT-MAG/config.py if MT-MAG and/or MLDSP are not cloned in the root directory.

# MT-MAG commands to run existing tasks

To run a small task

- python exec_entire_process.sh task_metadata/Archaea.json

To run Task 1 : simulated/sparse

- python exec_entire_process.sh task_metadata/HGR-r202.json

To run Task 2: real/dense dataset

- python exec_entire_process.sh task_metadata/GTDB-r202.json

In the json file, five attributes are specified:

- ranks: List[str]. Mandatory. All ranks with increasing classification depth in the taxonomy

- data_type: str. Mandatory. Name of the task. Results per rank will be stored in outputs-${data_type}/*. Final results will be stored in ${data_type}-full-prediction-path.csv

- base_path: str. Mandatory. Path to the training and testing dataset directories.

- test_dir:  str. Mandatory. Name of the test dataset folder within base_path.

- root_taxon: str. Mandatory. Root taxon of the task. We assume test genomes are in base_path+test_dir+root_taxon. e.g. d__Bacteria for Task 1, root for Task 2

- partial: bool. Optional (default False). Enables partial classification or not. 

- variability: float. Optional (default 0.2). Variability bewteen the training dataset and test dataset

# commands to see benchmark result for MT-MAG Task 1: simulated/sparse dataset) and Task 2: real/dense dataset

- python3 result_stat.py