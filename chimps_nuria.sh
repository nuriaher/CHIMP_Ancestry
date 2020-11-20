ssh -X clf254@demeter.binf.ku.dk
ssh -X clf254@artemis.binf.ku.dk
Chimpsnuria97.

"/isdata/hansgrp/pfrandsen/Projects/Student/Nuria"

######################################################################

Chimps are related, so ADMIXTURE can't be run on all of them at the same time.
One by one against a reference panel: ~90 individuals of known subspecies.
  .Pan troglodytes troglodytes    - Central: Cameroon, Congo
  .Pan troglodytes verus          - Western
  .Pan troglodytes ellioti        - Nigeria and Cameroon
  .Pan troglodytes schweinfurthii - Eastern

Idea: pipeline to process these one by one individuals
Input: VCF files - can be filtered with VCF-Tools
       Then turned into PLINK files - filtering with PLINK


######################################################################


Steps:
-1. Do ADMIXTURE on Reference Panel and check with evalADMIX: identify if underlying level of ERROR.

0. DATA FILTERING -> PLINK
  # https://www.cog-genomics.org/plink/1.9/index

1. Relatedness check of 1 query individual vs Reference Panel - Theoretically unrelated. Check anyway.
  # METHOD: NGS relate
  https://github.com/ANGSD/NgsRelate/blob/master/README.md

2. Origin identification of individual using Reference Panel.
  # METHOD: ADMIXTURE

3. Check fit of ADMIXTURE model - Output is a correlation: can we get quantitative output? matrix or so.
                                    . If we can: set a threshold
                                    . If we cant simply output the plot - Stay with this for now
  # METHOD: evalADMIX (Genis)


######################################################################

########
######## 1. Filtering
########
# VCF
--minDP          - minimum seq depth

# PLINK
--not-chr         - Exclude all variants on the specified chromosomes. (X,Y)
--remove          ../rmDonald.txt
--indep-pairwise  - These commands produce a pruned subset of markers that are in approximate linkage equilibrium with each other. They are currently based on correlations between genotype allele counts.
                    <window size>[kb] <step size (variant ct)> <r^2 threshold>
                    Accepted 0.5 
