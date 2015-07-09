#!/usr/bin/python

# stddev.py
# chandan yeshwanth

# a twitter event detection technique that 
# uses std dev threshold to remove stopwords and 
# find keywords

import mysql.connector
import datetime
import math
import numpy
import string

# this will connect to the database, returning cnx and cursor objects that will be used later
def init_db():
	cnx = mysql.connector.connect(user='root', password='internship',
                              host='127.0.0.1',
                              database='twitter')

	cursor = cnx.cursor()

	return cnx, cursor

def get_data_by_event(cursor, event_name):
	# query = "select TIME(creation_date), GROUP_CONCAT(content SEPARATOR ' ') from tweet where creation_date between '{0}' and '{1}' limit 10"
	query = "select id, creation_date, content from {0}"

	query = query.format(event_name)

	cursor.execute(query)

	return cursor

def get_num_table_rows(cursor, event_name):
	query = "select count(*) from {0}"
	query = query.format(event_name)
	cursor.execute(query)
	count_of_row = cursor.fetchone()
	return count_of_row[0]


def main():
	print "hello hello"
	cnx, cursor = init_db()
	event_name = raw_input("Name of the event: ")
	num_rows=get_num_table_rows(cursor,event_name)
	print num_rows

	print "Getting data from %s..." % event_name
	cursor = get_data_by_event(cursor,event_name)

	print string.punctuation
	print "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~" 

	tweet_list = [None]*num_rows

	print len(tweet_list)


	i = 0
	progressFract = ""
	print "Processed " + progressFract
	for (id, date, tweet) in cursor:
		punct_dict={ord(c): None for c in string.punctuation}
		# print tweet
		#print tweet.replace("'","")
		# print tweet.replace("'","").translate(punct_dict).split() 
		t = tuple([id, date, tweet.replace("'","").translate(punct_dict).split()]) # doesn't filter out emoji but oh well
		# print t
		tweet_list[i] = t
		i+=1
		if i >= num_rows:
			print "Error: list index has exceeded the number of rows!!"
		prevProg = progressFract
		progressFract = "{0}/{1}".format(i,num_rows)
		backspaceBlock = "\b"*len(prevProg)
		print backspaceBlock
		print backspaceBlock+progressFract


	# print tweet_list	


if __name__ == '__main__':
	main()