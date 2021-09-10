# Requirements

Python 3.7.9

Matlab 

grep >= 3.1

# Installation

git clone https://github.com/wxli0/MLDSP.git

git clone https://github.com/wxli0/MT-MAG.git

Modify the paths in MT-MAG/config.py if MT-MAG and/or MLDSP are not cloned in the root directory.

# MT-MAG commands to run existing tasks

cd MT-MAG

screen -S new

In a json file in task_metadata/, five mandatory attributes and two optional attributes are specified:

- ranks: List[str]. Mandatory. All ranks with increasing classification depth in the taxonomy.

- data_type: str. Mandatory. Name of the task. Results per rank will be stored in outputs-data_type/*. Final results will be stored in data_type-full-prediction-path.csv

- base_path: str. Mandatory. The path to the training and testing dataset directories. Training datasets are stored within base_path. Test datasets are stored within a subfolder (see next attribute test_dir) inside base_path. You are likely to modify this attribute in your json file.

- test_dir:  str. Mandatory. The Name of the test datasets folder within base_path. That is, test genomes are stored in base_path/test_dir.

- root_taxon: str. Mandatory. Root taxon of the task. We assume test genomes are stored in base_path/test_dir/root_taxon. e.g. d__Bacteria for Task 1, root for Task 2

- partial: bool. Optional (default False). Enables partial classification or not. 

- variability: float. Optional (default 0.2). Variability bewteen the training dataset and test dataset.

To run a small task

- python exec_entire_process.py task_metadata/Archaea.json

The test dataset is at [d__Archaea.zip](https://drive.google.com/file/d/12QzHooVu7Pqzvd9DVq3FlYRw1f0tLrhz/view?usp=sharing). You need to download, unzip this file, and put it into base_path/test_dir/d__Archaea.

To run Task 1 : simulated/sparse

- python exec_entire_process.py task_metadata/HGR-r202.json

To run Task 2: real/dense dataset

- python exec_entire_process.py task_metadata/GTDB-r202.json

# commands to see benchmark result for MT-MAG Task 1: simulated/sparse dataset) and Task 2: real/dense dataset

- python3 result_stat.py