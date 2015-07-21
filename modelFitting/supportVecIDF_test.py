#!/usr/bin/python

# supportVecIDF_test.py
# this script will test the svm model given by supportVecIDF_observeBound

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing
from sklearn import svm, datasets
import csv
from sklearn.externals import joblib
import sys

def class2Logical(tupleClass):
	if(tupleClass == "TRUE"):
		return 1
	elif (tupleClass == "FALSE"):
		return 0
	else:
		print("Not a valid class!!")
		return -1


def main():
	eventName = sys.argv[1]

	svc = joblib.load('/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/modelInfo/svIdfModel.pkl')

	idfTuples = list()		# ALL of the tuples. gets used for the support vector computation
	idfWords = list()		# the list of words that the idf tuples are describing 
	colsToGet = [1,2,3]		# this has the a1, a2, and a3 parameters


	# read the file
	with open("/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/testDat/"+eventName+"_tuples.csv",'rb') as inCsvFile:
		tupleReader = csv.reader(inCsvFile,delimiter=',')
		next(tupleReader, None)  
		for row in tupleReader:
			idfTuples.append(map(float,[row[i] for i in colsToGet])	)
			idfWords.append(row[0])
	idfTuples = np.array(idfTuples)

	pred = svc.predict(idfTuples)

	print(pred)
	print(pred.shape[0])
	print(idfTuples.shape[0])

	if(pred.shape[0] != idfTuples.shape[0]):
		print("Problem with array sizes!!!")

	print("Writing discovered words to file...")

	with open('testResults/'+eventName+'_testResults.csv','wb') as outCsvFile:
		testResWriter = csv.writer(outCsvFile, delimiter='	')
		for rowNum in range(pred.shape[0]):
			if(pred[rowNum]):
				testResWriter.writerow([idfWords[rowNum], idfTuples[rowNum,0], idfTuples[rowNum,1], idfTuples[rowNum,2], pred[rowNum]])

	print("Done!")

if __name__ == '__main__':
	main()