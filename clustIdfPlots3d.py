#!/usr/bin/python

# clustIdfPlots3d.py
# this script will cluster the 4 tuples derived from the idf plots into two clusters
# the goal is to see if the contents of the two clusters match our own labels
# same idea as clustIdfPlots.py but this does the k means in 3d, so allowing one extra parameter 

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans
import csv