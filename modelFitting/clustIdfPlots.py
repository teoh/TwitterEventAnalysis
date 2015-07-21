#!/usr/bin/python

# clustIdfPlots.py
# this script will cluster the 4 tuples derived from the idf plots into two clusters
# the goal is to see if the contents of the two clusters match our own labels

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans
import csv

def class2Logical(tupleClass):
	if(tupleClass == "TRUE"):
		return 1
	elif (tupleClass == "FALSE"):
		return 0
	else:
		print("Not a valid class!!")
		return -1

def main():

	print("fsdfsdf")

	idfTuples = list()		# ALL of the tuples. gets used for the k means computation
	idfLabels = list()		# ALL of the TRUE/FALSE labels, used when printing the cluster labels vs the true labels
	idfClassTuple = list()	# all of the tuples as in idfTuples, but also with the true labels
	idfWords = list()		# the list of words that the idf tuples are describing 
	rowCount = 0
	colsToGet = [3,4]

	with open("/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/wordIdfTuples.csv",'rb') as csvFile:
		tupleReader = csv.reader(csvFile,delimiter=',')
		next(tupleReader, None)  
		for row in tupleReader:
			rowCount += 1
			# print(row[2])
			idfTuples.append(map(float,[row[i] for i in colsToGet])+[row[2]])
			idfClassTuple.append(map(float,[row[i] for i in colsToGet] )+[class2Logical(row[6])])
			idfWords.append(row[1])
			# print(idfTuples[rowCount-1])
			idfLabels.append(row[6])

	#print(idfClassTuple)

	twoCluster = KMeans(n_clusters = 2)
	twoCluster.fit(idfTuples)
	pred = twoCluster.predict(idfTuples)

	print(pred)

	# pred = twoCluster.labels_
	# for i in range(rowCount):
	# 	print(pred[i],idfLabels[i])
	centers = twoCluster.cluster_centers_
	print(centers)

	# plot the tuples in (a2,a3) space
	tuplesTrue = list()
	tuplesFalse = list()
	wordsTrue = list()
	wordsFalse = list()
	# split the list into event and non event words
	for i in range (rowCount):
		if(idfClassTuple[i][2] == 1):
			tuplesTrue.append(idfClassTuple[i])
			wordsTrue.append(idfWords[i])
		elif(idfClassTuple[i][2] == 0):
			tuplesFalse.append(idfClassTuple[i])
			wordsFalse.append(idfWords[i])
		else:
			print("Not a valid class!!")

	# plot the points coloured according to the manual classification
	fig = plt.figure(1, figsize=(16, 9))
	# redDots, = plt.plot([row[0] for row in tuplesTrue],[row[1] for row in tuplesTrue],'ro')
	# blueDots, = plt.plot([row[0] for row in tuplesFalse],[row[1] for row in tuplesFalse],'bo')
	plt.scatter([row[0] for row in idfTuples ],[row[1] for row in idfTuples ], c=[class2Logical(c) for c in idfLabels], s= 500)
	# plt.scatter([centers[0][0],centers[1][0] ], [centers[0][1],centers[1][1] ], c=[0.5,1], s = [100,200])
	plt.axis([-3,0.1,0,50])
	plt.xlabel("a2 < 0 (vertical dilation)")
	plt.ylabel("a3 > 1 (horizotal dilation)")
	plt.title("a2 a3 feature space: actual classes")

	# plt.annotate(wordsTrue, xy=( [row[0] for row in tuplesTrue],[row[1] for row in tuplesTrue] ), xytext=(-20,20) )
	# for label, x, y in zip( wordsTrue, [row[0] for row in tuplesTrue], [row[1] for row in tuplesTrue] ):
	# 	plt.annotate(label, xy=(x,y),  xytext = (-20, (250*np.absolute(np.sin(20*x)))), textcoords = 'offset points')
	for label, x, y in zip( wordsFalse, [row[0] for row in tuplesFalse], [row[1] for row in tuplesFalse] ):
		plt.annotate(label, xy=(x,y),  xytext = (-20, 30), textcoords = 'offset points')

	# plot the points coloured to the clusters
	fig = plt.figure(2, figsize=(16, 9))
	plt.scatter([row[0] for row in idfTuples ],[row[1] for row in idfTuples ],c=pred, s=500)
	plt.axis([-3,0.1,0,50])
	plt.xlabel("a2 < 0 (vertical dilation)")
	plt.ylabel("a3 > 1 (horizotal dilation)")
	plt.title("a2 a3 feature space: predicted classes")

	#show those plots
	plt.show()


if __name__ == '__main__':
	main()