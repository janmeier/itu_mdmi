import itertools
import sys
import csv

"""
	Run the apriori algorithm

	dataset - A list of data points (iterables), each representing a transaction
	min_support - The minimum support required for a transaction

	Returns - A dict with frozensets as keys, and the support for each set as values
"""
def apriori(dataset, min_support):
	# Find the frequent 1 item sets (the frequency of each item)
	L = {}
	for datapoint in dataset:
		for item in datapoint:
			item = frozenset([item])
			if item in L:
				L[item] += 1
			else:
				L[item] = 1

	k = 1
	L = frequent_sets(L, min_support)

	while True:
		candidates = generate_candidates(L, k)

		next = calculate_supports(candidates, dataset)
		next = frequent_sets(next, min_support)

		if len(next): # If any candidates with support >= min_support remain
			L = next
			k += 1
		else:
			break

	return calculate_supports(L, dataset)
	
"""
	Generate all len-1 subsets of s
"""
def generate_subsets(s):
	return itertools.combinations(s, len(s)-1)

"""
	Generate candiates, based on a list of frozen sets (item sets), and a k (for convenience, k could also be
	calculated from the input, since it is the length of each set in 'sets')
"""
def generate_candidates(sets, k):
	candidates = set()
	for i in range(0, len(sets)):
		for j in range(i + 1, len(sets)):
			one = sets[i]
			two = sets[j]

			candidate = one.union(two)
			if len(candidate) == k +1:
				subsets = generate_subsets(candidate)
				for subset in subsets:
					if subset not in sets:
						continue # Candidate has an infrequent subset, throw it away

				candidate = frozenset(candidate)
				candidates.add(candidate)

	return candidates

"""
	Return the sets from frequencies that are frequent (>= the threshold)

	frequencies - A dict with frozen sets as keys, and their frequencies as values
	threshold - An int representing the threshold (min supports)

	Returns - a list of frozen sets that are at or above the threshold
"""
def frequent_sets(frequencies, threshold):
	return [k for k, v in frequencies.iteritems() if v >= threshold]

"""
	Calculate the support for each set in the list.

	sets - A list of sets
	dataset - The dataset of transactions

	Returns a dict with sets as keys, and their frequencies as values
"""
def calculate_supports(sets, dataset):
	counts = {s: 0 for s in sets}
	for datapoint in dataset:
		match = False
		for s in sets:
			if s.issubset(datapoint):
				counts[s] += 1
				match = True

	return counts
	
dataset = []

with open(sys.argv[1], 'r') as f:
	data = csv.reader(f, delimiter=',')

	for row in data:
		dataset.append(set(row))

print apriori(dataset, int(sys.argv[2]))
