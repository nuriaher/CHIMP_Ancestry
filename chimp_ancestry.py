#Núria Hermosilla-Albala
#20.11.20
import argparse
import subprocess
import glob
import os

##########################################################
############# CHIMP Ancestry Pipeline EEP ################
##########################################################

#a = system("echo This_is_the_output", intern = TRUE)

# Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-input', help="batchID, vcf file path, Family and Within-family IDs file path", dest="pca_plot", action='store_true')
parser.add_argument('--pca_plot', help="Wants to get a .pdf PCA Plot", dest="input", required=True)
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

    #####################    #####################
    ### 1 - VCF from NGS variant calling Filtering
    #####################    #####################
    out_path_filtering=out_path+'/CA_01-Filtering'


        ## 1.1 - VCF filtering and Renaming
    output_11=out_path+'/'+batch_ID+'-in_Plink_reformat' ####### ####### ####### ####### ####### ####### #######  ADD EXTENSION WHEN RUN
    new_IDs=out_path+'/'+batch_ID[i]+'-new_IDs.txt'

    filtering1Cmd='python '+current_dir+'/bin/CA_01.1-Filter-VCF_Rename.py -in_VCF '+VCF_path[i]+' -in_IDs '+ID_file[i]+' -batch_ID '+batch_ID[i]+' -out_path '+out_path_filtering+''
    subprocess.Popen(filtering1Cmd,shell=True).wait()


        ## 1.2 - Split into 1 individual + Reference panel .bed files + PLINK filtering

    output_12_base=out_path_filtering+'/'+batch_ID[i]

    filtering2Cmd='python '+current_dir+'/bin/CA_01.2-Filter-Split_PLINK.py -in_bed '+output_11+' -new_IDs '+new_IDs+' -batch_ID '+batch_ID[i]+' -out_base '+output_12_base+''
    subprocess.Popen(filtering2Cmd,shell=True).wait()



    #####################    #####################    #####################    #####################
    ######################   Rest of pipeline for individual bed files        ######################
    #####################    #####################    #####################    #####################
            ## 1.3 - Retrieve individual files - keep pipeline

    # Get full paths of all individual .bed files
    bed_individuals=glob.glob(out_path_filtering+'/'+batch_ID[i]+'*')
    for bed in bed_individuals:

        individual_ID=os.path.basename(bed)
        individual_ID=individual_ID.replace(batch_ID[i]+'-pruned','')
        individual_ID=individual_ID.replace('.bed','')



        #####################    #####################
        ### 2 - PCA - Over individual filtered data (Ref Panel.coloured , Unkown ancestry.grey)
        #####################    #####################

        if args.pca_plot:
            pcaCmd='python '+current_dir+'/bin/CA_02-PCA.py -filt_bed '+bed+' -out_path '+out_path+' -ind_ID '+individual_ID+' -batch_ID '+batch_ID[i]+' --pca_plot'
            subprocess.Popen(pcaCmd,shell=True).wait()
        else:
            pcaCmd='python '+current_dir+'/bin/CA_02-PCA.py -filt_bed '+bed+' -out_path '+out_path+' -ind_ID '+individual_ID+' -batch_ID '+batch_ID[i]+''
            subprocess.Popen(pcaCmd,shell=True).wait()



        #####################    #####################
        ### 3 - ADMIXTURE - Reference Panel x 1 Query Individual (avoid relatedness bias)
        #####################    #####################

        admixtureCmd='python '+current_dir+'/bin/CA_03-Admixture.py -filt_bed '+bed+''
        subprocess.Popen(admixtureCmd,shell=True).wait()


        #####################    #####################
        ### 4 - evalADMIX - Evaluate ADMIXTURE Output for Reference Panel x 1 Query Individual
        #####################    #####################



        #####################    #####################
        ### 5 - NGSRelate2 - Relatedness: 1 Query Individual x ADMIXTURE estimated ancestral population
        #####################    #####################



        #####################    #####################
        ### 6 - NGSRelate2 - Inbreeding : 1 Query Individual
        #####################    #####################



        ######
        ### *** 7 *** - Estimate genomic diversity 1 Query Individual
        ###
