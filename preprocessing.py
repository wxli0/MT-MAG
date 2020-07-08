# Sample file for formatting data.
# Our metadata is in the file 'metadata_lanl_whole.json'
# Our sequences are in 'lanl_whole'

# Dependencies.

import json
import pickle
import os
from Bio import SeqIO
import random

# Read the metadata file.

with open('data/metadata_lanl_whole.json','rb') as f:
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


for filename in os.listdir('data/lanl_whole'):

    ID = filename.split('.')[0]

    # Read the file:
    filename = os.path.join('data/lanl_whole', filename)
    fasta_files = SeqIO.parse(filename, "fasta")
    for file in fasta_files:
        seq = str(file.seq)
        seq = seq.replace('-','').upper()

    if len(seq) > min_length and len(seq) < max_lenght:
        # Get the label from the hash table:
        label = d[ID]
        # Add the sequence to the dataset:
        data.append((label, seq))

print(len(data))
#print a random sample:
index = random.randint(0,len(data))
print(data[index])

# Save the dataset.

filename = 'data.p'
with open(filename, 'wb') as f:
    pickle.dump(data, f)
