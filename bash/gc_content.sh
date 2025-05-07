#!/usr/bin/bash

# DNA input

echo -n -e "Enter DNA sequence: "
read SEQUENCE

# variables - length, GC content and percent
N=${#SEQUENCE}
GC=$(echo "$SEQUENCE" | tr -cd 'GgCc' | wc -c)
PERCENT=$(($GC*100/$N))	

# output

echo -e "Length: $N"
echo -e "GC no: $GC"
#echo -e "Total GC: $TOTAL_GC"
echo -e "GC: $PERCENT%"
