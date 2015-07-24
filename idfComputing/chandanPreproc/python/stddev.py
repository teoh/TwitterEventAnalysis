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

import itertools
import string

def get_stopwords(fname):
	with open(fname, 'r') as f:
		return set(map(lambda s : s.strip(), f.readlines()))

# had to make this an absolute path so that other scripts not in the same director as stddev.py could import stddev.py
STOPWORDS = get_stopwords("/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/idfComputing/chandanPreproc/python/stopwords.txt")

# connect to database and return the connection
# and cursor objects
def init_db():
	cnx = mysql.connector.connect(user='root', password='internship',
                              host='127.0.0.1',
                              database='twitter')

	cursor = cnx.cursor()

	return cnx, cursor

# close database connection
def close_db(cnx):
	cnx.close()	

# get tweets in a date,time range
def get_data_by_date(cursor, start_date, end_date):
	query = "select creation_date, content from tweet_en where creation_date between '{0}' and '{1}'"
	query = query.format(start_date, end_date)

	cursor.execute(query)

	return cursor

# IDF formula
def get_idf(total, count):
	return math.log10(float(total)/(count + 1))

def group_tweets_by_time(cursor):
	grouped_tweets = {}

	for (date, tweet) in cursor:
		# remove the second, microsecond parts from the time 
		# time = date.replace(second=0, microsecond=0).time()
		time = date.replace(second=0, microsecond=0)

		if time in grouped_tweets:
			grouped_tweets[time].append(tweet)
		else:
			grouped_tweets[time] = [tweet]

	return grouped_tweets

# args:
# 	tweet text
# return: 
# 	list of distinct words per tweet, punctuation, stopwords removed
def get_words_from_text(text):
	english_chars = set(string.printable)
	trans_table = dict((ord(char), unicode(" ", "utf-8")) for char in string.punctuation)

	text = text.lower()

	# remove punctuation
	text = text.translate(trans_table)
	
	# remove stopwords
	words = [w for w in text.split() if w not in STOPWORDS]

	# remove words with non-english characters
	is_english = lambda word : not set(word) - english_chars
	words = filter(is_english, words)

	# remove small / large words
	words = [w for w in words if len(w) >= 4 and len(w) <= 10]

	# remove duplicates
	return set(words)

# count occurrences of words per minute and find IDF
# 
# args: 
# 	grouped_tweets: dict of {time (minute): [list of tweet strings in this minute]}
# 	tweets_per_minute_dict: dict of {time (minute): total no of tweets in this minute}
# return: 
# 	{word: [list of IDF values]}
def get_word_IDFseries_from_tweets(grouped_tweets, tweets_per_minute_dict):
	print "Finding IDFs"
	word_IDFseries = {}
	
	for time, tweets in grouped_tweets.iteritems():
		word_count_dict = {}
		words = get_words_from_text(" ".join(tweets))

		for word in words:
			if word in word_count_dict:
				word_count_dict[word] += 1
			else:
				word_count_dict[word]  = 1

		# find IDF for each word in this minute
		for word in word_count_dict:
			idf = get_idf(tweets_per_minute_dict[time], word_count_dict[word])

			if word not in word_IDFseries:
				word_IDFseries[word] = [idf]
			else:	
				word_IDFseries[word].append(idf)

	return word_IDFseries

# args:
# 	word_IDFseries: {word: [list of IDF values]}
# return:
# 	{word: stddev of list}
def get_word_stdev_from_IDFseries(word_IDFseries):
	word_stdev = {}

	for word in word_IDFseries:
		word_stdev[word] = numpy.std(word_IDFseries[word])

	return word_stdev

# args:
# 	start and end date, time for tweets in database
# return:
# 	{word: stddev of IDF} for tweets in date range
def get_word_stdev(start_date, end_date):
	cnx, cursor = init_db()

	print "Getting data"
	cursor = get_data_by_date(cursor, start_date, end_date)

	# group tweets by time (minute)
	grouped_tweets = group_tweets_by_time(cursor)
	
	# count tweets per minute
	tweets_per_minute_dict = {
		time : len(tweets) for (time, tweets) in grouped_tweets.iteritems()
	}

	word_IDFseries = get_word_IDFseries_from_tweets(grouped_tweets, tweets_per_minute_dict)		

	print "Unique words: ", len(word_IDFseries)

	# dict for word - std dev of word IDF in this time period
	word_stdev = get_word_stdev_from_IDFseries(word_IDFseries)
	
	close_db(cnx)

	return word_stdev	

