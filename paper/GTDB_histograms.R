tab1 = read.table(file = "/Users/wanxinli/Desktop/project.nosync/MLDSP-desktop/samples/Table_S1_new.csv", sep = ",", header = TRUE)
tab1 = tab1[which(tab1$Species!='s__'),]
library(ggplot2)

pdf("/Users/wanxinli/Desktop/project.nosync/MLDSP-desktop/outputs-HGR-r202/HGR_bar_charts.pdf")
#ALL DATA

#GC content histogram
qplot(tab1$gc_percentage, geom="histogram", ylab = "Number of genomes (all)", xlab = "Percent GC")

#contig count, outliers above 1000 removed
qplot(tab1$contig_count, geom = "histogram", ylab = "Number of genomes (all)", xlab = "Contig count")

#genome size
qplot(tab1$genome_size, geom = "histogram", ylab = "Number of genomes (all)", xlab = "Genome size in basepairs")
# 
dev.off()
# #REPRESENTATIVES
# 
# tab2 = tab1[which(tab1$gtdb_representative=="t"),]
# 
# #GC content histogram
# qplot(tab2$gc_percentage, geom="histogram", ylab = "Number of genomes (species-level representatives)", xlab = "Percent GC")
# 
# #contig count, outliers above 1000 removed
# qplot(tab2[which(tab2$contig_count<1000),2], geom = "histogram", , ylab = "Number of genomes (species-level representatives)", xlab = "Contig count (max 1000 displayed)")
# 
# #genome size
# qplot(tab2[which(tab2$genome_size<12500000),5], geom = "histogram", ylab = "Number of genomes (species-level representatives)", xlab = "Genome size in basepairs (max 1.25 Gbp displayed)")
