# Q file looks like this
# The FIRST row is the QUERY individual, the rest is the REFERENCE PANEL

0.000018 0.999962 0.000010 0.000010
0.000010 0.000010 0.999970 0.000010


# .FAM file looks like this
# Should have same number of entries as Q file

ZOOChimp_430_BigMac ZOOChimp_430_BigMac 0 0 0 -9
Pt-A996_Diana Pt-A996_Diana 0 0 0 -9
Pt-B010_Ikuru Pt-B010_Ikuru 0 0 0 -9



# Read .Q
# Find 0.99*** in line , else pass
# Split line by ' '
# Save position in line where 0.99*** is (same-subspecies RefPanel will have it in same place)
# For every line, split, look for 0.99*** in line[saved position] , else pass
# If found, append positions in .readlines()to list

# Read .fam file
# Split lines by ' '
# Append first two fields  ( = ID file )
# Write in .txt


# Create NGS .VCF files : ZOOChimp + Same ancestry RefPanel
# Plink .bed files in CA_01-Filtering/Batch/Batch_indv/Individual.bed:
    #keepCmd='plink1.9 --file '+in_plink_filtering+' --keep '+ID_ancestral_pop+' --recode vcf --out '+plink_prefix+''
# Append plink_prefix_individual (output to be returned to chimp_ancestry.py)

------ In chimp_ancestry.py, do NGS relate for every plink_prefix_individual
