library("RColorBrewer")
library("argparse")


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

# Generate Subspecies column - plot's sake
fam$subspp <- ''
fam$subspp[grep("Pt_troglodytes", fam$V1)] <- "Pt_troglodytes"
fam$subspp[grep("Pt_ellioti", fam$V1)] <- "Pt_ellioti"
fam$subspp[grep("Pt_verus", fam$V1)] <- "Pt_verus"
fam$subspp[grep("Pt_schweinfurthii", fam$V1)] <- "Pt_schweinfurthii"
Subspecies_in_sample=levels(as.factor(fam$subspp))
Subspecies_in_sample=Subspecies_in_sample[Subspecies_in_sample != ""]


pdf(file = paste0(out_path,"/ADMIXTURE-",batch,"-",individual,".pdf"))
par(mar=c(7.5,4,2.5,6.5),cex.lab=0.75,cex.axis=0.6)
barplot(t(as.matrix(tbl)),
        col=brewer.pal(6,"Set1"), ylab = 'Ancestry Proportions',
        border = NA, space = 0, names.arg = fam$V1,
        las=2, cex.names = 0.4, main=paste0(fam$V1[1],' vs Reference Panel'), cex.main=1 )
legend("right", Subspecies_in_sample, fill = brewer.pal(6,"Set1"), bty = "n", xpd=TRUE, inset = -0.25, cex=.8)
dev.off()


