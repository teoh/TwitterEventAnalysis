# getCooccurr.py

# takes in a list of keywords found by the sigmoid event detection and find the top co occurring words for each word in the list

import numpy
import sys
sys.path.append("/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/idfComputing/chandanPreproc/python/")
import stddev

TOP_N_COOC = 5

