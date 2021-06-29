library(reliabilitydiag)

args = commandArgs(trailingOnly=TRUE)
file <- args[1]
X_file <- paste0('outputs-r202/', file, '-rej-X.txt')
Y_file <- paste0('outputs-r202/', file, '-rej-Y.txt')
output_file <- paste0('outputs-r202/', file[1:(nchar(file)-11)], '-reliabilitydiag.png', '')
X <- scan(X_file)
Y <- scan(Y_file)
res <- reliabilitydiag(x = X, y = Y)
reliablity_score <- (summary(res))$miscalibration
parent <- strsplit(file, '/')[[1]][1]
write(reliablity_score,file=paste0('outputs-r202/', parent, '-score.txt'),append=TRUE)

plot(res)
png(output_file)
print(res)
dev.off()
