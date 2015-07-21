#!/usr/bin/python

import statistics
import stddev
import fileio

# input: event name, start datetime, end datetime
# output: eventname.csv where each row is the word plus its IDF series

# new function
def idf():
	event_name = raw_input("Enter event name: ")
	start_date = raw_input("Enter start date, time (yyyy-mm-dd hh:MM): ")
	end_date = raw_input("Enter finish date, time (yyyy-mm-dd hh:MM): ") 

	print "Start: %s, End: %s, Event: %s" %(start_date, end_date, event_name)

	word_stddev, word_idf = stddev.get_word_IDFcomplete(start_date, end_date, select=True, threshold=0.3)

	# file names
	dir_name = "out/"

	# sd_fname = event_name + "sd" + ".csv"
	idf_fname = event_name + ".csv"

	fileio.write_idf_to_file(word_idf, dir_name + idf_fname)

def main():
	idf()

if __name__ == '__main__':
	main()