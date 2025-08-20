#!/usr/bin/zsh

############################## PIPELINE ###############################
#
#   top output - batch mode
#                 V
#   sed - exclude 1st seven lines (boilerplate)
#                 V
#   awk - select columns for time, comand, cpu and memory
#                 V
#   sort - based on column 2 i.e memory
#                 V
#   head - filter for top fifty lines (i.e top fifty processes by memory)
#
#######################################################################

top -b -n 1 | sed 1,7d | awk '{print $9, $10, $11, $12}' | sort -r -k2 | head -n 50 >top_info.csv

/home/james/Documents/analysis/scriptin/top_viz.py
