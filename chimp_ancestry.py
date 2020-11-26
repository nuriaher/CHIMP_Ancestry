#Núria Hermosilla-Albala
#20.11.20

##########################################################
############# CHIMP Ancestry Pipeline EEP ################
##########################################################

#a = system("echo This_is_the_output", intern = TRUE)



######
### 1 - VCF from NGS variant calling Filtering
###



######
### 2 - PCA - Over all filtered data (Ref Panel.coloured , Unkown ancestries.grey)
###



######
### 3 - ADMIXTURE - Reference Panel x 1 Query Individual (avoid relatedness bias)
###



######
### 4 - evalADMIX - Evaluate ADMIXTURE Output for Reference Panel x 1 Query Individual
###



######
### 5 - NGSRelate2 - Relatedness: 1 Query Individual x ADMIXTURE estimated ancestral population
###



######
### 6 - NGSRelate2 - Inbreeding : 1 Query Individual
###



######
### *** 7 *** - Estimate genomic diversity 1 Query Individual
###
