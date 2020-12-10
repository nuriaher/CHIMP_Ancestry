#### 26.11.20
import subprocess
import argparse
import sys
import os


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-plink_base', help="filtering step PLINK output", dest="plink_base", required=True)
parser.add_argument('--pca_plot', help="Wants to get a .pdf PCA Plot", action='store_true')
parser.add_argument('-out_path', help="output path", dest="out_path", required=True)
parser.add_argument('-batch_ID', help="batch_ID", dest="batch_ID", required=True)
parser.add_argument('-ind_ID', help="individual ID", dest="ind_ID", required=True)
args = parser.parse_args()

plink_base=args.plink_base
out_path=args.out_path
ind_ID=args.ind_ID
batch_ID=args.batch_ID



## Run

    # Generate .eigenvalues .eigenvectors files
out_base=out_path+'/'+ind_ID

if not os.path.isfile(out_base+'.eigenval'):
    pcaCmd='plink1.9 --bfile '+plink_base+' --pca 10 --out '+out_base+''
    subprocess.Popen(pcaCmd,shell=True).wait()

else:
    pass


if args.pca_plot:
    print('PCA')
        # Generate PCA plot
    out_evalues=''+out_base+'.eigenval'
    out_evectors=''+out_base+'.eigenvec'

    # Get current directory
    file = os.path.dirname(sys.argv[0])
    curr_dir = os.path.abspath(file)

    pcaplotCmd='Rscript '+curr_dir+'/CA_02.1-PCA_Plot.R --eval '+out_evalues+' --evec '+out_evectors+' -ind_ID '+ind_ID+' -batch_ID '+batch_ID+' -out_path '+out_path+''
    subprocess.Popen(pcaplotCmd,shell=True).wait()

else:
    pass
