library(reliabilitydiag)

args = commandArgs(trailingOnly=TRUE)
parent <- args[1]
child <- args[2]
file <- paste0(parent, '-', child)
X_file <- paste0('outputs-GTDB-r202/', file, '-rej-X.txt')
Y_file <- paste0('outputs-GTDB-r202/', file, '-rej-Y.txt')
output_file <- paste0('outputs-GTDB-r202/', file, '-reliabilitydiag.png', '')
X <- scan(X_file)
Y <- scan(Y_file)
res <- reliabilitydiag(x = X, y = Y)
reliablity_score <- (summary(res))$miscalibration
write(reliablity_score,file=paste0('outputs-GTDB-r202/', parent, '-score.txt'),append=TRUE)

plot(res)
png(output_file)
print(res)
dev.off()
