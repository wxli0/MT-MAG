library(reliabilitydiag)

args = commandArgs(trailingOnly=TRUE)
file <- args[1]
output_file <- paste(file[1:(nchar(file)-11)], '-reliabilitydiag.png', '')
X <- scan(file)
Y <- scan(file)
res <- reliabilitydiag(x = X, y = Y)
png(output_file)
print(res)
dev.off()
