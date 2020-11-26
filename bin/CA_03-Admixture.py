#### 26.11.20
import subprocess
import argparse
import os
import re


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-filt_bed', help="filtering step PLINK output", dest="filt_bed", required=True)
parser.add_argument('-out_path', help="output path", dest="out_path", required=True)
parser.add_argument('-batch_ID', help="batch_ID", dest="batch_ID", required=True)
args = parser.parse_args()

filt_bed=args.filt_bed
out_path=args.out_path
batch_ID=args.batch_ID


## Run

# Number of clusters equal to number of chimpanzee subspecies
k = 4

# Convert bed file into ped file
plink --bfile filename --recode --tab --out myfavpedfile.ped

BED is the binary of PED:
In short, the PED format will start with six fields in each row:

Family ID ('FID')
Within-family ID ('IID'; cannot be '0')
Within-family ID of father ('0' if father isn't in dataset)
Within-family ID of mother ('0' if mother isn't in dataset)
Sex code ('1' = male, '2' = female, '0' = unknown)
Phenotype value ('1' = control, '2' = case, '-9'/'0'/non-numeric = missing data if case/control)


# Run Admixture on one individual at a time vs Reference Panel
with open(filt_ped) as ped:

#--> maybe create temporal ped files for each individual (PED= REFERENCE PANEL + 1 Individual)

# convert to bed again


    admixtureCmd='admixture '+filt_bed+' '+k+''
    subprocess.Popen(admixtureCmd,shell=True).wait()

    admixture [options] inputFile K
    inputFile: PLINK .bed file
    K: 4
