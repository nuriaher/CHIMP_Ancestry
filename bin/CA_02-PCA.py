#### 26.11.20
import subprocess
import argparse
import sys
import os


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-filt_bed', help="filtering step PLINK output", dest="filt_bed", required=True)
parser.add_argument('--pca_plot', help="Wants to get a .pdf PCA Plot", dest="input", required=True)
parser.add_argument('-out_path', help="output path", dest="out_path", required=True)
parser.add_argument('-batch_ID', help="batch_ID", dest="batch_ID", required=True)
parser.add_argument('-ind_ID', help="individual ID", dest="ind_ID", required=True)
args = parser.parse_args()

filt_bed=args.filt_bed
out_path=args.out_path
ind_ID=args.ind_ID
batch_ID=args.batch_ID



## Run

    # Generate .eigenvalues .eigenvectors files
out_base=out_path+'/'+batch_ID'-'+ind_ID

pcaCmd='plink1 --bfile '+filt_bed+' --pca 10 --out '+out_base+''
subprocess.Popen(pcaCmd,shell=True).wait()


if args.pca_plot:
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
