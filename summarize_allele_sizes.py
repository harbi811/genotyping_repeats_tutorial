#!/usr/bin/env python3

import sys

import cyvcf2
import numpy as np
import pandas as pd

vcf = sys.argv[1]

### Load sample metadata ####
df = pd.read_csv("str_resources/all_metadata.csv")
samples = df[["SampleID","Population","Superpopulation"]]

def GetPopOrder(spop):
    spops = ["Africa","Europe","America","South Asia","East Asia"]
    return "%s_%s"%(spops.index(spop), spop)

samples["Superpopulation"] = samples["Superpopulation"].apply(GetPopOrder)

############# Preprocess VCF ##########

# Load VCF
reader = cyvcf2.VCF(vcf)
vcf_sample_list = reader.samples

# Keep track of allele sizes for each sample
asize_other = {}
asize_hom = {}
for s in vcf_sample_list:
    asize_other[s] = {}
    asize_hom[s] = {}

numloc = 0

sys.stderr.write("Reading records\n")

for v in reader:
    if v.FILTER is not None: continue
    is_hom = (v.INFO["PERIOD"]==1)
    diffs = [0] + [int((len(v.ALT[j])-len(v.REF))/v.INFO["PERIOD"]) for j in range(len(v.ALT))]
    for i in range(len(vcf_sample_list)):
        s = vcf_sample_list[i]
        gt = v.genotypes[i]
        if len(gt) != 3: continue # missing
        for al in gt[0:2]:
            diff = diffs[al]
            if is_hom:
                asize_hom[s][diff] = asize_hom[s].get(diff, 0) + 1
            else:
                asize_other[s][diff] = asize_other[s].get(diff, 0) + 1
    numloc += 1
#    if numloc > 100: break #  for debugging. remove

###### Output #########
for s in vcf_sample_list:
    sys.stderr.write(s+"\n")
    pop = samples[samples["SampleID"]==s]["Population"].values[0]
    spop = samples[samples["SampleID"]==s]["Superpopulation"].values[0]
    counts_other = []
    counts_hom = []
    for diff in range(-11, 12): # 1-10, then 11 is 11+
        if diff == -11:
            ct_other = np.sum([asize_other[s][d] for d in asize_other[s].keys() if d<=-11])
            ct_hom = np.sum([asize_hom[s][d] for d in asize_hom[s].keys() if d<=-11])
        elif diff == 11:
            ct_other = np.sum([asize_other[s][d] for d in asize_other[s].keys() if d>=11])
            ct_hom = np.sum([asize_hom[s][d] for d in asize_hom[s].keys() if d>=11])
        else:
            ct_other = asize_other[s].get(diff, 0)
            ct_hom = asize_hom[s].get(diff, 0)
        counts_other.append(ct_other)
        counts_hom.append(ct_hom)
    sys.stdout.write("\t".join([s, spop, pop, "other"]+[str(item) for item in counts_other])+"\n")
    sys.stdout.write("\t".join([s, spop, pop, "hom"]+[str(item) for item in counts_hom])+"\n")
