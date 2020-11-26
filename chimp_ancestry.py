#Núria Hermosilla-Albala
#20.11.20
import argparse
import subprocess
import os

##########################################################
############# CHIMP Ancestry Pipeline EEP ################
##########################################################

#a = system("echo This_is_the_output", intern = TRUE)

# Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-input', help="batchID, vcf file path, Family and Within-family IDs file path", dest="input", required=True)
parser.add_argument('-out_path', help="output path", dest="out_path", required=True)
args = parser.parse_args()

input=args.input
out_path=args.out_path


# Get current path to find bin scripts
current_dir=os.getcwd()

# Process input
batch_ID=list()
VCF_path=list()
ID_file=list()

with open(input,'r') as input_data:
    for line in input_data:
        line.split(',')

        if not(len(line) == 3):
            print("Input file error.\nFormat reminder:\n\tbatch_ID,VCF_path,ID_file_path")

        if len(line) == 3:
            batch_ID.append(line[0])
            VCF_path.append(line[1])
            ID_file.append(line[2])


## Run

for i in range(len(bach_ID)):

    ######
    ### 1 - VCF from NGS variant calling Filtering
    ###
    out_path_filtering=out_path+'/CA_01-Filtering'
    output_filtering=out_path_filtering+'/'+batch_ID[i]+'-pruned.bed'

    filteringCmd='python '+current_dir+'/bin/CA_01-Filtering.py -in_VCF '+VCF_path[i]+' -in_IDs '+ID_file[i]+' -batch_ID '+batch_ID[i]+' -out_path '+out_path_filtering+''
    subprocess.Popen(filteringCmd,shell=True).wait()


    ######
    ### 2 - PCA - Over all filtered data (Ref Panel.coloured , Unkown ancestries.grey)
    ###
    out_path_pca=out_path+'/CA_02-PCA'

    pcaCmd='python '+current_dir+'/bin/CA_02-PCA.py -filt_bed '+output_filtering+' -out_path '+out_path_pca+' -batch_ID '+batchID[i]+''
    subprocess.Popen(pcaCmd,shell=True).wait()


    ######
    ### 3 - ADMIXTURE - Reference Panel x 1 Query Individual (avoid relatedness bias)
    ###

    out_path_admixture=out_path+'CA_03-Admixture'

    admixtureCmd='python '+current_dir+'/bin/CA_03-Admixture.py -filt_bed '+output_filtering+' -out_path '+out_path_admixture+' -batch_ID '+batchID[i]+''
    subprocess.Popen(admixtureCmd,shell=True).wait()

    
    ######
    ### 4 - evalADMIX - Evaluate ADMIXTURE Output for Reference Panel x 1 Query Individual
    ###



    ######
    ### 5 - NGSRelate2 - Relatedness: 1 Query Individual x ADMIXTURE estimated ancestral population
    ###



    ######
    ### 6 - NGSRelate2 - Inbreeding : 1 Query Individual
    ###



    ######
    ### *** 7 *** - Estimate genomic diversity 1 Query Individual
    ###
