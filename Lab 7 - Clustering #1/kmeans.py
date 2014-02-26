import csv
import math
import random
import sys

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
	Calculate the mean point of points
"""
def mean(centroid):
	if len(centroid.points):
		acc = [0]*len(centroid.points[0])
		for point in centroid.points:
			for i in range(0, len(point) - 1):
				acc[i] += point[i]

		return map(lambda c: c/len(centroid.points), acc)
	else:
		return centroid.point ## The cluster is empty

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
		dist = math.pow((p1[i] - p2[i]), 2)

	return dist

rows = []
with open('iris.csv', 'r') as f:
	data = csv.reader(f, delimiter=',')

	headers = data.next()
	for line in data:
		line = map(float,line[:-1]) + line[len(line)-1:] # Convert all numbers to float, and keep the label
		rows.append(line)

centroids = kmeans(rows, 3)

for centroid in centroids:
	print "Centroid: " + str(centroid.point)
	classes = {
		'Iris-setosa': 0,
		'Iris-versicolor': 0,
		'Iris-virginica': 0
	}
	rows = len(centroid.points)
	for point in centroid.points:
		klass = point[-1]

		classes[klass] += 1

	for (klass, count) in classes.items():
		print klass + ": " + str(float(count) / rows * 100.0) + "%"