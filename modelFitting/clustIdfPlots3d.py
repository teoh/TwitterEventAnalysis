#!/usr/bin/python

# clustIdfPlots3d.py
# this script will cluster the 4 tuples derived from the idf plots into two clusters
# the goal is to see if the contents of the two clusters match our own labels
# same idea as clustIdfPlots.py but this does the k means in 3d, so allowing one extra parameter 

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans
from sklearn import preprocessing
import csv

def class2Logical(tupleClass):
	if(tupleClass == "TRUE"):
		return 0						# was 1 in the previous 2d version
	elif (tupleClass == "FALSE"):
		return 1 						# was 0 in the previous 2d version
	else:
		print("Not a valid class!!")
		return -1

def main():
	scaleData = 0

	idfTuples = list()		# ALL of the tuples. gets used for the k means computation
	idfLabels = list()		# ALL of the TRUE/FALSE labels, used when printing the cluster labels vs the true labels
	colsToGet = [2,3,4]
	rowCount = 0

	# read the file
	with open("/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/wordIdfTuples.csv",'rb') as csvFile:
		tupleReader = csv.reader(csvFile,delimiter=',')
		next(tupleReader, None)  
		for row in tupleReader:
			rowCount += 1
			idfTuples.append(map(float,[row[i] for i in colsToGet])	)
			idfLabels.append(row[6])

	print("Computing K-means...")
	twoCluster = KMeans(n_clusters = 2)
	# turn idfTuples into an array 
	idfTuples = np.array(idfTuples)
	if(scaleData):
		idfTuples = preprocessing.scale(idfTuples)
	twoCluster.fit(idfTuples)
	pred = twoCluster.predict(idfTuples)

	fig = plt.figure(1, figsize=(16, 9))
	ax = fig.add_subplot(111,projection='3d')
	ax.scatter(idfTuples[:,0],idfTuples[:,1],idfTuples[:,2],c=[class2Logical(c) for c in idfLabels],s=200)
	ax.set_xlabel('a1')
	ax.set_ylabel('a2')
	ax.set_zlabel('a3')
	plt.title('a1 a2 a3 feature space: actual class for each point')

	fig = plt.figure(2, figsize=(16, 9))
	ax = fig.add_subplot(111,projection='3d')
	ax.scatter(idfTuples[:,0],idfTuples[:,1],idfTuples[:,2],c=pred,s=200)
	ax.set_xlabel('a1')
	ax.set_ylabel('a2')
	ax.set_zlabel('a3')
	plt.title('a1 a2 a3 feature space: fitted class for each point')

	plt.show()


if __name__ == '__main__':
	main()