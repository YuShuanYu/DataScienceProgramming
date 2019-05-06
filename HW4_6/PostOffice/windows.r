
dataset <- read.csv("/Users/kiki/Desktop/PostData/dealed_data/PostOffice.csv")

rownames(dataset)<- dataset$office
dataset <- dataset[,-1]
dataset <- t(dataset)
head(dataset)

ind <- which(as.matrix(apply(dataset, 1, sum))==0)
dataset <- dataset[-ind,]
ind <- which(as.matrix(apply(dataset, 2, sum)) == 0)
dataset <- dataset[,-ind]

tf <- apply(dataset, 2, sum) # term frequency
idf <- function(word_doc){ log2( (length(word_doc)) / length(which(word_doc!=0)) ) }
idf <- apply(dataset, 1, idf)
data.tfidf <- as.matrix(dataset)
for(i in 1:nrow(dataset)){
    for(j in 1:ncol(dataset)){
        data.tfidf[i,j] <- (dataset[i,j] / tf[j]) * idf[i]
    }
}

head(data.tfidf)

t = as.data.frame(t(data.tfidf))
t = apply(t, 2, as.numeric)
pcat = prcomp(t)

pca <- pcat$x[, 1:2]
pca.eigenvector <- pcat$rotation[, 1:2]

dataset <- as.data.frame(t(dataset))
scaled_df <- apply(dataset, 2, scale)

PC1 <- as.matrix(scaled_df) %*% pca.eigenvector[,1]
PC2 <- as.matrix(scaled_df) %*% pca.eigenvector[,2]

ndata <- data.frame( Office = rownames(dataset), PC1, PC2)

ndata$dis <- (ndata$PC1^2+ ndata$PC2^2)^0.5
ind <- which(ndata$dis <= 1)
ndata_sub <- subset(ndata, dis <= 1)
dataset_sub <- dataset[ind,]

library(arules)
df <- data.frame(matrix(NA,dim(dataset_sub)[1],dim(dataset_sub)[2]))
for(i in 1:dim(dataset_sub)[1]){
  for(j in 1:dim(dataset_sub)[2]){
    if (dataset_sub[i,j]==0){
      df[i,j] <- FALSE
    }else{
      df[i,j] <- TRUE
    }
  }
}



sup = apriori(df, parameter=list(minlen=4, supp=0.3, conf=0.7))
sup <- sort(sup, by="lift")

sup <- sort(sup, by="support")
subset.matrix <- as.matrix(is.subset(x=sup, y=sup))
subset.matrix[lower.tri(subset.matrix, diag=T)] <- NA
redundant <- colSums(subset.matrix, na.rm=T) >= 1
sup_sub <- sup[!redundant]
save(sup_sub,sup, file = "aprioridata.RData")
load("/Users/kiki/Documents/GitHub/DataScienceProgramming/HW4_6/PostOffice/aprioridata.rdata")
plot(sup_sub, method="graph")
plot(sup_sub, method="grouped")
