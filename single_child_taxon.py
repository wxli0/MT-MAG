import os

GTDB_dir = "/mnt/sda/MLDSP-samples-r202/"

print("======== GTDB ========")
for file in os.listdir(GTDB_dir):
    if file == "root" or file.startswith("d__") or file.startswith("p__") or file.startswith("c__") or \
        file.startswith("o__") or file.startswith("f__"):
        children = os.listdir(GTDB_dir+file)
        if len(children) == 1:
            print(file)

print("======== HGR ========")
HGR_dir = "/mnt/sda/DeepMicrobes-data/labeled_genome-r202/"
for file in os.listdir(GTDB_dir):
    if file.endswith("_split_pruned"):
        children = os.listdir(GTDB_dir+file)
        if len(children) == 1:
            print(file[:-13])