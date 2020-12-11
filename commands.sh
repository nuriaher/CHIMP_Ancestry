ssh -X clf254@demeter.binf.ku.dk
ssh -X clf254@artemis.binf.ku.dk
Chimpsnuria97.

"/isdata/hansgrp/pfrandsen/Projects/Student/Nuria"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

screen
screen -r #see
screen -r -ID- #go inside
cntrl+a+d # deattach
--------

ps -r which are running
ps -ef
kill ID
ps -ef | grep 174367
--------

visualize .vcf: 		less -S
visualize .vcf.gz: 	zless -S
--------

In any PLINK command, --recode is necessary to write output file


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Chimps are related, so ADMIXTURE can't be run on all of them at the same time.
# One by one against a reference panel: ~90 individuals of known subspecies.
#   .Pan troglodytes troglodytes    - Central: Cameroon, Congo
#   .Pan troglodytes verus          - Western
#   .Pan troglodytes ellioti        - Nigeria and Cameroon
#   .Pan troglodytes schweinfurthii - Eastern
#
# Idea: pipeline to process these one by one individuals
# Input: VCF files - can be filtered with VCF-Tools
#        Then turned into PLINK files - filtering with PLINK
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

COMMANDS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

data_path="/isdata/hansgrp/pfrandsen/Projects/Student/Nuria"


- Test  Filter 1.1
		# Filtering commands
1.1R		# 	172672	# nohup python ${data_path}/CHIMP_Ancestry/bin/CA_01.1-Filter-VCF_Rename.py -in_VCF ${data_path}/data/Hvilsom_ZOOchimp_BI_II_all.g.vcf.gz -in_IDs ${data_path}/CHIMP_Ancestry/data/newNAMES_batchI_II.txt -out_path ${data_path}/CA_01-Filtering/ZOOchimp_BI_II -batch_ID ZOOchimp_BI_II > ${data_path}/CA_01-Filtering/fil_BI_II.log &
1.1R		# 	172694	# nohup python ${data_path}/CHIMP_Ancestry/bin/CA_01.1-Filter-VCF_Rename.py -in_VCF ${data_path}/data/Hvilsom_ZOOchimp_BIII_all.g.vcf.gz -in_IDs ${data_path}/CHIMP_Ancestry/data/newNAMES_batchIII.txt -out_path ${data_path}/CA_01-Filtering/ZOOchimp_BIII -batch_ID ZOOchimp_BIII > ${data_path}/CA_01-Filtering/fil_BIII.log &
nohup python ${data_path}/CHIMP_Ancestry/bin/CA_01.1-Filter-VCF_Rename.py -in_VCF ${data_path}/data/Hvilsom_ZOOchimp_BIV_V.all.g.vcf.gz -in_IDs ${data_path}/CHIMP_Ancestry/data/newNAMES_batchIV_V.txt -out_path ${data_path}/CA_01-Filtering/ZOOchimp_BIV_V -batch_ID ZOOchimp_BIV_V > ${data_path}/CA_01-Filtering/ZOOchimp_BIV_V/fil_BIV_V.log &
		nohup python ${data_path}/CHIMP_Ancestry/bin/CA_01.1-Filter-VCF_Rename.py -in_VCF ${data_path}/data/Hvilsom_ZOOchimp_BVI_all.g.vcf.gz -in_IDs ${data_path}/CHIMP_Ancestry/data/newNAMES_batchVI.txt -out_path ${data_path}/CA_01-Filtering/ZOOchimp_BVI -batch_ID ZOOchimp_BVI > ${data_path}/CA_01-Filtering/ZOOchimp_BVI/fil_BVI.log &


- Test  Filter 1.2
nohup python ${data_path}/CHIMP_Ancestry/bin/CA_01.2-Filter-Split_PLINK.py -in_plink ${data_path}/CA_01-Filtering/ZOOchimp_BI_II-in_Plink_reformat -new_IDs ${data_path}/CA_01-Filtering/ZOOchimp_BI_II/ZOOchimp_BI_II-new_IDs.txt -out_base ${data_path}/CA_01-Filtering/ZOOchimp_BI_II -batch_ID ZOOchimp_BI_II > ${data_path}/CA_01-Filtering/ZOOchimp_BI_II/fil_BI_II.log &
nohup python ${data_path}/CHIMP_Ancestry/bin/CA_01.2-Filter-Split_PLINK.py -in_plink ${data_path}/CA_01-Filtering/ZOOchimp_BIII-in_Plink_reformat -new_IDs ${data_path}/CA_01-Filtering/ZOOchimp_BIII/ZOOchimp_BIII-new_IDs.txt -out_base ${data_path}/CA_01-Filtering/ZOOchimp_BIII -batch_ID ZOOchimp_BIII > ${data_path}/CA_01-Filtering/ZOOchimp_BIII/fil_BIII.log &
nohup python ${data_path}/CHIMP_Ancestry/bin/CA_01.2-Filter-Split_PLINK.py -in_plink ${data_path}/CA_01-Filtering/ZOOchimp_BIV_V-in_Plink_reformat -new_IDs ${data_path}/CA_01-Filtering/ZOOchimp_BIV_V/ZOOchimp_BIV_V-new_IDs.txt -out_base ${data_path}/CA_01-Filtering/ZOOchimp_BIV_V -batch_ID ZOOchimp_BIV_V > ${data_path}/CA_01-Filtering/ZOOchimp_BIV_V/fil_BIV_V.log &

- Pipeline commands
nohup python ${data_path}/CHIMP_Ancestry/chimp_ancestry.py -input ${data_path}/input_BI_II.txt -out_path ${data_path} --admx_plot --pca_plot > ${data_path}/CA_BI_II.log &
#nohup python ${data_path}/CHIMP_Ancestry/chimp_ancestry.py -input ${data_path}/input_BIII.txt -out_path ${data_path} --pca_plot > ${data_path}/CA_BIII.log &
nohup python ${data_path}/CHIMP_Ancestry/chimp_ancestry.py -input ${data_path}/input_BIV_V.txt -out_path ${data_path} --admx_plot --pca_plot > ${data_path}/CA_BIV_V.log &

	# two samples together BVI-BIII
	nohup python ${data_path}/CHIMP_Ancestry/chimp_ancestry.py -input ${data_path}/input_BVI-BIII.txt -out_path ${data_path} --admx_plot --pca_plot > ${data_path}/CA_BVI-BIII.log &
