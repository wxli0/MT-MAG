#!/bin/sh
i=0  
while true  
do  
    echo "iteration ${i}"
    echo "==== git commit ===="
    cd ~/MLDSP
    git add .
    git commit -m "updated outputs"
    git push
    cd ~/BlindKameris-new
    git add .
    git commit -m "updated outputs"
    git push
    echo "==== begin check_missing_time ====" 
    python3 checking_missing_time.py 
    echo "==== begin sleep 5 minutes at $(date)===="
    sleep 300
    i=$((i+1))  
done