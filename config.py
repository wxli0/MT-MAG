"""
Configuration file for global parameters
"""

import os
from os.path import expanduser
import os
import platform



home = expanduser("~")
base_path = os.path.join(home, "Desktop/project.nosync/")
if platform.platform()[:5] == 'Linux':
    base_path = home

MLDSP_path = os.path.join(base_path, "MLDSP")
DM_path = os.path.join(base_path, "DeepMicrobes")
MT_MAG_path = os.path.join(base_path, "MT-MAG")
