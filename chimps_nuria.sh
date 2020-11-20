ssh -X clf254@demeter.binf.ku.dk
ssh -X clf254@artemis.binf.ku.dk
Chimpsnuria97.

Chimps are related, so ADMIXTURE can't be run on all of them at the same time.
One by one against a reference panel: ~90 individuals of known subspecies.
  .Pan troglodytes troglodytes    - Central: Cameroon, Congo
  .Pan troglodytes verus          - Western
  .Pan troglodytes ellioti        - Nigeria and Cameroon
  .Pan troglodytes schweinfurthii - Eastern

Idea: pipeline to process these one by one individuals
Input: VCF files - can be filtered with VCF-Tools
       Then turned into PLINK files - filtering with PLINK


Steps:
-1. DATA FILTERING -> PLINK

0. Do ADMIXTURE on Reference Panel and check with evalADMIX: identify if underlying level of ERROR.

1. Relatedness check of 1 query individual vs Reference Panel - Theoretically unrelated. Check anyway.
  METHOD: NGS relate

2. Origin identification of individual using Reference Panel.
  METHOD: ADMIXTURE

3. Check fit of ADMIXTURE model - Output is a correlation: can we get quantitative output? matrix or so.
                                    . If we can: set a threshold
                                    . If we cant simply output the plot - Stay with this for now
  METHOD: evalADMIX (Genis)
