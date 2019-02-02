#!/bin/bash
echo "Password: "
read -s PASSWORD
while true
do
    python3 update_sidebar.py $PASSWORD
done
