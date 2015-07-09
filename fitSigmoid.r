library(xts)

# lets you show or suppress output that I used in debugging
PRINTDETAILS = TRUE

#four parameter sigmoid function; t stands for "time"
sigmoid = function(params,t){
  a1=params[1]
  a2=params[2]
  a3=params[3]
  a4=params[4]
  sigmoid=a1 + a2/(1+exp(-a3*(t-a4)))
}

setwd('/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/results')
csvFiles<-list.files(pattern=".csv")
csvFiles

# this will define which filescsv files in the director to get
fileNums = matrix(c(1,3,4,5,6,8,9,10,11,13,14,16,17,23,24,26,27,28,29,30,31,33,34,36,37,39,40,44,45,47,48,49,50,52), 
                  nrow=2, 
                  ncol=17)

# fileGroup indexes the events (thus groups of csv files). there are 17 event; thus fileGroup goes from 1 to 17
for(fileGroup in c(1:dim(fileNums)[2])){
  # create the empty plot to put the idf plots on
  plot(0,0,xlab="Minutes Passed",ylab="IDF",xlim = c(0,200),ylim = c(0,6),type = "n")
  
  # gets the (multiple) files specific to a certain event
  filesToRead <- c(fileNums[,fileGroup][1]:fileNums[,fileGroup][2])
  
  # prints the csv files whose idf data we are using
  if(PRINTDETAILS){
    print(filesToRead)
  }
  
  # list of colours so that we can tell the idf plots apart
  cl <- rainbow(length(filesToRead))
  
  # loop all over the key words for that event. i is an index that represents the file to be read
  for(i in c(1:length(filesToRead))){
    
    fileInd=filesToRead[i]
    filename=csvFiles[fileInd]
    if(PRINTDETAILS){
      print(filename)
    }
    # read the data
    data=read.table(paste('/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/results/',filename,sep=""))
    
    # prepare the minutes and the idf values
    t <- c(1:dim(data)[1]) # these are the minutes
    y <- data[,"V6"] # these are the idf values
    
    # plot the idf values for the word versus the minutes. we have not smoothed the points, 
    # but the code is below in case you would like to smooth the points
#     smaIdfs_raw <- TTR::SMA(y,15) # 15 is the number of points you average over in the moving average
#     smaIdf <- smaIdfs_raw
#     smaIdf[is.na(smaIdfs_raw)] <- y[is.na(smaIdfs_raw)] # for the NA values in the start of the array (nature of moving average) are replaced with their original idf values 
    points(t,y,type="p",col=cl[i]) 

    # so that you can tell which key word matches which idf plot
    legend("topright",col=cl,csvFiles[filesToRead],cex=.75,lty=c(1,1))
    if(PRINTDETAILS){
      print("---")  
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
    
    # plot the fitted curve
    params=coef(fitmodel)
    y2=sigmoid(params,t)
    lines(t,y2,type="l")
    
    if(PRINTDETAILS){
      print(params)  
    }
  }
}