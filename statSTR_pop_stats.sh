#!/bin/bash

# get genotype statistics using statSTR

# populations=("africa" "europe" "east_asia" "south_asia" "america")

declare -a populations=( "$@" )

for population in "${populations[@]}"; do

    statSTR \
        --vcf output/ensembletr_output/ensembletr_sorted.vcf.gz \
        --vcftype hipstr \
        --thresh --afreq --use-length \
        --out downstream/"${population}"_stats \
        --samples str_resources/"${population}"_ids.csv

done

# Get list of STR, period, diff, AF
# python get_diff_af.py output/ensembletr_output/ensembletr_sorted.vcf.gz > downstream/diff_afreqs.tab


