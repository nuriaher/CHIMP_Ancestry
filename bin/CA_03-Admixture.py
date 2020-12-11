#### 26.11.20
import subprocess
import argparse
import os
import re


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-plink_bed', help="filtering step PLINK output", dest="plink_bed", required=True)
parser.add_argument('-out_path', help="output path", dest="out_path", required=True)
parser.add_argument('-t', help="threads", dest="threads")
args = parser.parse_args()

plink_bed=args.plink_bed
out_path=args.out_path

if not args.threads: #default
    t=10
else:
    t=args.threads

## Run

# Number of clusters equal to number of chimpanzee subspecies
k = 4

# Run admixture
plink_base=plink_bed.replace('.bed','')
if not os.path.isfile(plink_base+'.'+str(k)+'.Q'):
    admixtureCmd='cd '+out_path+' && admixture '+plink_bed+' '+str(k)+' -j'+str(t)+''
    subprocess.Popen(admixtureCmd,shell=True).wait()
