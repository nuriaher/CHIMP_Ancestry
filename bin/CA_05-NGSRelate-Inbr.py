
 #-bed_base '+bed_base+' -ancestral_pp '+ancestry+' -individual_ID '+individual_ID+' -out_path'

#### 27.11.20
import subprocess
import argparse
import sys
import os


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-in_bed', help="filtering step PLINK output", dest="in_bed", required=True)
parser.add_argument('-ancestral_pp', help="ancestral population estimated by ADMIXTURE", dest="ancestral_pp", required=True)
parser.add_argument('-ind_ID', help="individual ID", dest="ind_ID", required=True)
parser.add_argument('-t', help="threads", dest="threads")
parser.add_argument('-out_path', help="output path", dest="out_path", required=True)
args = parser.parse_args()

in_bed=args.in_bed
ancestral_pp=args.ancestral_pp
ind_ID=args.ind_ID
out_path=args.out_path


# Only for non-hybrid individuals

# Reformat individual_ID file - keep only Individual + RP in ancestral_pp

# PLINK keep command, subtract from bed the selected individuals in new_individual_ID

# Convert reformatted bed to vcf (.gz)



# Run NgsRelate
output=out_path+"-"+individual_ID+'.res' ## .res Probably not necessary

if args.threads:
    ngsCmd='ngsRelate  -h '+my_reformatted.VCF.gz+' -O '+output+' -p '+str(args.threads)+''
    subprocess.Popen(ngsCmd,shell=True).wait()

else: # default threads 4
    ngsCmd='ngsRelate  -h '+my_reformatted.VCF.gz+' -O '+output+''
    subprocess.Popen(ngsCmd,shell=True).wait()
