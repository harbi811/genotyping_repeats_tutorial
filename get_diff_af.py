#!/usr/bin/env python3

import sys

import cyvcf2
import numpy as np
import pandas as pd
import trtools.utils.tr_harmonizer

vcf = sys.argv[1]

# Load VCF
reader = cyvcf2.VCF(vcf)

for v in reader:
    if v.FILTER is not None: continue
    trrecord = trtools.utils.tr_harmonizer.HarmonizeRecord(trtools.utils.tr_harmonizer.VcfTypes.hipstr, v)
    afreqs = trrecord.GetAlleleFreqs(uselength=True)
    reflen = trrecord.ref_allele_length
    for a in afreqs:
        if afreqs[a] < 0.001: continue 
        if a == reflen: continue
        sys.stdout.write("\t".join([v.CHROM, str(v.POS), str(v.INFO["PERIOD"]), "%.2f"%(a-reflen), "%.3f"%afreqs[a]])+"\n")