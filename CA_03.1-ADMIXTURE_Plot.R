library("RColorBrewer")
tbl <-read.table("Desktop/ZOOChimp_14221_Whisky_plink.pruned.4.Q")
fam <-read.table("Desktop/ZOOChimp_14221_Whisky_plink.pruned.fam")

pdf(file ="Desktop/Whisky.pdf")
par(mar=c(1.5,4,2.5,2),cex.lab=0.75,cex.axis=0.6)
barplot(t(as.matrix(tbl)),
        col=brewer.pal(6,"Set1"), ylab = 'Ancestry Proportions',
        border = NA, space = 0) + title(main=paste0(fam$V1[1],' vs Reference Panel')) 

dev.off()


