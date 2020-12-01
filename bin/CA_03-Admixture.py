#### 26.11.20
import subprocess
import argparse
import os
import re


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-plink_ped', help="filtering step PLINK output", dest="plink_ped", required=True)
parser.add_argument('-out_path', help="output path", dest="out_path", required=True)
parser.add_argument('-t', help="threads", dest="threads")
args = parser.parse_args()

plink_ped=args.plink_ped
out_path=args.out_path

if not args.threads: #default
    t=10
else:
    t=args.threads

## Run

# Number of clusters equal to number of chimpanzee subspecies
k = 4

# Run admixture
admixtureCmd='admixture '+plink_ped+' '+k+' -j'+t+'
subprocess.Popen(admixtureCmd,shell=True).wait()


######## MOVE OUTPUTS TO ADMIXTURE PATH ########## how are output files called?
admix_output_base= '*'


#mvCmd='mv '+OUTPUTS+' '+out_path+''
#subprocess.Popen(mvCmd,shell=True).wait()
