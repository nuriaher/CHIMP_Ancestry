ssh -X clf254@demeter.binf.ku.dk
ssh -X clf254@artemis.binf.ku.dk
Chimpsnuria97.

"/isdata/hansgrp/pfrandsen/Projects/Student/Nuria"

git clone https://github.com/nuriaher/CHIMP_Ancestry.git
######################################################################

0. Data filtering  - Plink, VCF
1. Admixture       -
2. Relatedness     - https://github.com/ANGSD/NgsRelate/blob/master/README.md
3. evalAdmixture   -


######################################################################

## 20.11.20 ##
PIPELINE:

0. DATA FILTERING -> PLINK
  # VCF- min depth 4, minQ 30, removeIndels
# PLINK- maf 0.05, geno 0, LD allow 50%

1. Check relatedness 1 query individual vs Reference panel - Theoretically unrelated.
  # METHOD: NGS relate - https://github.com/ANGSD/NgsRelate
2. Ancestry identification 1 individual x Reference Panel.
  # METHOD: ADMIXTURE
3. Check fit of ADMIXTURE model -
 # METHOD: evalADMIX (Genis-Anders Albrechsten)


PUBLICATION:

. EEP related individuals  + sanctuary populations -  analysed separately one by one against a reference panel of all wild born individuals.
. MAF filter (--maf 0.05) in PLINK
. Individuals admixture coefficients >0.99  NGSRELATEv2
	-> estimate pairwise relatedness and individual inbreeding coefficients based on population allele frequencies from inferred admixture clusters


## 26.11.20 ##
	# New working dir
data_path="/isdata/hansgrp/pfrandsen/Projects/Student/Nuria"

	- Wrote PCA (python and R)
	- Test Filtering by steps - saw that programs add the .extensions: CHECK OUTPUT NAMES

# Batch samples
Hvilsom_ZOOchimp_BIV_V.all.g.vcf.gz			102 individuals
Hvilsom_ZOOchimp_BI_II_all.g.vcf.gz			73 individuals
Hvilsom_ZOOchimp_BVI_all.g.vcf.gz
Hvilsom_ZOOchimp_BIII_all.g.vcf.gz

donald_rm.txt
newNAMES_batchI_II.txt
newNAMES_batchIII.txt
newNAMES_batchIV_V.txt
newNAMES_batchVI.txt

## 27.11.20 ##

#- The other way around:
	# .first VCF filtering all together
	# .split into different bed files (Ref panel + 1 individual)
	# .All with these files

# - REMOVE BLANK LINES IN INPUT.TXT


## 30.11.20 ##

# - What is the name of NGSRelate2 in the server?
# - Ask install evalADMIX


# - batchIV_V jas finished VCF filtering: -------------- BI_II, BIII -- Running 1.1, should work
# 		. YES but error:
# 						After filtering, kept 76653948 out of a possible -1434190462 Sites
# 						File does not contain any sites
# 			The "not contain any sites" is because these are negative. WHY NEGATIVE?
#
# 		. Now running PLINK recoding + ID_renaming
#
# 						.ped - Original standard text format for sample pedigree information and genotype calls.
# 						.map - A text file with no header file, and one line per variant with the following 3-4 fields:
# 											1	Chromosome code. PLINK 1.9 also permits contig names here.
# 											2	Variant identifier
# 											3	Position in morgans or centimorgans (optional; also safe to use dummy value of '0')
# 											4	Base-pair coordinate



## 1.12.20 ##
# . Everything fixed -- test pipeline with two last samples - SEPARATE INPUT.TXT
# . Test pipeline with 1 input.txt for two first samples

## 8.12.20 ##
. FILTERING
	#-BI_II IDs
	#	A quick fix to this would be to do '--make-bed' on the plink files before the re-naming step and then use the .fam file. Here, the ID is not attached to the whole sequence

. PCA
	#-plot working - MAKE PRETTY
. ADMIXTURE
	#- Artemis 'Segmentation fault', not on Helios - email
	#-How to redirect ADMIXTURE outputs - cd to desired output directory - output created in dir where run
	#-plot R STUDIO! --admixture_plot ASK PETER WHICH SOFTWARE
	- DELTA in ADMIXTURE makes reference to the loglikelihood difference between the Current&Previous iterations.
. NGSRelate2 & evalADMIX
	- Prioritize evalADMIX
	- Test evalADmix plot 




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
											# # # # STATUS # # # # #
											# # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

BI_II 		indv pipeline 		--DONE running evaladmix

BIII			pipeline + BIV_V  --DONE running evaladmix

BVI				indv pipeline 		--DONE running evaladmix

BIV_V			pipeline + BIII  	--DONE running evaladmix




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	- See ADMIXTURE outputs and decide how decide which samples continue to NgsRelate
	- Now all tmp files are kept --> At some point keep only important ones
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
