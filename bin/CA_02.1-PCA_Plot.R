library("argparse")
library("ggplot2")
library("dplyr")
library("tidyverse")

# Parse inputs
parser <-  ArgumentParser(description='Runs Chimp Ancestry.')
parser$add_argument('--eval', dest='eval', help='eigen values outputted by PLINK --pca', required=TRUE)
parser$add_argument('--evec', dest='evec', help='eigen vectors outputted by PLINK --pca', required=TRUE)
parser$add_argument('-ind_ID', dest='individual', help='individual bed analysed by PLINK --pca', required=TRUE)
parser$add_argument('-batch_ID', dest='batch', help='sample batch', required=TRUE)
parser$add_argument('-out_path', dest='out_path', help='directory to redirect output', required=TRUE)
args <- parser$parse_args()

# Define variables
eval <- args$eval
evec <- args$evec
individual <- args$individual
batch <- args$batch
out_path <- args$out_path

# Read PLINK output
evec_pc <- read_table2(evec, col_names = FALSE)
eval_pc <- scan(eval)

# Fix data to plot
  # Remove nuisance column - plink outputs the individual ID twice
evec_pc <- evec_pc[,-1]

  # Give columns proper names
names(evec_pc)[1] <- "IDs"
names(evec_pc)[2:ncol(evec_pc)] <- paste0("PC", 1:(ncol(evec_pc)-1))

  # Generate Subspecies column - plot's sake
evec_pc$subspp <- ''
evec_pc$subspp[grep("ZOOChimp", evec_pc$IDs)] <- "ZOOChimp"
evec_pc$subspp[grep("Pt_troglodytes", evec_pc$IDs)] <- "Pt_troglodytes"
evec_pc$subspp[grep("Pt_ellioti", evec_pc$IDs)] <- "Pt_ellioti"
evec_pc$subspp[grep("Pt_verus", evec_pc$IDs)] <- "Pt_verus"
evec_pc$subspp[grep("Pt_schweinfurthii", evec_pc$IDs)] <- "Pt_schweinfurthii"


  # Convert eigen values to percentage of explained variance
p_eval <- data.frame(PC = 1:10, p_eval = eval_pc/sum(eval_pc)*100)

# Plot PCA and save as pdf
title <- paste0(individual," vs Reference Panel")


Subspecies_in_sample=as.factor(evec_pc$subspp)

pca <- ggplot(evec_pc, aes(PC1, PC2, col = Subspecies_in_sample)) + geom_point(alpha = 0.5, size = 4)
ggtitle(title)

pc_1 = paste0("PC1 (", round(p_eval[,2][1],2), "%)")
pc_2 = paste0("PC1 (", round(p_eval[,2][2],2), "%)")

if (length(levels(as.factor(evec_pc$subspp))) == 5){
  pca <- pca + scale_colour_manual(values = c("blue", "orange", "yellow", "purple","green"))}
if (length(levels(as.factor(evec_pc$subspp))) == 6){
  pca <- pca + scale_colour_manual(values = c("blue", "orange", "yellow", "purple" , "red", "green"))}

pca <- pca + coord_equal() + theme_light() + xlab(pc_1) + ylab(pc_2)

ggsave(pca, device = NULL, path = out_path, filename = paste0("PCA_",batch,"-",individual,".pdf"))
