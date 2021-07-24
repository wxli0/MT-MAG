import os

GTDB_dir = "/mnt/sda/MLDSP-samples-r202/"
for file in os.listdir(GTDB_dir):
    if file == "root" or file.startswith("d__") or file.startswith("p__") or file.startswith("c__") or \
        file.startswith("o__") or file.startswith("f__") or file.startswith("g__"):
        children = os.listdir(GTDB_dir+file)
        if len(children) == 1:
            print(file)