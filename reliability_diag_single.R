library(reliabilitydiag)

args = commandArgs(trailingOnly=TRUE)
data_type <- args[1]
parent <- args[2]
X_file <- paste0('outputs-', data_type, '/', parent, '-rej-X.txt')
Y_file <- paste0('outputs-', data_type, '/', parent, '-rej-Y.txt')
output_file <- paste0('outputs-', data_type, '/', parent, '-RD.png')
X <- scan(X_file)
Y <- scan(Y_file)
res <- reliabilitydiag(x = X, y = Y)
reliablity_score <- (summary(res))$miscalibration
write(reliablity_score,file = paste0('outputs-', data_type, '/', parent, '-score.txt'),append=TRUE)

png(output_file)
print(res)
dev.off()
