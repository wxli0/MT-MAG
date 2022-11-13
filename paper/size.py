import argparse
from Bio import SeqIO
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--task',  default = 0, type=int, help='1 or 2')
parser.add_argument('--type', default="", type=str, help='training or test')
parser.add_argument('--tool', default="", type=str, help='DeepMicrobes or MT-MAG')
args = parser.parse_args()
task = args.task
tool = args.tool
file_num = 0
contig_num = 0
genome_size = 0

def count_train(data_path, folder_path, suffix = "_trimmed.fa"):
    """
    Counts the genome size, contig number, file number, minimum sequence length and maximum sequence length
    in data_path within folder path for test set
    Assuming the fasta file ends with suffix
    """
    genome_size = 0
    contig_num = 0
    file_num = 0
    len_min = float("inf")
    len_max = float("-inf")
    fasta_sequences = SeqIO.parse(open(data_path), 'fasta')
    for fasta in fasta_sequences:
        _, sequence = fasta.id, str(fasta.seq)
        seq_len = len(sequence)
        genome_size += seq_len
        len_min = min(len_min, seq_len)
        len_max = max(len_max, seq_len)
        contig_num += 1
    for fasta_file in os.listdir(folder_path):
        if fasta_file.endswith(suffix):
            file_num += 1
    return genome_size, contig_num, file_num, len_min, len_max

def count_test(folder_path, suffix = "_trimmed.fa"):
    """
    Counts the genome size, contig number, file number, minimum sequence length and maxmimum sequence length
    in folder path for test set
    Assuming the fasta file ends with suffix
    """
    len_min = float("inf")
    len_max = float("-inf")
    genome_size = 0
    contig_num = 0
    file_num = 0
    
    for fasta_file in os.listdir(folder_path):
        if fasta_file.endswith(suffix):
            file_num += 1
            fasta_sequences = SeqIO.parse(open(os.path.join(folder_path, fasta_file)), 'fasta')
            for fasta in fasta_sequences:
                _, sequence = fasta.id, str(fasta.seq)
                seq_len = len(sequence)
                genome_size += seq_len
                len_min = min(len_min, seq_len)
                len_max = max(len_max, seq_len)
                contig_num += 1
    return genome_size, contig_num, file_num, len_min, len_max

len_min = float("inf")
len_max = float("-inf")
print("printing args parameter, type: ", args.type, " task: ", args.task, " tool: ", args.tool)
if args.type == "training":
    if args.task == 1 and args.tool  == "MT-MAG":
        # command python3 paper/size.py --task=1 --tool=MT-MAG
        data_path = "/mnt/sda/DeepMicrobes-data/labeled_genome-r202/d__Bacteria"
        for dir_nested in os.listdir(data_path):
            for fasta_file in os.listdir(os.path.join(data_path, dir_nested)):
                fasta_sequences = SeqIO.parse(open(os.path.join(data_path, dir_nested, fasta_file)),'fasta') 
                for fasta in fasta_sequences:
                    _, sequence = fasta.id, str(fasta.seq)
                    seq_len = len(sequence)
                    len_min = min(len_min, seq_len)
                    len_max = max(len_max, seq_len)
                    genome_size += seq_len
                    contig_num += 1
                file_num += 1
    elif args.task == 1 and args.tool == "DeepMicrobes":
        # command: python3 paper/size.py --task=1 --tool=DeepMicrobes
        data_path = "/mnt/sda/DeepMicrobes-data/labeled_genome_train_species_reads_author/author_train.fa"
        folder_path = "/mnt/sda/DeepMicrobes-data/labeled_genome_train_species_reads_author"
        genome_size, contig_num, file_num, len_min, len_max = count_train(data_path, folder_path)
    elif args.task == 2 and args.tool == "MT-MAG":
        data_path = "/mnt/sda/MLDSP-samples-r202"
        for dir_nested1 in os.listdir(data_path):
            for dir_nested2 in os.listdir(data_path, dir_nested1):
                for fasta_file in os.listdir(os.path.join(data_path, dir_nested1, dir_nested2)):
                    fasta_sequences = SeqIO.parse(open(os.path.join(data_path, dir_nested1, dir_nested2, fasta_file)),'fasta') 
                    for fasta in fasta_sequences:
                        _, sequence = fasta.id, str(fasta.seq)
                        seq_len = len(sequence)
                        genome_size += seq_len
                        len_min = min(len_min, seq_len)
                        len_max = max(len_max, seq_len)
                        contig_num += 1
                    file_num += 1  
    elif args.task == 2 and args.tool == "DeepMicrobes":
        # command: python3 paper/size.py --task=2 --tool=DeepMicrobes
        data_path_11 = "/mnt/sda/MLDSP-samples-r202/GTDB_small_11_label_reads/Task2_small_11_all.fa"
        folder_path_11 = "/mnt/sda/MLDSP-samples-r202/GTDB_small_11_label_reads/"
        genome_size_11, contig_num_11, file_num_11, len_min_11, len_max_11 = count_train(data_path_11, folder_path_11)
        data_path_1 = "/mnt/sda/MLDSP-samples-r202/GTDB_small_1_label_reads/Task2_small_1_all.fa"
        folder_path_1 = "/mnt/sda/MLDSP-samples-r202/GTDB_small_1_label_reads/"
        genome_size_1, contig_num_1, file_num_1, len_min_1, len_max_1 = count_train(data_path_11, folder_path_11)
        data_path_2 = "/mnt/sda/MLDSP-samples-r202/GTDB_small_2_label_reads/Task2_small_2_all.fa"
        folder_path_2 = "/mnt/sda/MLDSP-samples-r202/GTDB_small_2_label_reads/"
        genome_size_2, contig_num_2, file_num_2, len_min_2, len_max_2 = count_train(data_path_11, folder_path_11)
        genome_size = genome_size_11+genome_size_1+genome_size_2
        contig_num = contig_num_11+contig_num_1+contig_num_2
        file_num = file_num_11 # assume just use one file in the end
        len_min = min(len_min_1, len_min_11, len_min_2)
        len_max = max(len_max_1, len_max_11, len_max_2)
if args.type == "test":
    if args.task == 1 and args.tool == "DeepMicrobes":
        folder_path = "/mnt/sda/DeepMicrobes-data/mag_reads_150bp_1w_provided_split"
        genome_size, contig_num, file_num, len_min, len_max = count_test(folder_path)
    elif args.task == 2 and args.tool == "DeepMicrobes":
        folder_path = "/mnt/sda/DeepMicrobes-data/rumen_mags_reads_Task2_small_all"
        genome_size, contig_num, file_num, len_min, len_max = count_test(folder_path)
    elif args.task == 1 and args.tool == "MT-MAG":
        folder_path = "/mnt/sda/DeepMicrobes-data/labeled_genome-r202/hgr_mags/d__Bacteria"
        genome_size, contig_num, file_num, len_min, len_max = count_test(folder_path)
    elif args.task == 2 and args.tool == "MT-MAG":
        folder_path = "/mnt/sda/MLDSP-samples-r202/rumen_mags/root"
        genome_size, contig_num, file_num, len_min, len_max = count_test(folder_path)


print("file_num is:", file_num)
print("contig_num is:", contig_num)
print("genome_size is:", genome_size)
print("len_min is:", len_min)
print("len_max is:", len_max)


      
