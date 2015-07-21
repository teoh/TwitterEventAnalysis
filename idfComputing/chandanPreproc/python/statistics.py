#!/usr/bin/python

import numpy
import matplotlib.pyplot as plt

def print_stats(word_stdev, IDF_HIGH, IDF_LOW):
	total = float(len(word_stdev.keys()))
	print "total words", total

	less4 = len([1 for word in word_stdev.keys() if len(word) <= 4])
	great10 = len([1 for word in word_stdev.keys() if len(word) >= 10])

	highidf = len([1 for idf in word_stdev.values() if idf > IDF_HIGH])
	lowidf = len([1 for idf in word_stdev.values()  if idf < IDF_LOW])

	print "<4: %f"       % (less4/total)
	print ">10: %f"      % (great10/total)
	print "high idf: %f" % (highidf/total)
	print "low idf: %f"  % (lowidf/total)

def plot_stats(word_stdev):
	plt.hist(word_stdev.values(), normed=True, bins=100, histtype='step')
	plt.title("IDF Std-dev histogram")
	plt.xlabel("IDF Std-dev")
	plt.ylabel("Count")
	plt.show()

	