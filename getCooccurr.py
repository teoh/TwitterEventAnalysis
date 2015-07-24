#!/usr/bin/python
# getCooccurr.py

# takes in a list of keywords found by the sigmoid event detection and find the top co occurring words for each word in the list

import numpy
import sys
sys.path.append("/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/idfComputing/chandanPreproc/python/")
import stddev
import csv
import mysql.connector
import pprint
import os


def toStr(num):
	if(num >= 10):
		return str(num)
	else:
		return '0'+str(num)

def toDate(yyyy,mm,dd,hh,MM):
	return toStr(yyyy)+"-"+toStr(mm)+"-"+toStr(dd)+" "+toStr(hh)+":"+toStr(MM)

# gets the tweets from the specified time period, that contain the keyword (process tweets into keywords first??)
def get_data_count_by_date(cursor, start_date, end_date):
	query = "select count(*) from tweet_en where creation_date between '{0}' and '{1}'"
	query = query.format(start_date, end_date)

	cursor.execute(query)

	return cursor

def get_cooccurs(keywords, startDate, endDate):
	cnx, cursor = stddev.init_db()

	# make set for fast lookup
	keywords = set(keywords)

	cursor = get_data_count_by_date(cursor, startDate, endDate)

	total_rows = cursor.fetchone()[0]

	print "Getting data..."
	cursor = stddev.get_data_by_date(cursor, startDate, endDate)
	print "Got data!"

	results = { word: {} for word in keywords }		

	print "Looping over all the tweets..."
	rows_done = 0
	for (date, tweet) in cursor:
		tweet_words = stddev.get_words_from_text(tweet)
		keywords_found = keywords & tweet_words

		for keyword in keywords_found:
			for word in tweet_words:
				if word in results[keyword]:
					results[keyword][word] += 1
				else:
					results[keyword][word]  = 1
		rows_done += 1
		# print("Finished row ",rows_done,"/",total_rows,"\r")
		sys.stdout.write("\rFinished row %d/%d" % (rows_done,total_rows))
    	sys.stdout.flush()
	print "Finished looping over tweets!"

	return results


def main():
	TOP_N_COOC = 6

	# ==== needs to be specified to get the right file and time period
	kwordDir = "/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/testResults/"
	cooccurr_dir = "/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/coocurrResults/"

	kwordFiles = os.listdir(kwordDir)
	print kwordFiles

	for i in range(6,7):
		fileYear = 2015
		fileMonth = 6
		fileDay = 1
		fileHrSrt = i #1
		fileHrEnd = fileHrSrt+1
		# ====
		#inResultFileName = toStr(fileYear)+"_"+toStr(fileMonth)+"_"+toStr(fileDay)+"_"+toStr(fileHrSrt)+toStr(fileHrEnd)+"_testResults"
		inResultFileName = "mh17_testResults"
		inResultExt = ".csv"

		startDate = toDate(fileYear, fileMonth, fileDay, fileHrSrt - 1, 0)
		endDate = toDate(fileYear, fileMonth, fileDay, fileHrEnd, 0)

		if(inResultFileName+inResultExt in kwordFiles):
			with open(kwordDir+inResultFileName+inResultExt,'rb') as inCsvFile:
				print("File: "+kwordDir+inResultFileName+inResultExt)

				tupleReader = csv.reader(inCsvFile,delimiter='	')

				keywords = [row[0] for row in tupleReader]
				print keywords

				cooccurs = get_cooccurs(keywords, startDate, endDate)

				# select top 5 for each word
				kword_coocurrences = { kw : sorted(cooccurs[kw].iteritems(), 
										reverse=True, 
										key=lambda (w, c) : c)[:TOP_N_COOC]
					for kw in cooccurs }
				kword_coocurrences_str = pprint.pformat(kword_coocurrences)
				outfile = open(cooccurr_dir+inResultFileName+".txt",'w')
				outfile.write(kword_coocurrences_str)
				outfile.close()






if __name__ == '__main__':
	main()