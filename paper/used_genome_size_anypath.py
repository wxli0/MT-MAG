import os
import sys
from Bio import SeqIO

base_path = sys.argv[1]
size = 0
for file in os.listdir(base_path):
    # if file.endswith("_1.fa") or file.endswith('_2.fa'):
    fasta_sequences = SeqIO.parse(open(os.path.join(base_path, file)),'fasta') 
    for fasta in fasta_sequences:
        _, sequence = fasta.id, str(fasta.seq)
        size += len(sequence)

print("base_path:", base_path, "size:", size)