# count occurrences of words per minute and find IDF
# 
# args: 
# 	grouped_tweets: dict of {time (minute): [list of tweet strings in this minute]}
# 	tweets_per_minute_dict: dict of {time (minute): total no of tweets in this minute}
# return: 
# 	{time (minute): {word: IDF in this minute}} 
def get_word_IDFcomplete_from_tweets(grouped_tweets, tweets_per_minute_dict, select, threshold, keywords):
	print "Finding IDFs"

	time_word_idf = {}
	word_IDF = {}
	word_IDF_stdev = {}

	for time, tweets in grouped_tweets.iteritems():
		word_count_dict = {}

		# get unique words from each tweet, then join into single list of words
		words = itertools.chain.from_iterable(map(get_words_from_text, tweets))

		# find IDF only for these words
		if keywords:
			words = [w for w in words if w in keywords]

		for word in words:
			if word in word_count_dict:
				word_count_dict[word] += 1
			else:
				word_count_dict[word]  = 1

		word_IDF_dict = {}

		# find IDF for each word in this minute
		for word in word_count_dict:
			idf = get_idf(tweets_per_minute_dict[time], word_count_dict[word])
			word_IDF_dict[word] = idf

			# an IDF series for each word to find the stdev
			# does not contain data points for all time points!
			if word in word_IDF_stdev:
				word_IDF_stdev[word].append(idf)
			else:
				word_IDF_stdev[word] = [idf]
				
		time_word_idf[time] = word_IDF_dict	

	# find the base IDF only once (log (total no of tweets))
	base_IDF = {}

	for time in time_word_idf:
		base_IDF[time] = get_idf(tweets_per_minute_dict[time], 0)

	print "Finding stdevs of %d words" % len(word_IDF_stdev)
	word_stdev = get_word_stdev_from_IDFseries(word_IDF_stdev)

	# pick words to find complete IDF series for 
	# based on IDF stddev
	if select:
		final_word_stdev = { word: word_stdev[word] for word in word_stdev if word_stdev[word] >= threshold }
		print "First filter: ", len(final_word_stdev), " words from ", len(word_stdev)
	else:
		final_word_stdev = word_stdev
		print len(final_word_stdev), " words"

	# empty list for each word
	for word in final_word_stdev:
		word_IDF[word] = []

	# find IDF for each word for each time point
	for word in word_IDF:
		for time in sorted(time_word_idf):
			# word occurred in this time
			if word in time_word_idf[time]:
				# real IDF value
				word_IDF[word].append(time_word_idf[time][word])
			else:
				# default IDF value
				word_IDF[word].append(base_IDF[time])

	# find stdev again for the whole timeseries
	new_word_stdev = get_word_stdev_from_IDFseries(word_IDF)
	# second filtering of words based on stddev of complete time series
	# below is the "second filter". top line enables the seconf filter and the second line disables it
	# final_word_IDF = { word: word_IDF[word] for word in new_word_stdev if new_word_stdev[word] >= 0.5}
	final_word_IDF = word_IDF


	print "Second filter: %d words from %d" %(len(final_word_IDF), len(new_word_stdev))

	return word_stdev, final_word_IDF

def get_word_IDFcomplete(start_date, end_date, select=False, threshold=0.7, keywords=[]):
	cnx, cursor = init_db()

	print "Getting data"
	cursor = get_data_by_date(cursor, start_date, end_date)

	# group tweets by time (minute)
	grouped_tweets = group_tweets_by_time(cursor)
	
	# count tweets per minute
	tweets_per_minute_dict = {
		time : len(tweets) for (time, tweets) in grouped_tweets.iteritems()
	}

	word_stdev, word_IDF = get_word_IDFcomplete_from_tweets(grouped_tweets, tweets_per_minute_dict, select, threshold, keywords)		

	close_db(cnx)

	return word_stdev, word_IDF	

def main():
	pass	

if __name__ == '__main__':
	main()
