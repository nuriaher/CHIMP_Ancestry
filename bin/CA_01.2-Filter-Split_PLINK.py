#### 20.11.20
import subprocess
import argparse
import os
import re


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-in_bed', help="input bed file", dest="in_bed", required=True)
parser.add_argument('-new_IDs', help=".csv file with new Family and Within-family IDs", dest="new_IDs", required=True)
parser.add_argument('-out_base', help="output path+base", dest="out_base", required=True)
parser.add_argument('-batch_ID', help="batch_ID", dest="batch_ID", required=True)
args = parser.parse_args()

in_bed=args.in_bed
new_IDs=args.new_IDs
out_base=args.out_base
batch_ID=args.batch_ID


## Run

with open(new_IDs,'r') as IDs:
    reference_panel=list()
    to_test=list()

    # Save reference panel IDs and individuals to test's in different lists
    for line in IDs.readlines():
        line = line.split()

        if 'P_t' in line:
            reference_panel.append(str(line[2]+'\t'+line[3]))
        else:
            to_test.append(str(line[2]+'\t'+line[3]))


    for individual in to_test:
        ID=individual.split('\t')[0]

        # Define path to new .bed and .txt files
        individual_bed_base = out_base+'-'+ID
        individual_ID = out_base+'-'+ID+'.txt'

        # Create individual ID.txt file + reference panel
        with open(individual_ID,'w+') as ID_file:
            ID_file.write(individual+'\n'+reference_panel)

        # Generate individual file + reference panel
        keepCmd='plink1 --bfile '+in_bed+' --keep '+individual_ID+' --make-bed --out '+individual_bed_base+''
        subprocess.Popen(keepCmd).wait()


        #####################
        ## PLINK filtering of individual bed
        #####################

        # remove sex non-somatic chromosomes and Donald (hybrid chimp, out of RefPanel)
        file = os.path.dirname(sys.argv[0])
        curr_dir = os.path.abspath(file)
        donald_path=str(curr_dir+'/../data/donald_rm.txt')
        plink2Cmd='plink --file '+individual_bed_base+' --not-chr X,Y --remove '+donald_path+' --recode --out '+individual_bed_base+'_somatic_rmDon'
        subprocess.Popen(plink2Cmd,shell=True).wait()

        # minor allele freq 0.05 and missing data
        plink3Cmd='plink --file '+individual_bed_base+'_somatic_rmDon --maf 0.05 --geno 0 --recode --out '+individual_bed_base+'_maf05_geno0'
        subprocess.Popen(plink3Cmd,shell=True).wait()

        # LD pruning
        plink4Cmd='plink --file '+individual_bed_base+'_maf05_geno0 --indep-pairwise 50 5 0.5'
        subprocess.Popen(plink4Cmd,shell=True).wait()

        plink5Cmd='plink --file '+individual_bed_base+'_maf05_geno0 --extract plink.prune.in --make-bed --out '+individual_bed_base+'_plink.pruned'
        subprocess.Popen(plink5Cmd,shell=True).wait()