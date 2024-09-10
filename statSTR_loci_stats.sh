#!/bin/bash

CHROM=$1
START=$2

statSTR \
    --vcf output/ensembletr_output/ensembletr_sorted.vcf.gz \
    --vcftype hipstr \
    --afreq --use-length \
    --region chr${CHROM}:${START}-${START} \
    --out downstream/chr${CHROM}.${START}_stats \
    --samples str_resources/africa_ids.csv,str_resources/america_ids.csv,str_resources/europe_ids.csv,str_resources/east_asia_ids.csv,str_resources/south_asia_ids.csv \
    --sample-prefixes africa,america,europe,east_asia,south_asia
