
 #-bed_base '+bed_base+' -ancestral_pp '+ancestry+' -ind_ID '+ind_ID+' -out_path'

#### 27.11.20
import subprocess
import argparse
import sys
import os


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-plink_base', help="filtering step individual PLINK output", dest="plink_base", required=True)
parser.add_argument('-admx_base', help="ancestral population estimated by ADMIXTURE", dest="admx_base", required=True)
parser.add_argument('-ind_ID', help="individual ID", dest="ind_ID", required=True)
parser.add_argument('-t', help="threads", dest="threads")
parser.add_argument('-ngsrelate_base', help="ngsrelate_base path", dest="ngsrelate_base", required=True)
args = parser.parse_args()

plink_base=args.plink_base
admx_base=args.admx_base
ind_ID=args.ind_ID
ngsrelate_base=args.ngsrelate_base


output = ngsrelate_base+"-"+ind_ID+'.res' ## batchID/batchID-individualID.res - .res Probably not necessary

if not os.path.isfile(output):

    ##### 1 - Reformat ind_ID file - keep only Individual + RP in ancestral_pp

    # Define required inputs
    k = str(4)
    Q_path = admx_base+'.'+k+'.Q'
    fam_path = plink_base+'.fam'

    # Q file step
    ancestry_index = int()      # Index of the ancestral population column the query individual belongs to
    pop_indexes = list()        # List where to append positions in Q file of all individuals in ancestral pop
    with open(Q_path,'r') as Q_file:
        # Identify ancestral population from first individual
        query_individual = Q_file.readline()
        query_indv_data = query_individual.split(' ')
        for pop in query_indv_data:
            if str(pop).startswith('0.99'): # If ancestral pop continue, if hybrid pass
                ancestry_index = int(query_indv_data.index(pop))
            else:
                pass

        # Retrieve indexes of same-ancestry RefPanel individuals
        Q_data = Q_file.readlines()
        for i in range(len(Q_data)):
            line = Q_data[i]
            if not (i == 0):
                if '0.99' in str(line.split(' ')[ancestry_index]):  # If ancestral pop continue, if hybrid pass
                    pop_indexes.append(i)
                else:
                    pass
            else:
                pop_indexes.append(0) # Append query individual index in Q file for ID retrieval


    # fam file step
    indv_ancestry_reformatted = ngsrelate_base+'-'+ind_ID # Define ancestry files base
    ID_ancestral_pop = indv_ancestry_reformatted+'_IDs.txt'

    with open(fam_path,'r') as fam_file, open(ID_ancestral_pop,'w+') as ancestry_IDs:
        fam_data = fam_file.readlines()
        for index in pop_indexes:
            fam_line = fam_data[index].split(' ')
            ancestry_IDs.write(fam_line[0]+' '+fam_line[1]+'\n') # Generate new file with same-ancestry indvs' IDs




    ##### 2 - PLINK step, Generate .VCF files : (ZOOChimp + Same ancestry RefPanel)

    # from Plink .bed files in CA_01-Filtering/Batch/Batch_indv/Individual.bed + keep IDs new file
    vcfCmd='plink1.9 --bfile '+plink_base+' --keep '+ID_ancestral_pop+' --make-bed --out '+indv_ancestry_reformatted+''
    subprocess.Popen(vcfCmd,shell=True).wait()



    ##### 3 -  Run NgsRelate, only on newly generated VCF files

    if os.path.isfile(indv_ancestry_reformatted+'.bed') and (not os.path.isfile(output)):
        if args.threads:
            ngsCmd='ngsRelate  -P '+indv_ancestry_reformatted+' -O '+output+' -c 1 -p '+str(args.threads)+''
            subprocess.Popen(ngsCmd,shell=True).wait()

        else:   # default threads 4
            ngsCmd='ngsRelate  -P '+indv_ancestry_reformatted+' -c 1 -O '+output+''
            subprocess.Popen(ngsCmd,shell=True).wait()

# If called genotypes are being used, the software requires an additional argument (-c 1).
