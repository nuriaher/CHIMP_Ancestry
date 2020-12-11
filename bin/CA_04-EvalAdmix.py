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
parser.add_argument('-output', help="output file", dest="output", required=True)
parser.add_argument('-t', help="threads", dest="threads")
args = parser.parse_args()

plink_base=args.plink_base
admx_base=args.admx_base
output=args.output

if args.threads:
    threads=str(args.threads)
else:
    threads=str(1)



# Evaladmix command


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
    pop plink_base.fam
    q admx_base.k.Q
    r output

    

    admxplotCmd='Rscript '+curr_dir+'/CA_03.1-Admixture_Plot.R --Q_admx '+Q_file+' --fam_file '+fam_file+' -ind_ID '+ind_ID+' -batch_ID '+batch_ID+' -out_path '+out_path+''
    subprocess.Popen(admxplotCmd,shell=True).wait()
