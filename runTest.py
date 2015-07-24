# runTest.py

# this is the python version of runTest.sh
# made this because its easier do to it in python

import os

rawIdfDir = "/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/testRawIdf/"
currTestRes = "/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/testResults/"

rawIdfFiles = os.listdir(rawIdfDir)
currResultFiles = os.listdir(currTestRes)

for fileName in rawIdfFiles:
	rawIdfFileBase, ext = os.path.splitext(fileName)
	if( ((rawIdfFileBase+"_testResults"+ext) not in currResultFiles) and (fileName.endswith('.csv')) ):
		print(rawIdfFileBase+":")
		os.system("Rscript ./sigmoidFitting/idfSeriesToTuples_Testing.r "+rawIdfFileBase)
		os.system("./modelFitting/supportVecIDF_test.py "+rawIdfFileBase)

 