import argparse
from Bio import SeqIO
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--base_path', default="", type=str, help='directories of the fasta files')
parser.add_argument('--onetwofa', default=False, action="store_true", help='check only for files with suffix _1.fa and _2.fa')
parser.add_argument('--one_file', default=False, action="store_true", help='check for a specific file')
args = parser.parse_args()

base_path = args.base_path
genome_size = 0
contig_count = 0
sample_count = 0

if args.one_file:
    fasta_sequences = SeqIO.parse(open(os.path.join(base_path)),'fasta') 
    for fasta in fasta_sequences:
        _, sequence = fasta.id, str(fasta.seq)
        genome_size += len(sequence)
        contig_count += 1
else:
    for file in os.listdir(base_path):
        if args.onetwofa:
            if not (file.endswith("_1.fa") or file.endswith('_2.fa')):
                continue
        fasta_sequences = SeqIO.parse(open(os.path.join(base_path, file)),'fasta') 
        for fasta in fasta_sequences:
            _, sequence = fasta.id, str(fasta.seq)
            genome_size += len(sequence)
            contig_count += 1
        sample_count += 1


print("base_path:", base_path, "genome_size:", genome_size, "sample_count is:", sample_count, "contig_count is:", contig_count)