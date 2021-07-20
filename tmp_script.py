import os
import sys
import subprocess
import time

classes = ["g__Absicoccus",
"g__CADAUA01",
"g__RUG033",
"g__UBA9722",
"f__Bacillaceae",
"g__CAIFEU01",
"g__RUG721"]

for c in classes:
    os.system('screen -dm bash -c "cd ~/MLDSP; bash phase_test.sh '+c + '"')
    print('enter screen -dm bash -c "cd ~/MLDSP; bash phase_test.sh '+c + '"')
