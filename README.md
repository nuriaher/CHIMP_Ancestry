# CHIMP Ancestry Pipeline
### Filtering and Ancestry estimation of Chimpanzee high-quality NGS data

## Running CHIMP_Ancestry
Designed to be run in *Artemis KU Server* (Log in: ssh -X ID@artemis.binf.ku.dk).  
This pipeline is to be used on a batch of individual samples which contains a reference panel and a number X of query samples to be tested.  

### Input file 
An *input.txt* file is required with the following fields **white-space delimited**:

```bash
#batchID,vcf_path, Family and Within-family IDs file path
Chimps1 my/user/directory/path/chimps1.vcf.gz my/user/directory/path/chimps1_old_IDs.txt
Chimps2 my/user/directory/path/chimps2.vcf.gz my/user/directory/path/chimps2_old_IDs.txt
```
The .VCF file can be both compressed and not compressed.  
If you still have doubts, check the example Input file above.

### IDs file 
An *individuals_IDs.txt* file is required with the following fileds **tab delimited**:  
#### Want to update the IDs
The IDs file is necessary when one wants to modify the individuals' IDs in the .VCF file. For this, the IDs file will have to contain **two identical columns tab delimited** which will contain one row for each individual's ID in the VCF file, the original ones. The new and simplified IDs will be automatically generated. See more in the section *--update-ids* of the [PLINK Software manual](https://www.cog-genomics.org/plink/1.9/data#update_indiv).

* Keep in mind that the new IDs are **automatically generated and pattern-search-based**. Therefore, if you have in mind to use the pipeline, make sure the .VCF IDs of your reference-panel samples contain the pattern *Pan_troglodytes* and if your query samples contain the word *chimp*, make it lower-case.

#### Do not want to update the IDs
If you *do not want to update the IDs*, can simply give the pipeline a file which contains one single row with four text fields tab delimited, it does not matter what is written there, if the pipeline detects 4 fields it will skip the updating step.  
  
If you still have doubts, check the example IDs file above.

### Command
Once the pre-requisites are fullfiled, run this command on the *Artemis* terminal:
```bash
${pipeline_path}="my/user/directory/path/pipeline"
${my_path}="my/user/directory/path/bla"
nohup python ${pipeline_path}/CHIMP_Ancestry/chimp_ancestry.py -input ${my_path}/input_SAMPLEBATCH.txt -out_path ${my_path} > ${my_path}/SAMPLEBATCH.log &

```

This command:
* **It is meant to be run on the directory which contains the cloned GitHub repository "CHIMP_Ancestry".**
* Will produce a .log file in the specified path where the process of the pipeline can be followed.  
* Has some required arguments and some optional ones which can be added:

```bash
required arguments:
  -input    {input_file_path}     batchID, vcf file path, Family and Within-family IDs file path
  -out_path {output_path}         output path
optional arguments:
  --pca_plot                            wants to get a .pdf PCA Plot
  --admx_plot                           wants to get a .pdf ADMIXTURE results Plot
  --evalAdmix_plot                      wants to get a .pdf evalADMIX correlations Plot
  --t_admixture         {new_num}       admixture number of threads, default 10
  --t_evaladmx          {new_num}       evaladmix number of threads, default 1
  --t_ngsrelate         {new_num}       ngsrelate number of threads, default 4  
```  

