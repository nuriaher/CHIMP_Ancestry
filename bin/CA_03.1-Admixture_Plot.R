library("RColorBrewer")
library("argparse")
library("ggplot2")
library("tidyverse")


# Parse inputs
parser <-  ArgumentParser(description='Runs Chimp Ancestry.')
parser$add_argument('--Q_admx', dest='Q_admx', help='Q file outputted by ADMIXTURE', required=TRUE)
parser$add_argument('--fam_file', dest='fam_path', help='fam file', required=TRUE)
parser$add_argument('-ind_ID', dest='individual', help='individual ID', required=TRUE)
parser$add_argument('-batch_ID', dest='batch', help='sample batch', required=TRUE)
parser$add_argument('-out_path', dest='out_path', help='directory to redirect output', required=TRUE)
args <- parser$parse_args()

# Define variables
Q_admx <- args$Q_admx
fam_path <- args$fam_path
individual <- args$individual
batch <- args$batch
out_path <- args$out_path

# Read necessary files
tbl <-read.table(Q_admx)
fam <-read.table(fam_path)


# Rearrange data 
plot_data <- tbl %>%
  mutate(id = fam$V1) %>%
  gather('pop', 'prob', V1:V4) %>%
  group_by(id) %>%
  mutate(likely_assignment = pop[which.max(prob)],
         assingment_prob = max(prob)) %>%
  arrange(likely_assignment, desc(assingment_prob)) %>%
  ungroup() %>%
  mutate(id = forcats::fct_inorder(factor(id)))


# Plot
admx <- ggplot(plot_data, aes(id, prob, fill = pop)) +
  geom_col() + facet_grid(~likely_assignment, scales = 'free', space = 'free') +
  theme(axis.text.x = element_text(angle = 90, size=7))

title <- paste0(individual," vs Reference panel")
admx <- admx + ggtitle(title)


ggsave(plot = admx, filename = paste0("ADMIXTURE-",batch,"-",individual,".pdf"), path = out_path)
