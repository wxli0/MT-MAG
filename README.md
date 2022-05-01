# Requirements

(1) Python >= 3.7.9, in addition to the standard packages in anaconda3, and the following packages are required:
- biopython
- bs4
- openpyxl
- xlrd == 1.2.0

(2) Matlab 

(3) grep >= 3.1


# Installation

git clone https://github.com/wxli0/MLDSP.git

git clone https://github.com/wxli0/MT-MAG.git

Modify the paths in MT-MAG/config.py if MT-MAG and/or MLDSP are not cloned in the root directory.

# Tasks

The Tasks that we present in the paper are:

- Task 1 (sparse): The dataset for Task  1 was specifically chosen so as to allow a direct comparison between the quantitative performance  of MT-MAG and that of [DeepMicrobes](https://github.com/MicrobeLab/DeepMicrobes). The genomes that the training sets for Task 1 were based on comprise only 2.4 \% of the GTDB at the Species level. The training set was prepared using 2,505 representative genomes of human gut microbial species, and the test set was prepared using 3,269 high-quality MAGs reconstructed from human gut microbiomes from  a European Nucleotide Archive study titled ``A new genomic blueprint of the human gut microbiota''.

- Task 2 (dense): The training sets used in Task 2 were  based on  genomes comprising  7.7\% of GTDB taxonomy. The training set  was prepared using GTDB R06-RS202. The test set was prepared using 913 full microbial genomes from metagenomic 201
sequencing of cow rumen, which were derived from 43 Scottish cattle

# Data preparation for Task 1 (sparse) and Task 2 (dense)

If you want to prepare data explictly, not using the pipeline in the following section, use the following commands

cd MLDSP/data/preprocess

- Task 1 (sparse): python3 select_sample_cluster.py non-clade-exclusion-r202/GTDB_small.json

- Task 2 (dense): python3 select_sample_cluster.py non-clade-exclusion-r202/[all json files for Task 2]

Or you can download datasets directly at [MT-MAG-data](https://www.dropbox.com/sh/v8zpsr2v4ytohb2/AABzlrlp6U0CTzAcQqyyQbI_a?dl=0)

Note that the dataset for Task 2 (dense) is too large to be stored in one zip, after unzipping order_family_genus_rumen.zip and root_domain_phylum_class.zip, you need to put them into one folder, as the unzipped folder for Task 1 (sparse).

# MT-MAG commands to run existing tasks

cd MT-MAG

screen -S new

In a json file in task_metadata/, five mandatory attributes and two optional attributes are specified:

- ranks: List[str]. Mandatory. All ranks with increasing classification depth in the taxonomy.

- data_type: str. Mandatory. Name of the task. Results per rank will be stored in outputs-data_type/*. Final results will be stored in data_type-full-prediction-path.csv

- suffix: str. Optional (default empty string). Suffix of the names of training sets folder.

- base_path: str. Mandatory. The path to the training and testing dataset directories. Training datasets are stored within base_path. Test datasets are stored within a subfolder (see next attribute test_dir) inside base_path. You are likely to modify this attribute in your json file.

- test_dir:  str. Mandatory. The Name of the test datasets folder within base_path. That is, test genomes are stored in base_path/test_dir.

- root_taxon: str. Mandatory. Root taxon of the task. We assume test genomes are stored in base_path/test_dir/root_taxon. e.g. d__Bacteria for Task 1, root for Task 2

- partial: bool. Optional (default False). Enables partial classification or not. 

- variability: float. Optional (default 0.2). Variability bewteen the training dataset and test dataset.

- accepted_CA: float. Optional (default 0.9). Accepted constrained accuracy when deciding stopping thresholds.

To run a small task

- python exec_entire_process.py task_metadata/Archaea.json

The test dataset is at [d__Archaea.zip](https://drive.google.com/file/d/12QzHooVu7Pqzvd9DVq3FlYRw1f0tLrhz/view?usp=sharing). You need to download, unzip this file, and put it into base_path/test_dir/d__Archaea.

To run Task 1 : simulated/sparse

- python exec_entire_process.py task_metadata/HGR-r202.json

To run Task 2: real/dense dataset

- python exec_entire_process.py task_metadata/GTDB-r202.json

After "python exec_entire_process.py" command, "bash phase.sh -s …" will be running in another screen session. The first classification is the root taxon (root_taxon) classification. When it finishes, it will trigger phylum level classifications, followed by class, order, family, genus level classifications. When missing_ranks should be empty, the program terminates. It will take some time for classifications, and you should monitor if any screen sessions run into memory issues. The basic commands to check screen sessions are:

(1) To find the screen session ID: screen -ls 

(2) Attach to the screen: screen -d -r <screenid>

@REM # commands to see benchmark result for MT-MAG Task 1: simulated/sparse dataset) and Task 2: real/dense dataset

@REM - python3 result_stat.py, you need to 