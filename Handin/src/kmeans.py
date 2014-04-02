import csv
import math
import random
import sys
from collections import Counter

class Centroid(object):
	def __init__(self, point):
		self.point = point
		self.points = []

	def __repr__(self):
		return "I am a centroid at: " + str(self.point) + ", my points are: " + str(self.points)

def kmeans(points, k):
	centroids = random.sample(points, k)
	for i in range(0, len(centroids)):
		centroids[i] = Centroid(centroids[i])

	while True:
		assign(points, centroids)

		new_centroids = []
		for old_centroid in centroids:
			new_centroid = Centroid(mean(old_centroid))
			new_centroids.append(new_centroid)

		match = True
		for new_centroid in new_centroids:
			if len(filter(lambda x: x.point == new_centroid.point, centroids)) == 0:
				match = False
				break

		if match:
			return centroids
		else:
			centroids = new_centroids
	
"""
	Calculate the mean or mode for each feature
"""
def mean(centroid):
	if len(centroid.points):
		no_attributes = len(centroid.points[0])
		no_points = len(centroid.points)
		result = [None]*no_attributes

		for i in range(no_attributes):
			feature_vector = column(centroid.points, i)

			if isinstance(feature_vector[0], float) or isinstance(feature_vector[0], int): 
				# The above check could perhaps be changed to a global vector that stores the type of every feature (numerical, nominal etc.) instead of doing type introspection each time
				result[i] = sum(feature_vector) / no_points
			else:
				# The most common attribute (the mode)
				c = Counter(feature_vector)
				result[i] = c.most_common(1)[0][0]

		return result
	else:
		return centroid.point ## The cluster is empty

"""
	Return the column at position i in the matrix (which is actually a list of lists)
	Eg:

	2	4
	5	3

	Column 0 would return the list 2,5 while 1 would return 4,3
"""
def column(matrix, i):
    return [row[i] for row in matrix]

"""
	Assign the points in points to the closest centroid
"""
def assign(points, centroids):
	for point in points:
		closest_centroid = None
		min_distance 	 = sys.maxint

		for centroid in centroids:
			d = distance(point, centroid.point)

			if d < min_distance:
				min_distance 	 = d
				closest_centroid = centroid

		closest_centroid.points.append(point)

"""
	Calculate the distance between two points
"""
def distance(p1, p2):
	dist = 0
	for i in range(0, len(p1) - 1):
		t = type(p1[i])
		if t is float or t is int:
			dist = math.sqrt(math.pow((p1[i] - p2[i]), 2))
		else:
			if p1[i] != p2[i]:
				dist += 1

	return dist

rows = []
with open(sys.argv[1], 'r') as f:
	data = csv.reader(f, delimiter=',')
	
	headers = data.next()
	for line in data:
		for i, col in enumerate(line):
			try:
				line[i] = float(col)
			except ValueError:
				pass

		rows.append(line)


for k in range(1, 31):
	centroids = kmeans(rows, k)

	variance = 0
	for centroid in centroids:
		cluster_variance = 0
		for p1 in centroid.points:
			for p2 in centroid.points:
				cluster_variance += distance(p1, p2)**2

		if len(centroid.points) != 0:
			variance += cluster_variance / len(centroid.points)

	print k, '\t',  variance