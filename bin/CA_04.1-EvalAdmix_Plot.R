library("argparse")


# Parse inputs
parser <-  ArgumentParser(description='Runs Chimp Ancestry.')
parser$add_argument('-fam_file', dest='fam_file', help='population fam data', required=TRUE)
parser$add_argument('-Q_admx', dest='Q_admx', help='Q admixture output file', required=TRUE)
parser$add_argument('-matrix_out', dest='matrix_out', help='evalAdmix output matrix', required=TRUE)
parser$add_argument('-ind_ID', dest='individual', help='individual ID', required=TRUE)
parser$add_argument('-batch_ID', dest='batch', help='sample batch', required=TRUE)
parser$add_argument('-out_path', dest='out_path', help='directory to redirect output', required=TRUE)
parser$add_argument('-script_path', dest='script_path', help='visfuns directory', required=TRUE)
args <- parser$parse_args()

# Define variables
Q_admx <- args$Q_admx
fam_file <- args$fam_file
matrix_out <- args$matrix_out
individual <- args$individual
batch <- args$batch
out_path <- args$out_path
script_path <- args$script_path

source(paste0(script_path,"/evalAdmix_visFuns.R"))

pop <- as.vector(read.table(fam_file)) # N length character vector with each individual population assignment
q <- as.matrix(read.table(Q_admx)) # admixture porpotions q is optional for visualization but if used for ordering plot might look better
r <- as.matrix(read.table(matrix_out))

ord <- orderInds(pop=as.vector(pop)[,2], q=q) # ord is optional but this make it easy that admixture and correlation of residuals plots will have individuals in same order


pdf(file = paste0(out_path,"/Correlation_Residuals-",batch,"-",individual,".pdf"))
plotCorRes(cor_mat = r, pop = as.vector(pop)[,2], ord=ord, title = "Admixture evaluation as correlation of residuals", max_z=0.25, min_z=-0.25, cex.lab = 0.5)
dev.off()
