#!/bin/bash
n=0
while [ $n -le 50 ]
do
    python3 upload2ArchiveOrg2.py
    let n++
done