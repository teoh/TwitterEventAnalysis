#!/usr/bin/python

# supportVecIDF_observeBound.py
# this script will do the classification of the idf tuples using support vector machines, then plot a mesh to see where the decision boundary lies

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing
from sklearn import svm, datasets
import csv
from sklearn.externals import joblib

def class2Logical(tupleClass):
	if(tupleClass == "TRUE"):
		return 1
	elif (tupleClass == "FALSE"):
		return 0
	else:
		print("Not a valid class!!")
		return -1


def main():

	scaleData = 0

	idfTuples = list()		# ALL of the tuples. gets used for the support vector computation
	idfLabels = list()		# ALL of the TRUE/FALSE labels, used when printing the cluster labels vs the true labels
	colsToGet = [2,3,4]		# this has the a1, a2, and a3 parameters
	rowCount = 0 			# counts the number of observations we have

	# read the file
	with open("/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/modelInfo/wordIdfTuples.csv",'rb') as csvFile:
		tupleReader = csv.reader(csvFile,delimiter=',')
		next(tupleReader, None)  
		for row in tupleReader:
			rowCount += 1
			idfTuples.append(map(float,[row[i] for i in colsToGet])	)
			idfLabels.append(row[6])

	# convert idfTuples into an array (easier to work with) and scale if needed
	idfTuples = np.array(idfTuples)
	if(scaleData):
		idfTuples = preprocessing.scale(idfTuples)
	# convert idfLabels into array
	idfLabels = np.array([class2Logical(c) for c in idfLabels])

	# create a mesh to plot in
	h = 0.3
	x_min, x_max = idfTuples[:, 0].min() - 1, idfTuples[:, 0].max() + 1 	# x is the a1 column
	y_min, y_max = idfTuples[:, 1].min() - 1, idfTuples[:, 1].max() + 1 	# y is the a2 column
	z_min, z_max = idfTuples[:, 2].min() - 1, idfTuples[:, 2].max() + 1 	# z is the a3 column
	xx, yy, zz = np.meshgrid(np.arange(x_min, x_max, 0.5),
	                     np.arange(y_min, y_max, h),
	                     np.arange(z_min,z_max, 5))
	xx = xx.ravel().ravel()
	yy = yy.ravel().ravel()
	zz = zz.ravel().ravel()

	print(zz.shape)
	# print(idfTuples)
	# print(idfLabels)

	# make svm instance
	print("Computing SVM...")
	C = 1.0  # SVM regularization parameter
	svc = svm.SVC(kernel='linear', C=C).fit(idfTuples, idfLabels)
	# print(svc)
	# print(svc.get_params())

	# rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(X, y)
	# poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(X, y)
	# lin_svc = svm.LinearSVC(C=C).fit(X, y)

	# make the prediction for mesh points in the 3D space that we are plotting in. the goal here is to see where the decision boundary is
	fig = plt.figure(1, figsize=(16, 9))
	ax = fig.add_subplot(111,projection='3d')
	pred = svc.predict(np.c_[xx, yy, zz])
	print(pred.shape)
	# ax.scatter(xx, yy, zz, c=pred, alpha=0.8)
	ax.set_xlabel('a1: y-shift')
	ax.set_ylabel('a2: y-stretch')
	ax.set_zlabel('a3: t-compression')
	plt.title('a1 a2 a3 feature space: training data')
	ax.scatter(idfTuples[:,0],idfTuples[:,1],idfTuples[:,2],c=idfLabels,s=200, alpha= 1)
	plt.show()

	# joblib.dump(svc,'/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/modelInfo/svIdfModel.pkl')


if __name__ == '__main__':
	main()