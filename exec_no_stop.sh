#!/bin/sh  
while true  
do  
    echo "==== begin group_pred ===="
    python3 outputs-HGR-r202/group_pred_HGR.py family
    python3 outputs-HGR-r202/group_pred_HGR.py genus
    echo "==== begin checking_missing_exec ====" 
    python3 checking_missing_exec.py True
    echo "==== begin sleep ===="
    sleep 1600  
done