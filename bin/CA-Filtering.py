#### 20.11.20
# Define all input and output files relative to argparse current path

import subprocess
import argparse
import os


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-in_VCF', help="input vcf file", dest="in_VCF", required=True)
parser.add_argument('-sample', help="sample", dest="sample", required=True)
args = parser.parse_args()

in_VCF=args.in_VCF
sample=args.sample

# Run

# remove indels, only biallelic, minimum quality 30, minimum depth 4
'vcftools --gzvcf '+in_VCF+' --minDP 4 --minQ 30 --min-alleles 2 --max-alleles 2 --remove-indels --recode --out '+out_path+'/'+sample+'-filtered_VCF.vcf'

# convert to PLINK
'vcftools --vcf '+out_path+'/'+sample+'-filtered_VCF.vcf --plink --out '+out_path+'/'+sample+'-in_Plink'

# reformat file name

Generate newIDs.csv with new names
--update-ids expects input with the following four fields:

Old family ID
Old within-family ID
New family ID
New within-family ID

# update names (shorten names with subspecies abbreviated prefix)
'plink --file '+out_path+'/'+sample+'-in_Plink --update-ids '+out_path+'/'+sample+'-newIDs.csv --recode --out '+out_path+'/'+sample+'-in_Plink_reformat'

# remove sex non-somatic chromosomes and Donald (hybrid chimp, out of RefPanel)
donald_path= (load file or something).txt
'plink --file '+out_path+'/'+sample+'-in_Plink_reformat --not-chr X,Y --remove '+donald_path+' --recode --out '+out_path+'/'+sample+'-in_Plink_somatic_rmDon'

# minor allele freq 0.05 and missing data
'plink --file '+out_path+'/'+sample+'-in_Plink_somatic_rmDon --maf 0.05 --geno 0 --recode --out '+out_path+'/'+sample+'-in_Plink_maf05_geno0'


# LD pruning
'plink --file '+out_path+'/'+sample+'-in_Plink_maf05_geno0 --indep-pairwise 50 5 0.5'

'plink --file '+out_path+'/'+sample+'-in_Plink_maf05_geno0 --extract '+out_path+'/'+sample+'-plink.prune.in --make-bed --out '+out_path+'/'+sample+'-pruned.plink'
