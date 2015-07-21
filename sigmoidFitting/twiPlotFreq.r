# takes a csv file and plots the idf vs the data point
library(xts)

setwd('/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/results')
csvFiles<-list.files(pattern=".csv")
csvFiles

# this will define which filescsv files in the director to get
fileNums = matrix(c(1,3,4,5,6,8,9,10,11,13,14,16,17,23,24,26,27,28,29,30,31,33,34,36,37,39,40,44,45,47,48,49,50,52), 
                  nrow=2, 
                  ncol=17)

for (fileGroup in c(1:dim(fileNums)[2])){
  # create the empty plot to put the idf plots on
  plot(0,0,xlab="Minutes Passed",ylab="IDF",xlim = c(0,200),ylim = c(0,6),type = "n")
  # gets the (multiple) files specific to a certain event
  filesToRead <- c(fileNums[,fileGroup][1]:fileNums[,fileGroup][2])

  # list of colours so that we can tell the idf plots apart
  cl <- rainbow(length(filesToRead))
  
  # loop all over the key words for that event. 
  for(i in c(1:length(filesToRead))){
    fileInd=filesToRead[i]
    filename=csvFiles[fileInd]
    print(filename)
    data=read.table(paste('/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/results/',filename,sep=""))
    
    # prepare the minutes and the idf values
    data[,"V7"] <- c(1:dim(data)[1])
    mins <- data[,"V7"]
    idfs <- data[,"V6"] # scale(data[,"V6"])
    
    smaIdfs_raw <- TTR::SMA(idfs,15)
    smaIdf <- smaIdfs_raw
    smaIdf[is.na(smaIdfs_raw)] <- idfs[is.na(smaIdfs_raw)]
    med <- median(smaIdf)
    lines(mins,(smaIdf),type="l",col=cl[i])
  }
  
  legend("topright",col=cl,csvFiles[filesToRead],cex=.75,lty=c(1,1))
  print("---")
  
}



