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
    indv_ancestry_reformatted = ngsrelate_base+'-'+ind_ID # Define ancestry files base
    ID_ancestral_pop = indv_ancestry_reformatted+'_IDs.txt'


    # Q file step
    ZOOChimp_index = int()
    ancestry_index = int()      # Index of the ancestral population column the query individual belongs to
    pop_indexes = list()        # List where to append positions in Q file of all individuals in ancestral pop

    with open(fam_path,'r') as fam_file, open(Q_path,'r') as Q_file:

        fam_data = fam_file.readlines()
        Q_data = Q_file.readlines()


        # Identify ancestral population from first individual + get its index
        ZOOChimp = [i for i in fam_data if ind_ID in i]
        ZOOChimp_ID = ZOOChimp[0].split(' ')[0]
        ZOOChimp_index = fam_data.index(ZOOChimp[0])
        ZOOChimp_data = Q_data[ZOOChimp_index].split(' ')
        for pop in ZOOChimp_data:
            if str(pop).startswith('0.99'): # If ancestral pop continue, if hybrid pass
                ancestry_index = int(ZOOChimp_data.index(pop))
                break
            else:
                ancestry_index = False


        if ancestry_index:
            # Retrieve indexes of same-ancestry RefPanel individuals
            for i in range(len(Q_data)):
                line = Q_data[i]
                if not (i == ZOOChimp_index):
                    if '0.99' in str(line.split(' ')[ancestry_index]):  # If ancestral pop continue, if hybrid pass
                        pop_indexes.append(i)
                    else:
                        pass
                else:
                    pop_indexes.append(ZOOChimp_index) # Append query individual index in Q file for ID retrieval

            # fam file step
            with open(ID_ancestral_pop,'w') as chimp_ancestry_IDs:
                for index in pop_indexes:
                    fam_line = fam_data[index].split(' ')
                    if pop_indexes.index(index) == len(pop_indexes):
                        chimp_ancestry_IDs.write(fam_line[0]+' '+fam_line[1]) # Generate new file with same-ancestry indvs' IDs
                    else:
                        chimp_ancestry_IDs.write(fam_line[0]+' '+fam_line[1]+'\n') # Generate new file with same-ancestry indvs' IDs




            ##### 2 - PLINK step, Generate .VCF files : (ZOOChimp + Same ancestry RefPanel)

            # from Plink .bed files in CA_01-Filtering/Batch/Batch_indv/Individual.bed + keep IDs new file
            bedCmd='plink1.9 --bfile '+plink_base+' --keep '+ID_ancestral_pop+' --make-bed --out '+indv_ancestry_reformatted+''
            subprocess.Popen(bedCmd,shell=True).wait()



            ##### 3 -  Run NgsRelate, only on newly generated VCF files

            if os.path.isfile(indv_ancestry_reformatted+'.bed') and (not os.path.isfile(output)):
                if args.threads:
                    ngsCmd='cut -f1 -d" " ' +ID_ancestral_pop+' > '+IDs_to_ngsrelate+' && ngsRelate  -P '+indv_ancestry_reformatted+' -O '+output+' -c 1 -p '+str(args.threads)+' && rm '+IDs_to_ngsrelate+''
                    subprocess.Popen(ngsCmd,shell=True).wait()

                else:   # default threads 4

                    IDs_to_ngsrelate = indv_ancestry_reformatted+'_IDs_1c.txt'
                    ngsCmd='cut -f1 -d" " '+ID_ancestral_pop+' > '+IDs_to_ngsrelate+' && ngsRelate  -P '+indv_ancestry_reformatted+' -c 1 -O '+output+' -z '+IDs_to_ngsrelate+' && rm '+IDs_to_ngsrelate+''
                    subprocess.Popen(ngsCmd,shell=True).wait()

        # If called genotypes are being used, the software requires an additional argument (-c 1).
