# coding=utf-8

#Núria Hermosilla-Albala
#2020-2021
# University of Copenhagen

import argparse
import subprocess
import glob
import os

##########################################################
############# CHIMP Ancestry Pipeline EEP ################
##########################################################

# Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
    # Required arguments
parser.add_argument('-input', help="batchID, vcf file path, Family and Within-family IDs file path", dest="input", required=True)
parser.add_argument('-out_path', help="output path", dest="out_path", required=True)
    # Optional arguments
parser.add_argument('--admx_terminate', help="termination criterion for EM algoritm", dest="termination")
parser.add_argument('--pca_plot', help="wants to get a .pdf PCA Plot", dest="pca_plot", action='store_true')
parser.add_argument('--admx_plot', help="wants to get a .pdf ADMIXTURE Plot", dest="admx_plot", action='store_true')
parser.add_argument('--evalAdmix_plot', help="wants to get a .pdf evalADMIX Plot", dest="evalAdmix_plot", action='store_true')
parser.add_argument('--t_admixture', help="admixture number of threads, default 10", dest="t_admixture")
parser.add_argument('--t_evaladmix', help="evaladmix number of threads, default 1", dest="t_evaladmix")
parser.add_argument('--t_ngsrelate', help="ngsrelate number of threads, default 4", dest="t_ngsrelate")
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
        line = line.strip()

        if not line or line.startswith('#'): #line is blank or starts with #
            continue

        line = line.split(' ')

        if not(len(line) == 3):
            print("Input file error.\nFormat reminder:\n\tbatch_ID VCF_path ID_file_path")

        if len(line) == 3:
            batch_ID.append(line[0])
            VCF_path.append(line[1])
            ID_file.append(line[2])

## Run

