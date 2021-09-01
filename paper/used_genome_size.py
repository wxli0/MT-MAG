"""
Count the total genome size for task data_type

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

size = 0
for dir in os.listdir(base_path):
    if dir[1:3] == '__' and dir.endswith(suffix):
        for file in os.listdir(os.path.join(base_path, dir)):
            fasta_sequences = SeqIO.parse(open(os.path.join(base_path, dir, file)),'fasta') 
            for fasta in fasta_sequences:
                _, sequence = fasta.id, str(fasta.seq)
                size += len(sequence)

print("total genome size for", data_type, "is:", size)
