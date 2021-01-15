# coding=utf-8

#### 20.11.20
import subprocess
import argparse
import os
import re


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-in_VCF', help="input vcf file", dest="in_VCF", required=True)
parser.add_argument('-in_IDs', help=".csv file with current Family and Within-family IDs", dest="in_IDs", required=True)
parser.add_argument('-out_path', help="output path", dest="out_path", required=True)
parser.add_argument('-batch_ID', help="batch_ID", dest="batch_ID", required=True)
args = parser.parse_args()

in_VCF=args.in_VCF
in_IDs=args.in_IDs
out_path=args.out_path
batch_ID=args.batch_ID


## Run

if not (os.path.exists(out_path+'/'+batch_ID+'-filtered_VCF.recode.vcf')):
# remove indels, only biallelic, minimum quality 30, minimum depth 4
    vcf1Cmd='vcftools --gzvcf '+in_VCF+' --minDP 4 --minQ 30 --min-alleles 2 --max-alleles 2 --remove-indels --recode --out '+out_path+'/'+batch_ID+'-filtered_VCF'
    subprocess.Popen(vcf1Cmd,shell=True).wait()

if not (os.path.exists(out_path+'/'+batch_ID+'-in_Plink.map')):
# convert to PLINK
    vcf2Cmd='vcftools --vcf '+out_path+'/'+batch_ID+'-filtered_VCF.recode.vcf --plink --out '+out_path+'/'+batch_ID+'-in_Plink'
    subprocess.Popen(vcf2Cmd,shell=True).wait()

new_IDs=out_path+'/'+batch_ID+'-new_IDs.txt'
if not (os.path.exists(new_IDs)):
    # reformat file name in_IDs to new_IDs
        # Generate newIDs.csv with new names for every batch_ID, see example

    with open(in_IDs,'r+') as input_IDs, open(new_IDs,'w+') as reformatted_IDs:

        for line in input_IDs.readlines():

            if not len(line.split('\t')) == 4: # Reformat IDs

                sublines=line.split()
                new_line=''
                n=1
                for subline in sublines:

                    if '.variant' in subline:
                        subline = re.sub('\.variant[0-9]*','',subline)

                    if 'Pan_troglodytes' in subline:
                        subline = re.sub('Pan_troglodytes','Pt',subline)

                    if not (subline.startswith('Pt')):
                        if 'chimp' in subline:
                            subline = re.sub('chimp_','ZOOChimp_',subline)
                        if not ('ZOOChimp_' in subline) or ('ZooChimp_' in subline):
                            subline = 'ZOOChimp_'+subline

                    if n==1:
                        new_line+=subline+'\t'
                        n+=1
                    else:
                        new_line+=subline

                reformatted_IDs.write(line.strip()+'\t'+new_line+'\n')

            if len(line.split(' ')) == 4: # Names have already been reformated
                mvCmd='cp '+in_IDs+' '+new_IDs+''
                subprocess.Popen(mvCmd,shell=True).wait()



if not (os.path.exists(out_path+'/'+batch_ID+'-in_Plink_reformat.map')):
# update names (shorten names with subspecies abbreviated prefix)
    plink1Cmd='plink1.9 --file '+out_path+'/'+batch_ID+'-in_Plink --update-ids '+out_path+'/'+batch_ID+'-new_IDs.txt --make-bed --out '+out_path+'/'+batch_ID+'-in_Plink_reformat'
    subprocess.Popen(plink1Cmd,shell=True).wait()
