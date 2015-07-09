library(xts)

# sigmoid = function(params,t){
#   A=params[1];
#   K=params[2];
#   B=params[3];
#   nu=params[4];
#   Q=params[5];
#   M=params[6];
#   sigmoid=A + (K-A)/(1+Q*exp(-B*(t-M)))^(1/nu)
# }

sigmoid = function(params,t){
  a1=params[1]
  a2=params[2]
  a3=params[3]
  a4=params[4]
  
  sigmoid=a1 + a2/(1+exp(-a3*(t-a4)))
}

# sigmoid = function(params,t){
#   a1=params[1]
#   a2=params[2]
#   a4=params[3]
#   
#   sigmoid=a1 + a2/(1+exp(-(t-a4)))
# }

# hyptang = function(params,t){
#   a1=params[1]
#   a2=params[2]
#   a3=params[3]
#   a4=params[4]
#   
#   hyptang=a1+a2*tanh(a3*(t-a4))
# }


setwd('/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/results')
csvFiles<-list.files(pattern=".csv")
csvFiles

# this will define which filescsv files in the director to get
fileNums = matrix(c(1,3,4,5,6,8,9,10,11,13,14,16,17,23,24,26,27,28,29,30,31,33,34,36,37,39,40,44,45,47,48,49,50,52), 
                  nrow=2, 
                  ncol=17)

fileGroup = 17
#for(fileGroup in c(1:dim(fileNums)[2])){
  
  # create the empty plot to put the idf plots on
  plot(0,0,xlab="Minutes Passed",ylab="IDF",xlim = c(0,200),ylim = c(0,6),type = "n")
  # gets the (multiple) files specific to a certain event
  filesToRead <- c(fileNums[,fileGroup][1]:fileNums[,fileGroup][2])
  
  print(filesToRead)
  
  # list of colours so that we can tell the idf plots apart
  cl <- rainbow(length(filesToRead))
  
  #===============================
   i = 4 # 2 is good, 3 is bad
  
  # loop all over the key words for that event. i is an index that represents the file to be read
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
    points(mins,idfs,type="p",col=cl[i]) #smaIdf or idfs
  
  
    legend("topright",col=cl,csvFiles[filesToRead],cex=.75,lty=c(1,1))
    print("---")
    
    y=idfs#smaIdf or idfs
    t=mins
    # fitmodel=nls(y ~ A + (K-A)/(1+Q*exp(-B*(t-M)))^(1/nu), 
    #              start=list(A=1,K=1,B=1,nu=1,Q=1,M=1))
    start.time <- Sys.time()
    fitmodel=nls(y ~ a1 + a2/(1+exp(-a3*(t-a4))),
                 # start = list(a1=3,a2=-2,a3=1,a4=100), trace=TRUE, algorithm = "port", lower = c(-1,-Inf,0,0), upper=c(10,0,Inf,200),
                 # start = list(a1=1.5,a2=-1.5,a3=1.5,a4=21), trace=TRUE, algorithm = "port", lower = c(-1,-Inf,0,20), upper=c(10,0,Inf,200),
                 start = list(a1=mean(y),a2=-sd(y),a3=1,a4=100), trace=TRUE, algorithm = "port", lower = c(-1,-Inf,1,20), upper=c(10,0,Inf,200),
                 control = nls.control(warnOnly = TRUE))
    end.time <- Sys.time()
    print(end.time-start.time)
    
    # fitmodel=nls(y ~ a1 + a2/(1+exp(-(t-a4))),
    #              start = list(a1=3,a2=-2,a4=100), trace=TRUE)
    # fitmodel=nls(y ~ a1+a2*tanh(a3*(t-a4)),
    #              start = list(a1=3,a2=-1.5,a3=0.5,a4=100) )
    params=coef(fitmodel)
    y2=sigmoid(params,t)
    # y2=hyptang(params,t)
    lines(t,y2,type="l")
    print(params)
  }
#}