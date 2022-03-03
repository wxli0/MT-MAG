import argparse
from Bio import SeqIO
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--task',  default = 0, type=int, help='task 1 or task 2')
parser.add_argument('--tool', default="", type=str, help='DeepMicrobes or MT-MAG')
args = parser.parse_args()
task = args.task
tool = args.tool
file_num = 0
contig_num = 0
genome_size = 0


if args.task == 1 and args.tool  == "MT-MAG":
    # command python3 paper/size.py --task=1 --tool=MT-MAG
    data_path = "/mnt/sda/DeepMicrobes-data/labeled_genome-r202/d__Bacteria"
    for dir_nested in os.listdir(data_path):
        for fasta_file in os.listdir(os.path.join(data_path, dir_nested)):
            fasta_sequences = SeqIO.parse(open(os.path.join(data_path, dir_nested, fasta_file)),'fasta') 
            for fasta in fasta_sequences:
                _, sequence = fasta.id, str(fasta.seq)
                genome_size += len(sequence)
                contig_num += 1
            file_num += 1
elif args.task == 1 and args.tool == "DeepMicrobes":
    # command: python3 paper/size.py --task=1 --tool=DeepMicrobes
    data_path = "/mnt/sda/DeepMicrobes-data/HGR_species_label_reads/HGR_species_label_reads_train.fa"
    folder_path = "/mnt/sda/DeepMicrobes-data/HGR_species_label_reads"
    fasta_sequences = SeqIO.parse(open(data_path), 'fasta')
    for fasta in fasta_sequences:
        _, sequence = fasta.id, str(fasta.seq)
        genome_size += len(sequence)
        contig_num += 1
    for fasta_file in os.listdir(folder_path):
        if fasta_file.endswith("_trimmed.fa"):
            file_num += 1
    file_num -= 1 # to ignore labeled_genome_train_species_reads_trimmed.fa
elif args.task == 2 and args.tool == "MT-MAG":
    data_path = "/mnt/sda/MLDSP-samples-r202"
    for dir_nested1 in os.listdir(data_path):
        for dir_nested2 in os.listdir(data_path, dir_nested1):
            for fasta_file in os.listdir(os.path.join(data_path, dir_nested1, dir_nested2)):
                fasta_sequences = SeqIO.parse(open(os.path.join(data_path, dir_nested1, dir_nested2, fasta_file)),'fasta') 
                for fasta in fasta_sequences:
                    _, sequence = fasta.id, str(fasta.seq)
                    genome_size += len(sequence)
                    contig_num += 1
                file_num += 1  
#elif args.task == 2 and args.tool == "DeepMicrobes":

print("file_num is:", file_num)
print("contig_num is:", contig_num)
print("genome_size is:", genome_size)




      
