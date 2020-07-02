#!/bin/bash
echo "Password: "
read -s PASSWORD
while true
do
    python3 -u update_sidebar.py $PASSWORD | tee -a output.log
done
