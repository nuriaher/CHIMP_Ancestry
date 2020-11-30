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


# reformat file name in_IDs to new_IDs
    # Generate newIDs.csv with new names for every batch_ID, see example
tmp_new_IDs=out_path+'/'+batch_ID+'-tmp_new_IDs.txt'
new_IDs=out_path+'/'+batch_ID+'-new_IDs.txt'

with open(in_IDs,'r+') as input_IDs, open(tmp_new_IDs,'w+') as reformatted_IDs:

    for line in input_IDs.readlines():

        if len(line.split(' ')) == 4: # Names have already been reformated
            mvCmd='cp '+in_IDs+' '+new_IDs+''
            subprocess.Popen(mvCmd,shell=True).wait()
            pass

        if not len(line.split(' ')) == 4: # Reformat IDs

            if '.variant' in line:
                line = re.sub('\.variant[0-9]*','',line)

            if 'Pan_troglodytes' in line:
                line = re.sub('Pan_troglodytes','P_t',line)

            if not (line.startswith('Pan')):
                if 'chimp' in line:
                    line = re.sub('chimp','ZOOChimp_',line)
                else:
                    line = 'ZOOChimp_'+line

            reformatted_IDs.write(line)


            reformatfinalCmd='paste '+in_IDs+' '+tmp_new_IDs+' -d '"\t"' > '+new_IDs+' && rm '+tmp_new_IDs+''
            subprocess.Popen(reformatfinalCmd,shell=True).wait()


# update names (shorten names with subspecies abbreviated prefix)
plink1Cmd='plink --file '+out_path+'/'+batch_ID+'-in_Plink --update-ids '+out_path+'/'+batch_ID+'-new_IDs.txt --recode --out '+out_path+'/'+batch_ID+'-in_Plink_reformat'
subprocess.Popen(plink1Cmd,shell=True).wait()
