#### 20.11.20
import subprocess
import argparse
import os


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-in_VCF', help="input vcf file", dest="in_VCF", required=True)
parser.add_argument('-in_IDs', help=".csv file with current Family and Within-family IDs", dest="in_IDs", required=True)
parser.add_argument('-batch_ID', help="batch_ID", dest="batch_ID", required=True)
args = parser.parse_args()

in_VCF=args.in_VCF
in_IDs=args.in_IDs
batch_ID=args.batch_ID


## Run

# remove indels, only biallelic, minimum quality 30, minimum depth 4
vcf1Cmd='vcftools --gzvcf '+in_VCF+' --minDP 4 --minQ 30 --min-alleles 2 --max-alleles 2 --remove-indels --recode --out '+out_path+'/'+batch_ID+'-filtered_VCF.vcf'
subprocess.Popen(vcf1Cmd,shell=True).wait()

# convert to PLINK
vcf2Cmd='vcftools --vcf '+out_path+'/'+batch_ID+'-filtered_VCF.vcf --plink --out '+out_path+'/'+batch_ID+'-in_Plink'
subprocess.Popen(vcf2Cmd,shell=True).wait()

# reformat file name in_IDs to new_IDs
    # Generate newIDs.csv with new names for every batch_ID, see example
tmp_new_IDs=out_path+'/'+batch_ID+'-tmp_new_IDs.csv'
new_IDs=out_path+'/'+batch_ID+'-new_IDs.csv'

with open(in_IDs,'r+') as input_IDs:
    lines = input_IDs.readlines()

    if len(line.split(' ')) == 4: # Names have already been reformated
        in_IDs = newIDs
        break

    if not (len(line.split(' ')) == 4): # Reformat IDs
        with open(tmp_newIDs,w+) as reformat_IDs:
            reformat_IDs.write(input_IDs)

            if line.find(".variant"):
                reformat1Cmd='cat '+tmp_newIDs+' | grep variant | sed "s/\.variant[0-9]*//" > '+tmp_newIDs+''
                subprocess.Popen(reformat1Cmd,shell=True).wait()

            if line.find("Pan_troglodytes"):
                reformat2Cmd='cat '+tmp_newIDs+' | grep Pan_troglodytes | sed "s/Pan_troglodytes/P_t/" > '+tmp_newIDs+''
                subprocess.Popen(reformat2Cmd,shell=True).wait()

            if line.find("chimp_"):
                reformat3Cmd='cat '+tmp_newIDs+' | grep chimp | sed "s/chimp/ZOOChimp/" > '+tmp_newIDs+''
                subprocess.Popen(reformat3Cmd,shell=True).wait()

            # reformat finished, create final  IDs file
            reformatfinalCmd='paste '+in_IDs+' '+tmp_newIDs+' | column -t > '+newIDs+' && rm '+tmp_newIDs+''
            subprocess.Popen(reformatfinalCmd,shell=True).wait()

# update names (shorten names with subspecies abbreviated prefix)
plink1Cmd='plink --file '+out_path+'/'+batch_ID+'-in_Plink --update-ids '+out_path+'/'+batch_ID+'-new_IDs.csv --recode --out '+out_path+'/'+batch_ID+'-in_Plink_reformat'
subprocess.Popen(plink1Cmd,shell=True).wait()


# remove sex non-somatic chromosomes and Donald (hybrid chimp, out of RefPanel)
file = os.path.dirname(sys.argv[0])
curr_dir = os.path.abspath(file)
donald_path=str(curr_dir+'/../suppl/donald_rm.txt')
plink2Cmd='plink --file '+out_path+'/'+batch_ID+'-in_Plink_reformat --not-chr X,Y --remove '+donald_path+' --recode --out '+out_path+'/'+batch_ID+'-in_Plink_somatic_rmDon'
subprocess.Popen(plink2Cmd,shell=True).wait()

# minor allele freq 0.05 and missing data
plink3Cmd='plink --file '+out_path+'/'+batch_ID+'-in_Plink_somatic_rmDon --maf 0.05 --geno 0 --recode --out '+out_path+'/'+batch_ID+'-in_Plink_maf05_geno0'
subprocess.Popen(plink3Cmd,shell=True).wait()

# LD pruning
plink4Cmd='plink --file '+out_path+'/'+batch_ID+'-in_Plink_maf05_geno0 --indep-pairwise 50 5 0.5'
subprocess.Popen(plink4Cmd,shell=True).wait()

plink5Cmd='plink --file '+out_path+'/'+batch_ID+'-in_Plink_maf05_geno0 --extract '+out_path+'/'+batch_ID+'-plink.prune.in --make-bed --out '+out_path+'/'+batch_ID+'-pruned.plink'
subprocess.Popen(plink5Cmd,shell=True).wait()
