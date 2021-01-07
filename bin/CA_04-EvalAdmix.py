#### 27.11.20
import subprocess
import argparse
import sys
import os


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-plink_base', help="filtered PLINK output binary base", dest="plink_base", required=True)
parser.add_argument('-admx_base', help="admixture output base", dest="admx_base", required=True)
parser.add_argument('--evalAdmix_plot', help="Wants to get a .pdf evalADMIX Plot", dest="evalAdmix_plot", action='store_true')
parser.add_argument('-batch_ID', help="batch_ID", dest="batch_ID", required=True)
parser.add_argument('-ind_ID', help="individual ID", dest="ind_ID", required=True)
parser.add_argument('-out_path', help="output path", dest="out_path", required=True)
parser.add_argument('-t', help="threads", dest="threads")
args = parser.parse_args()

plink_base=args.plink_base
admx_base=args.admx_base
batch_ID=args.batch_ID
ind_ID=args.ind_ID
out_path=args.out_path

if args.threads:
    threads=str(args.threads)
else:
    threads=str(1)



# Evaladmix command

output = out_path+'/EvalAdmix_'+batch_ID+'-'+ind_ID+'.txt'
#fname path to ancestral population frequencies file (space delimited matrix where rows are sites and columns ancestral populations)
#path to admixture proportions file (space delimited matrix where rows are individuals and columns ancestral populations)
k = str(4) # Number of chimp subspecies
if not os.path.exists(output):
    evaladmixCmd='evalAdmix -plink '+plink_base+' -fname '+admx_base+'.'+k+'.P -qname '+admx_base+'.'+k+'.Q -P '+threads+' -o '+output+''
    subprocess.Popen(evaladmixCmd,shell=True).wait()
else:
    pass

    # Plot
    if args.evalAdmix_plot:
        fam_file = plink_base+'.fam'
        Q_file = admx_base+'.'+k+'.Q'

        # Get current directory
        file = os.path.dirname(sys.argv[0])
        curr_dir = os.path.abspath(file)


        evaladmxplotCmd='Rscript '+curr_dir+'/CA_04.1-EvalAdmix_Plot.R -Q_admx '+Q_file+' -fam_file '+fam_file+' -matrix_out '+output+' -ind_ID '+ind_ID+' -batch_ID '+batch_ID+' -script_path '+curr_dir+' -out_path '+out_path+''
        subprocess.Popen(evaladmxplotCmd,shell=True).wait()

    else:
        pass
