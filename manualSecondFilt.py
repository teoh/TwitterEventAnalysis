# manualSecondFilt.py

# i disabled the second filter when generating the idf series of the words. this is to correct that unwise decision

import numpy
import csv
import os

# firstFiltDir = "/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/testRawIdf/firstFilter/"
firstFiltDir = "/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/idfComputing/chandanPreproc/python/out/"
seconFiltDir = "/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/testRawIdf/"

inFileList = os.listdir(firstFiltDir)
outFileList = os.listdir(seconFiltDir)

print(inFileList)

# go over all of the first filter files
for inFileName in inFileList:
	if inFileName not in outFileList:
		print(inFileName)
		# parse the first filter file
		inFileBase, inFileExt = os.path.splitext(inFileName)
		with open(firstFiltDir+inFileBase+".csv",'rb') as inCsvFile:
			tupleReader = csv.reader(inCsvFile,delimiter=',')
			# next(tupleReader, None) 
			# open the out file
			with open(seconFiltDir+inFileBase+'.csv','wb') as outCsvFile:
				tupleWriter = csv.writer(outCsvFile,delimiter=',')
				# each row in the infile needs to be checked
				for row in tupleReader:
					idfs = row[1:len(row)]
					if(numpy.std( map(float,[el for el in idfs]) ) >= 0.5):
						tupleWriter.writerow(row)
			outCsvFile.close()
		inCsvFile.close()



