"""
Configuration file for global parameters
"""

import os
from os.path import expanduser
import os
import platform
import sys



home = expanduser("~")
base_path = os.path.join(home, "Desktop/project.nosync/")
if platform.platform()[:5] == 'Linux':
    base_path = home

MLDSP_path = os.path.join(base_path, "MLDSP")
DM_path = os.path.join(base_path, "DeepMicrobes")
MT_MAG_path = os.path.join(base_path, "MT-MAG")

GTDB_train_path = '/mnt/sda/MLDSP-samples-r202'

sys.path.append(MT_MAG_path))