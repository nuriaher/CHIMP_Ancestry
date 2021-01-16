#### 27.11.20
import subprocess
import argparse
import sys
import glob
import os


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-plink_base', help="filtering step individual PLINK output", dest="plink_base", required=True)
parser.add_argument('-admx_base', help="ancestral population estimated by ADMIXTURE", dest="admx_base", required=True)
parser.add_argument('-t', help="threads", dest="threads")
parser.add_argument('-ngsrelate_base', help="ngsrelate_base path", dest="ngsrelate_base", required=True)
args = parser.parse_args()

plink_base=args.plink_base
admx_base=args.admx_base
ngsrelate_base=args.ngsrelate_base


####### 1 - Retrieve same ancestry zoo chimps in batch and ref panel

ancestries = {}
for ancestry in range(0,4):
    ancestries[ancestry] = {}
    ancestries[ancestry]['ref'] = list()
    ancestries[ancestry]['zoo'] = list()

# Get full paths of all individual .bed files
plink_files=glob.glob(plink_base+'/*.pruned.bed')

for file in plink_files:
    ind_ID=os.path.basename(file)

    # Define paths
    ind_ID=ind_ID.replace('_plink.pruned.bed','') # indv ID
    plink_base_indv=file.replace('.bed','') # full path

    fam_path = plink_base_indv+'.fam'
    k = str(4)
    Q_path = admx_base+'/'+ind_ID+'_plink.pruned.'+k+'.Q'

    ## Q file step
    # Define variables
    ancestry_index = int()      # Index of the ancestral population column the query individual belongs to
    ZOOChimp_index = int()      # Index of the Zoo chimp to retrieve ID from fam file
    ref_indexes = list()        # List where to append positions in Q file of RefPanel individuals in SAME ancestral pop as ZOO


    with open(fam_path,'r') as fam_file, open(Q_path,'r') as Q_file:

        fam_data = fam_file.readlines()
        Q_data = Q_file.readlines()

        # Identify ancestral population from first individual + get its index
        ZOOChimp = [i for i in fam_data if ind_ID in i]
        ZOOChimp_ID = ZOOChimp[0].split(' ')[0]         # Get zoochimp ID from fam file
        ZOOChimp_index = fam_data.index(ZOOChimp[0])
        ZOOChimp_data = Q_data[ZOOChimp_index].split(' ')  # Get zoochimp index to find it in Q file

        # Get ancestry population index: 0,1,2 or 3
        for pop in ZOOChimp_data:
            if str(pop).startswith('0.99'): # If high ancestry coefficient continue, if hybrid pass
                ancestry_index = int(ZOOChimp_data.index(pop))  # Get which ancestral population the zoochimp belongs to
                break
            else:
                ancestry_index = None


        # Retrieve indexes of same-ancestry RefPanel individuals
        if (ancestry_index in ancestries.keys()) and (not ancestry_index == None):
            if (ancestries[ancestry_index]['ref']):
                pass    # If ref panel already defined, pass

            else:
                # If the individuals of the reference panel of a given ancestry are not defined yet
                for i in range(len(Q_data)):
                    line = Q_data[i]
                    if not (i == ZOOChimp_index):
                        if '0.99' in str(line.split(' ')[ancestry_index]):  # If ancestral pop continue, if hybrid pass
                            ref_indexes.append(i)
                        else:
                            pass
                    else:
                        pass # If the detected 0.99 is the ZOOChimp's, pass


            ## FAM file step
            # Get the ZOOChimp or the ZOOChimp and RefPanel IDs from indexes

            # Append zoochimp ID
            fam_zoochimp = fam_data[ZOOChimp_index].strip().split(' ')
            ancestries[ancestry_index]['zoo'].append(fam_zoochimp[0]+' '+fam_zoochimp[1])

            # If not defined already = ref_indexes not empty
            if ref_indexes:
                for index in ref_indexes:
                    fam_ref = fam_data[index].strip().split(' ')
                    ancestries[ancestry_index]['ref'].append(fam_ref[0]+' '+fam_ref[1])



#### 2 - Generate output paths and keep files

ancestry_keep_files = list()
subspecies = ['troglodytes', 'schweinfurthii','ellioti','verus']


for pop in range(0,4):
    if ancestries[pop]['zoo']:

        # Define outputs
        plink_base_ancestry = plink_base.replace('_indv','-in_Plink_reformat')

        ancestry_keep_file = ngsrelate_base+'-'+str(pop)+'_keep_ancestry.txt'
        out_plink_base = ngsrelate_base+'-'+str(pop)
        output = ngsrelate_base+'-'+str(pop)+'.res'
        IDs_to_ngsrelate = ngsrelate_base+'-'+str(pop)+'_keep_1c.txt'


        # Write Dictionary IDs to KEEP.txt files
        with open(ancestry_keep_file,'w+') as keep_ancestry:
            for ID in ancestries[pop]['zoo']:
                keep_ancestry.write(ID+'\n')
            for ID in ancestries[pop]['ref']:
                keep_ancestry.write(ID+'\n')


        # from Plink .bed files in CA_01-Filtering/Batch/Batch_indv/Individual.bed + keep IDs new file
        bedCmd='plink1.9 --bfile '+plink_base_ancestry+' --keep '+ancestry_keep_file+' --make-bed --out '+out_plink_base+''
        subprocess.Popen(bedCmd,shell=True).wait()



        ##### 3 -  Run NgsRelate, only on newly generated VCF files

        if os.path.isfile(out_plink_base+'.bed') and (not os.path.isfile(output)):

            if args.threads:
                ngsCmd='cut -f1 -d" " ' +ancestry_keep_file+' > '+IDs_to_ngsrelate+' && ngsRelate  -P '+out_plink_base+' -c 1 -O '+output+' -z '+IDs_to_ngsrelate+' -p '+str(args.threads)+' && rm '+IDs_to_ngsrelate+''
                subprocess.Popen(ngsCmd,shell=True).wait()

            else:   # default threads 4
                ngsCmd='cut -f1 -d" " '+ancestry_keep_file+' > '+IDs_to_ngsrelate+' && ngsRelate  -P '+out_plink_base+' -c 1 -O '+output+' -z '+IDs_to_ngsrelate+' && rm '+IDs_to_ngsrelate+''
                subprocess.Popen(ngsCmd,shell=True).wait()

        if os.path.isfile(output):
            os.remove(fam_path)
            plinks = glob.glob(out_plink_base+'*')
            for plink in plinks:
                os.remove(plink)


    else:
        pass
