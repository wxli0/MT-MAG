library(reliabilitydiag)
library(ggplot2)

args = commandArgs(trailingOnly=TRUE)
data_type <- args[1]
parent <- args[2]
X_file <- paste0('outputs-', data_type, '/', parent, '-rej-X.txt')
Y_file <- paste0('outputs-', data_type, '/', parent, '-rej-Y.txt')
output_file <- paste0('outputs-', data_type, '/', parent, '-RD.png')
X <- scan(X_file)
Y <- scan(Y_file)
res <- reliabilitydiag(x = X, y = Y, region.level = NA)
res_plot <- reliabilitydiag::autoplot(res, params_histogram = NA)
res_final <- res_plot + theme(axis.text.x = element_text(size=14), axis.text.y = element_text(size=14))
reliablity_score <- (summary(res))$miscalibration
write(reliablity_score,file = paste0('outputs-', data_type, '/', parent, '-score.txt'),append=TRUE)

png(output_file)
print(res_final)
dev.off()
