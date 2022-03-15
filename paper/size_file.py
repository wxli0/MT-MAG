"""
Calculates the size of an individual file

:param argv[1]: data_path. Absolute data path of the file
"""

import argparse
from Bio import SeqIO
import os
import sys

genome_size = 0
data_path = sys.argv[1]



fasta_sequences = SeqIO.parse(open(data_path),'fasta') 
for fasta in fasta_sequences:
    _, sequence = fasta.id, str(fasta.seq)
    genome_size += len(sequence)
print("genome size is:", genome_size)