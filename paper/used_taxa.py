"""
Count the number of used taxa in training datasets

Command line arguments
:param sys.argv[1]: data_type. Task data type
:param sys.argv[2]: rank. Target rank to count used taxa.

"""

import json
import os
import sys

def count_rank(dirs, start, base_path = None):
    """
    Count the number of directories in dirs that start with start

    :param dirs: directories
    :type dirs: List[str]
    :param start: the characters to start with
    :type start: str
    :param base_path: presents if start captures the pattern of previous rank. Used \
        for ranks[-1]. Default None
    :type base_path: str
    """
    count = 0
    for dir in dirs:
        if dir.startswith(start):
            if base_path is None:
                count += 1
            else:
                dir_path = os.path.join(base_path, dir)
                count += len(os.listdir(dir_path))
    return count


data_type = sys.argv[1]
rank = sys.argv[2]

json_data = json.load(open(os.path.join('task_metadata', data_type+".json")))
base_path = json_data['base_path']
ranks = json_data['ranks']

rank_count = 0
dirs = os.listdir(os.path.join(base_path))
if rank != ranks[-1]:
    rank_count = count_rank(dirs, rank[0]+'__')
else:
    rank_count = count_rank(dirs, ranks[-2][0]+'__', base_path)

print(rank+":", rank_count)


        



