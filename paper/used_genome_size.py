"""
Count the total genome genome_size for task data_type

Command line arguments:

param sys.argv[1]: data_type. Task data type.

"""
from Bio import SeqIO
import json
import os
import sys

data_type = sys.argv[1]
json_input = json.load(open(os.path.join('task_metadata', data_type+".json")))
base_path = json_input['base_path']
suffix = json_input['suffix']

genome_size = 0
contig_count = 0
sample_count = 0
for dir in os.listdir(base_path):
    if dir[1:3] == '__' and dir.endswith(suffix):
        for subdir in os.listdir(os.path.join(base_path, dir)):
            for file in os.listdir(os.path.join(base_path, dir, subdir)):
                fasta_sequences = SeqIO.parse(open(os.path.join(base_path, dir, subdir, file)),'fasta') 
                sample_count += 1
                for fasta in fasta_sequences:
                    _, sequence = fasta.id, str(fasta.seq)
                    genome_size += len(sequence)
                    contig_count += 1

print("base_path", base_path, "genome_size:", genome_size, "sample_count:", sample_count, "contig_count:", contig_count)
