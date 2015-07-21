#!/usr/bin/python

import csv

def csv_to_dict(fname):
	with open(fname, "r") as f:
		reader = csv.reader(f)
		return { line[0]: line[1] for line in list(reader) }

def main():
	pass

def write_idf_to_file(word_idf, fname):
	print "Writing IDFs to file: %s ... " %fname ,


	series_length = 180
	header = "word," + ",".join(map(str, range(1, series_length+1)))

	with open(fname, "w") as f:
		# write header
		f.write(header + "\n")

		# write each word
		for word in word_idf:
			f.write(word + "," + ",".join(map(str, word_idf[word])) + "\n")

	print "done"

def write_stddev_to_file(word_stdev, fname):
	print "Writing stddev to file: %s ..." %fname ,

	with open(fname, "w") as f:
		for w, c in word_stdev:
			s = w + ", " + str(c) + "\n"
			s = s.encode("utf8")
			f.write(s)	

	print "done"

if __name__ == '__main__':
	main()