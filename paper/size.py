import argparse
from Bio import SeqIO
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default="", type=str, help='path of the data')
parser.add_argument('--one_nested_folder', default=False, action="store_true", help='check only for files within a nested folder')
parser.add_argument('--one_file', default=False, action="store_true", help='check for a specific file')
args = parser.parse_args()
data_path = args.data_path
file_num = 0
contig_num = 0
genome_size = 0

# calculate the size for one folder, folder structure as follows:
# - d__Bacteria
#   - p__Actinobacteriota
#       - fasta
#   - p__Spirochaetota
#       - fasta
#       - fasta
# e.g. python3 paper/size.py --dir /mnt/sda/DeepMicrobes-data/labeled_genome-r202/d__Bacteria --one_nested_folder
if args.one_nested_folder:
    for dir_nested in os.listdir(data_path):
        for fasta_file in os.listdir(os.path.join(data_path, dir_nested)):
            fasta_sequences = SeqIO.parse(open(os.path.join(data_path, dir_nested, fasta_file)),'fasta') 
            for fasta in fasta_sequences:
                _, sequence = fasta.id, str(fasta.seq)
                genome_size += len(sequence)
                contig_num += 1
            file_num += 1
elif args.one_file:
    fasta_sequences = SeqIO.parse(open(data_path), 'fasta')
    for fasta in fasta_sequences:
        _, sequence = fasta.id, str(fasta.seq)
        genome_size += len(sequence)
        contig_num += 1
    file_num += 1

print("file_num is:", file_num)
print("contig_num is:", contig_num)
print("genome_size is:", genome_size)




      
