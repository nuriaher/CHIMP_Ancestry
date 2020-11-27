#### 26.11.20
import subprocess
import argparse
import os
import re


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-filt_bed', help="filtering step PLINK output", dest="filt_bed", required=True)
args = parser.parse_args()

filt_bed=args.filt_bed

## Run

# Number of clusters equal to number of chimpanzee subspecies
k = 4

# Run admixture
admixtureCmd='admixture '+filt_bed+' '+k+''
subprocess.Popen(admixtureCmd,shell=True).wait()
