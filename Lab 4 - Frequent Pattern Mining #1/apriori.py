import itertools


"""
	Run the apriori algorithm

	original_dataset - A list of data points (iterables), each representing a transaction
	min_support - The minimum support required for a transaction

	Returns - A dict with frozensets as keys, and the support for each set as values
"""
def apriori(original_dataset, min_support):
	"""
		Create a copy of the original dataset that we can perform transaction reduction on.
		This is because the last step of the algorithm (that ends up creating 0 candidates), reduces "too much"
	"""
	dataset = original_dataset[:]

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
		next = generate_candidates(L, k)

		next = calculate_supports(next, dataset)
		next = frequent_sets(next, min_support)

		if len(next):
			L = next
			k += 1
		else:
			break

	return calculate_supports(L, original_dataset)
	
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
	l = map(sorted, sets) # Convert sets to sorted lists for consistent iteration order

	candidates = []
	for i in range(0, len(l)):
		for j in range(i + 1, len(l)):
			if l[i][:k - 1] == l[j][:k - 1]: # If the items on i[0] to i[k-1] are equal to j[0] to j[k-1], this is a candidate
				candidate = frozenset(l[i] + l[j][k - 1:]) # Take all elements from i, and the last element from j

				subsets = generate_subsets(candidate)
				for subset in subsets:
					if subset not in sets:
						continue # Candidate has an infrequent subset, throw it away

				candidates.append(candidate)

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

	NOTE -  This function does transaction reduction, that is it removes transaction that are no longer needed (matches no sets). This means,
			that it modifies the passed 'dataset' argument	

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

		# Do transaction reduction. Since this transaction did not match any of the given sets, it will not match any of their supersets either, so we can remove it
		if not match:
			dataset.remove(datapoint)

	return counts
	
# dataset = [
# 	frozenset([ 1, 2, 3, 4, 5 ]), 
# 	frozenset([ 1, 3, 5 ]), 
# 	frozenset([ 2, 3, 5 ]), 
# 	frozenset([ 1, 5 ]), 
# 	frozenset([ 1, 3, 4 ]), 
# 	frozenset([ 2, 3, 5 ]), 
# 	frozenset([ 2, 3, 5 ]),
#     frozenset([ 3, 4, 5 ]), 
#     frozenset([ 4, 5 ]), 
#     frozenset([ 2 ]), 
#     frozenset([ 2, 3 ]), 
#     frozenset([ 2, 3, 4 ]), 
#     frozenset([ 3, 4, 5 ]) 
# ]

dataset = [
	{1,2,5},
	{2,4},
	{2,3},
	{1,2,4},
	{1,3},
	{2,3},
	{1,3},
	{1,2,3,5},
	{1,2,3}
]

print apriori(dataset, 2)