for i in range(len(batch_ID)):

    #####################    #####################
    ### 1 - VCF from NGS variant calling Filtering
    #####################    #####################
    out_path_filtering=out_path+'/CA_01-Filtering/'+batch_ID[i]
    if not os.path.exists(out_path_filtering):
        os.mkdir(out_path_filtering)


        ## 1.1 - VCF filtering and Renaming
    output_11=out_path_filtering+'/'+batch_ID[i]+'-in_Plink_reformat'
    new_IDs=out_path_filtering+'/'+batch_ID[i]+'-new_IDs.txt'

    filtering1Cmd='python '+current_dir+'/CHIMP_Ancestry/bin/CA_01.1-Filter-VCF_Rename.py -in_VCF '+VCF_path[i]+' -in_IDs '+ID_file[i]+' -batch_ID '+batch_ID[i]+' -out_path '+out_path_filtering+''
    subprocess.Popen(filtering1Cmd,shell=True).wait()


        ## 1.2 - Split into 1 individual + Reference panel .bed files + PLINK filtering

    output_12_base=out_path_filtering+'/'+batch_ID[i]+'_indv'
    if not os.path.exists(output_12_base):
        os.mkdir(output_12_base)

    filtering2Cmd='python '+current_dir+'/CHIMP_Ancestry/bin/CA_01.2-Filter-Split_PLINK.py -in_plink '+output_11+' -new_IDs '+new_IDs+' -batch_ID '+batch_ID[i]+' -out_base '+output_12_base+''
    subprocess.Popen(filtering2Cmd,shell=True).wait()



    #####################    #####################    #####################    #####################
    ######################   Rest of pipeline for individual bed files        ######################
    #####################    #####################    #####################    #####################


            ## 1.3 - Retrieve individual files - keep pipeline

    # Get full paths of all individual .bed files
    files_individuals=glob.glob(output_12_base+'/*.pruned.bed')
    for file in files_individuals:
        individual_ID=os.path.basename(file)
        individual_ID=individual_ID.replace('_plink.pruned.bed','') # indv ID

        plink_base=file.replace('.bed','') # full path


        #####################    #####################
        ### 2 - PCA - Over individual filtered data (Ref Panel.coloured , Unkown ancestry.grey)
        #####################    #####################
        main_path_pca=out_path+'/CA_02-PCA'
        out_path_pca = main_path_pca+'/'+batch_ID[i]


        if not os.path.exists(main_path_pca):
            os.mkdir(main_path_pca)

        if not os.path.exists(out_path_pca):
            os.mkdir(out_path_pca)

        if args.pca_plot:
            pcaCmd='python '+current_dir+'/CHIMP_Ancestry/bin/CA_02-PCA.py -plink_base '+plink_base+' -out_path '+out_path_pca+' -ind_ID '+individual_ID+' -batch_ID '+batch_ID[i]+' --pca_plot'
            subprocess.Popen(pcaCmd,shell=True).wait()

        else:
            pcaCmd='python '+current_dir+'/CHIMP_Ancestry/bin/CA_02-PCA.py -plink_base '+plink_base+' -out_path '+out_path_pca+' -ind_ID '+individual_ID+' -batch_ID '+batch_ID[i]+''
            subprocess.Popen(pcaCmd,shell=True).wait()


        #####################    #####################
        ### 3 - ADMIXTURE - Reference Panel x 1 Query Individual (avoid relatedness bias)
        #####################    #####################
        main_path_admx=out_path+'/CA_03-Admixture'
        out_path_admx = main_path_admx+'/'+batch_ID[i]

        if not os.path.exists(main_path_admx):
            os.mkdir(main_path_admx)

        if not os.path.exists(out_path_admx):
            os.mkdir(out_path_admx)


        admixtureCmd = 'python '+current_dir+'/CHIMP_Ancestry/bin/CA_03-Admixture.py -plink_bed '+plink_base+'.bed -ind_ID '+individual_ID+' -batch_ID '+batch_ID[i]+' -out_path '+out_path_admx+' '

        if args.t_admixture:
            if args.admx_plot:
                if args.termination:
                    admixtureCmd += '-C '+args.termination+' -t '+args.t_admixture+' --admx_plot'
                else:
                    admixtureCmd += '-t '+args.t_admixture+' --admx_plot'

            else:
                if args.termination:
                    admixtureCmd += '-C '+args.termination+' -t '+args.t_admixture+''
                else:
                    admixtureCmd += '-t '+args.t_admixture+''


        if not args.t_admixture:
            if args.admx_plot:
                if args.termination:
                    admixtureCmd += '-C '+args.termination+' --admx_plot'
                else:
                    admixtureCmd += '-t --admx_plot'

            else:
                if args.termination:
                    admixtureCmd += '-C '+args.termination+''
                else:
                    pass

        subprocess.Popen(admixtureCmd,shell=True).wait()



        #####################    #####################
        ### 4 - evalADMIX - Evaluate ADMIXTURE Output for Reference Panel x 1 Query Individual
        #####################    #####################

        # Define PLINK basename for file
        main_path_evaladmx = out_path+'/CA_04-evalAdmix'
        out_path_evaladmx = main_path_evaladmx+'/'+batch_ID[i]

        if not os.path.exists(main_path_evaladmx):
            os.mkdir(main_path_evaladmx)

        if not os.path.exists(out_path_evaladmx):
            os.mkdir(out_path_evaladmx)

        output_4 = out_path_evaladmx+'/EvalAdmix_'+batch_ID[i]+'-'+individual_ID+'.txt'
        admx_base= out_path_admx+'/'+individual_ID+'_plink.pruned'


        if os.path.exists(main_path_admx):
            if args.t_evaladmix:
                if args.evalAdmix_plot:
                    evaladmixCmd='python '+current_dir+'/CHIMP_Ancestry/bin/CA_04-EvalAdmix.py -plink_base '+plink_base+' -admx_base '+admx_base+' -ind_ID '+individual_ID+' -batch_ID '+batch_ID[i]+' -out_path '+out_path_evaladmx+' -t '+args.t_evaladmix+' --evalAdmix_plot'
                    subprocess.Popen(evaladmixCmd,shell=True).wait()

                else:
                    evaladmixCmd='python '+current_dir+'/CHIMP_Ancestry/bin/CA_04-EvalAdmix.py -plink_base '+plink_base+' -admx_base '+admx_base+' -ind_ID '+individual_ID+' -batch_ID '+batch_ID[i]+' -out_path '+out_path_evaladmx+' -t '+args.t_evaladmix+''
                    subprocess.Popen(evaladmixCmd,shell=True).wait()



            if not args.t_evaladmix:
                if args.evalAdmix_plot:
                    evaladmixCmd='python '+current_dir+'/CHIMP_Ancestry/bin/CA_04-EvalAdmix.py -plink_base '+plink_base+' -admx_base '+admx_base+' -ind_ID '+individual_ID+' -batch_ID '+batch_ID[i]+' -out_path '+out_path_evaladmx+' --evalAdmix_plot'
                    subprocess.Popen(evaladmixCmd,shell=True).wait()

                else:
                    evaladmixCmd='python '+current_dir+'/CHIMP_Ancestry/bin/CA_04-EvalAdmix.py -plink_base '+plink_base+' -admx_base '+admx_base+'  -ind_ID '+individual_ID+' -batch_ID '+batch_ID[i]+' -out_path '+out_path_evaladmx+''
                    subprocess.Popen(evaladmixCmd,shell=True).wait()




        #####################    #####################    #####################    #####################
        #####################   Consider individuals > 99% admix coefficients      #####################
        #####################    #####################    #####################    #####################

        #####################    #####################
        ### 5 - NGSRelate2 - All Query Individuals + RefPanel = ADMIXTURE estimated ancestral population
        #####################    #####################

    ###
    # Define output dirs for NGSRelate2
    main_path_ngsrelate = out_path+'/CA_05-NGSRelate2'
    out_path_ngsrelate = main_path_ngsrelate+'/'+batch_ID[i]

    if not os.path.exists(main_path_ngsrelate):
        os.mkdir(main_path_ngsrelate)

    if not os.path.exists(out_path_ngsrelate):
        os.mkdir(out_path_ngsrelate)

    output_5_base = out_path_ngsrelate+'/'+batch_ID[i]

    if args.t_ngsrelate:
        ngsrelateCmd='python '+current_dir+'/CHIMP_Ancestry/bin/CA_05-NGSRelate2.py -plink_base '+output_12_base+' -admx_base '+out_path_admx+' -ngsrelate_base '+output_5_base+' -t '+args.t_ngsrelate+''
        subprocess.Popen(ngsrelateCmd,shell=True).wait()

    else:
        ngsrelateCmd='python '+current_dir+'/CHIMP_Ancestry/bin/CA_05-NGSRelate2.py -plink_base '+output_12_base+' -admx_base '+out_path_admx+' -ngsrelate_base '+output_5_base+''
        subprocess.Popen(ngsrelateCmd,shell=True).wait()



        #####################    #####################
        ### 6 - Summary
        #####################    #####################
