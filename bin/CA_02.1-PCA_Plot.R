library("argparse")
library("ggplot2")
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
evec_pc$subspp[grep("P_t_troglodytes", evec_pc$IDs)] <- "Pt_troglodytes"
evec_pc$subspp[grep("P_t_ellioti", evec_pc$IDs)] <- "Pt_ellioti"
evec_pc$subspp[grep("P_t_verus", evec_pc$IDs)] <- "Pt_verus"
evec_pc$subspp[grep("P_t_schweinfurthii", evec_pc$IDs)] <- "Pt_schweinfurthii"

  # Convert eigen values to percentage of explained variance
p_eval <- data.frame(PC = 1:10, p_eval = eval_pc/sum(eval_pc)*100) ######################################## CHECK IF ACTUALLY ONLY 10 PC (should be, --pca 10)


# Plot PCA and save as pdf
pca <- ggplot(evec_pc, aes(PC1, PC2, col = as.factor(subspp))) + geom_point(size = 3)
pca <- pca + scale_colour_manual(values = c("blue", "green", "purple", "orange", "grey"))
pca <- pca + coord_equal() + theme_light()
pca + xlab(paste0("PC1 (", signif(p_eval$p_eval[1], 3), "%)")) + ylab(paste0("PC2 (", signif(p_eval$p_eval[2], 3), "%)"))

ggsave(pca, device = NULL, path = out_path, filename = paste0("PCA_",batch,"-",individual,".pdf"))
