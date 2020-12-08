# Sample file for formatting data.
# Our metadata is in the file 'metadata_lanl_whole.json'
# Our sequences are in 'lanl_whole'

# Dependencies.

import json
import pickle
import os
from Bio import SeqIO
import random
import sys

# Read the metadata file.
input_folder = sys.argv[1]


with open('data/'+input_folder+'.json','rb') as f:
  metadata = json.load(f)

# Create a Hash Table with the ID as keys and the labels as values,

d = {}
for seq in metadata:
  d[seq['id']] = seq['subtype']


# For each fasta FASTA file in our folder, we can search the ID
# in our hash table and add the pair (label, sequence) to our
# dataset. We can remove short or long seequences as well.

data = []
min_length = 0
max_lenght = 1e6


for filename in os.listdir('data/'+input_folder):

    # ID = filename.split('.')[0]
    ID = filename[:-6]

    # Read the file:
    filename = os.path.join('data/'+input_folder, filename)
    fasta_files = SeqIO.parse(filename, "fasta")
    for file in fasta_files:
        seq = str(file.seq)
        seq = seq.replace('-','').upper()

    if len(seq) > min_length and len(seq) < max_lenght:
        # Get the label from the hash table:
        label = d[ID]
        # Add the sequence to the dataset:
        data.append((label, seq, ID))

print(len(data))
#print a random sample:
index = random.randint(0,len(data))
print(data[index])

# Save the dataset.
dest_folder = "p_files/"
filename = dest_folder+input_folder+'.p'
with open(filename, 'wb') as f:
    pickle.dump(data, f)
