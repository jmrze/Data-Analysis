#!/bin/zsh
#
# script for conversion of a provided DNA strand into its pre-mRNA and reverse complement
#
# user input - DNA sequence
#
echo -n "Enter DNA sequence template (3' -> 5'): "
read sequence
#
# manipulate input to generate new variables
#
dna_c=$(echo "$sequence" | tr ACGT TGCA)
rna=$(echo "$dna_c" | tr T U)
rc=$(echo "$sequence" | tr ACGT TGCA | rev)
# # print template (input), coding, RNA, reverse complement #
echo -e "\tTemplate Strand: 3'-$sequence-5'
\tCoding Strand: 5'-$dna_c-3' 
\tRNA: 5'-$rna-3'
\tReverse Complement: 5'-$rc-3'"
#
