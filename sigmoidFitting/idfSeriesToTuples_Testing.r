# idfSeriesToTuples_Testing.r
# use this with chandans idf series for a larger set of words. the plot that chandan gave should have the "truth" values of the words
# based on where it is on the plane
args=(commandArgs(TRUE))

library(zoo)
library(xts)

# lets you show or suppress output that I used in debugging
PRINTDETAILS = FALSE

#four parameter sigmoid function; t stands for "time"
sigmoid = function(params,t){
  a1=params[1]
  a2=params[2]
  a3=params[3]
  a4=params[4]
  sigmoid=a1 + a2/(1+exp(-a3*(t-a4)))
}

# these are MANUALLY set:
eventWord = args[1] # "charlotte"
setwd('/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/')
data = read.table(paste('/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/testRawIdf/',
                        eventWord,'.csv',sep = ''),sep = ',',header = FALSE,skip = 1,stringsAsFactors = FALSE)
outFilePath = paste('/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/testDat/',eventWord,'_tuples.csv',sep = '')

numRows = dim(data)[1]
numCols = dim(data)[2]

wordIdfTuples <- data.frame(Word=character(),
                            a1=double(),
                            a2=double(),
                            a3=double(),
                            a4=double(),
                            stringsAsFactors = FALSE)

for(rowNum in c(1:numRows)){
  kword <- data[rowNum,1]
  t <- c(1:(numCols-1))
  y <- as.numeric(data[rowNum,2:numCols])

  if(length(t) != length(y)){
    print("Problem with the y and t lengths!!")
  }
  
  start.time <- Sys.time()
  # fit a sigmoid function to the data. the bounds of the parameter force a2 to be negative and a3 positive
  # this is to ensure that "flipping" the sigmoid to match the datapoints can only occur by vertical flipping, and not horizontal
  # idf plots that are "flat" should result in a small magnitude of a2 (vertical expansion/compression) in order to force this, we
  # set a3 to be greater than 1
  fitmodel=nls(y ~ a1 + a2/(1+exp(-a3*(t-a4))),
               start = list(a1=mean(y),a2=-sd(y),a3=1,a4=100), trace=PRINTDETAILS, algorithm = "port", lower = c(-1,-Inf,1,20), upper=c(10,0,Inf,200),
               control = nls.control(warnOnly = TRUE))
  end.time <- Sys.time()
  print(end.time-start.time)
  
  params=coef(fitmodel)
  
  wordIdfTuples[rowNum,] = c(kword,unlist(params))

}

write.table(wordIdfTuples,file = outFilePath, sep = ",", row.names = FALSE)
