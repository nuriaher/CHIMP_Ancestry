#### 27.11.20
import subprocess
import argparse
import sys
import os


#Argument parsing
parser = argparse.ArgumentParser(description='Runs Chimp Ancestry.')
parser.add_argument('-bed_base', help="filtered PLINK output base", dest="bed_base", required=True)
parser.add_argument('-output', help="output file", dest="output", required=True)
parser.add_argument('-t', help="threads", dest="threads", required=True)
args = parser.parse_args()

bed_base=args.bed_base
output=args.output
threads=args.threads



# Evaladmix command


#fname path to ancestral population frequencies file (space delimited matrix where rows are sites and columns ancestral populations)
#path to admixture proportions file (space delimited matrix where rows are individuals and columns ancestral populations)

evaladmixCmd='./evalAdmix -plink '+bed_base+' -fname '+bed_base+'.K.P -qname '+bed_base+'.K.Q -P '+threads+' -o '+output+''
subprocess.Popen(evaladmixCmd).wait()
