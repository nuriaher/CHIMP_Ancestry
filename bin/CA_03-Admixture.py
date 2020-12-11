#### 26.11.20
import subprocess
import argparse
import sys
import os
import re


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-plink_bed', help="filtering step PLINK output", dest="plink_bed", required=True)
parser.add_argument('--admx_plot', help="Wants to get a .pdf ADMIXTURE Plot", dest="admx_plot", action='store_true')
parser.add_argument('-batch_ID', help="batch_ID", dest="batch_ID", required=True)
parser.add_argument('-ind_ID', help="individual ID", dest="ind_ID", required=True)
parser.add_argument('-out_path', help="output path", dest="out_path", required=True)
parser.add_argument('-t', help="threads", dest="threads")
args = parser.parse_args()

plink_bed=args.plink_bed
ind_ID=args.ind_ID
batch_ID=args.batch_ID
out_path=args.out_path

if not args.threads: #default
    t=10
else:
    t=args.threads

## Run

# Number of clusters equal to number of chimpanzee subspecies
k = 4

# Run admixture
plink_base=plink_bed.replace('.bed','')
Q_file=out_path+'/'+ind_ID+'_plink.pruned.'+str(k)+'.Q'

if not os.path.isfile(Q_file):
    admixtureCmd='cd '+out_path+' && admixture '+plink_bed+' '+str(k)+' -j'+str(t)+''
    subprocess.Popen(admixtureCmd,shell=True).wait()


# Plot
if args.admx_plot:
    if not os.path.exists(out_path+'/ADMIXTURE-'+batch_ID+'-'+ind_ID+'.pdf'):
            # Generate ADMIXTURE plot
        fam_file=plink_base+'.fam'

        # Get current directory
        file = os.path.dirname(sys.argv[0])
        curr_dir = os.path.abspath(file)

        admxplotCmd='Rscript '+curr_dir+'/CA_03.1-Admixture_Plot.R --Q_admx '+Q_file+' --fam_file '+fam_file+' -ind_ID '+ind_ID+' -batch_ID '+batch_ID+' -out_path '+out_path+''
        subprocess.Popen(admxplotCmd,shell=True).wait()


    else:
        pass
