import sys
import csv
import pydot
import random
from math import log

class Node(object):
	class_counter = {}
	def __init__(self):
		self.attribute = 'EMPTY' # The name of the attribute this node discriminates on, or the value of the target attribute if this is a leaf node
		self.attribute_id = -1 # The index of the attribute this node discriminates on
		self.children = [] ## A list of tuples, of val (the value of the attribute that the node discriminates on) and child, and Node, representing the nexxt decision in the tree
		self.isLeaf = False

	def toPNG(self):
		graph = pydot.Dot(graph_type='graph')

		self.attach_childnodes(graph, None, None)

		graph.write_dot('out.dot')
		graph.write_png('out.png')


	def attach_childnodes(self, graph, val, parent):
		if not self.isLeaf:
			if (self.attribute not in self.class_counter):
				self.class_counter[self.attribute] = 0

			Node.class_counter[self.attribute] += 1
		else:
			Node.class_counter[self.attribute] = ''


		attribute = '"' + self.attribute + str(Node.class_counter[self.attribute]) + '"' #makes pydot happy
		this = pydot.Node(attribute)
		graph.add_node(this)

		if parent != None:
			graph.add_edge(pydot.Edge(this, parent, label=val))
 
		for (val, child) in self.children:
			child.attach_childnodes(graph, val, this)

	def __repr__(self):
		return self.attribute + str(self.children)

class Row(object):
	def __init__(self, label, attributes):
		self.label = label ## The value of the target attribute
		self.attributes = attributes ## The value of all attributes

	


"""
Run the id3 algorithm

Rows is a list of tuples
attribute_list is a list of tuples, representing the attributes that can still be used in the tree. Each tuple contains attribute id and attribute name


Returns the root node of the decision tree
"""
def id3(rows, attribute_list, target_attribute_index):
	n = Node()

	split = split_by_value(rows, target_attribute_index)
	num_rows = len(rows)

	label = rows[0].label
	if (all(item.label == label for item in rows)):
		## All rows have the same value for the target attribute. No need to recurse, so we create a leaf node with label 
		n.attribute = label
		n.isLeaf = True
		return n
	
	if len(attribute_list) == 0:
		## Not all rows have the same value, but we don't have any attributes to split on so we return the label with most values for the target attribute among the remaining rows
		count = 0
		label = ''

		for val in split:
			lenght = len(split[val])
			if lenght > count:
				count = lenght
				label = val

		n.attribute = val
		n.isLeaf = True
		return n 

	# Calculate the current entropy
	ent = entrophy(split, num_rows)

	gain = -1
	attribute_id = -1
	attribute_name = ''
	attribute_splits = []

	## Find the attribute that gives that largest gain
	for (attr_id, attr_name) in attribute_list:
		attr_splits = split_by_value(rows, attr_id)
		attr_gain = ent - info_needed(attr_splits, num_rows)

		if attr_gain > gain:
			gain  = attr_gain
			attribute_id = attr_id
			attribute_name = attr_name
			attribute_splits = attr_splits


	if gain == 0:
		## None of the remaninig attributes give any information gain, so we pick the majority class
		count = 0
		label = ''

		for val in split:
			lenght = len(split[val])
			if lenght > count:
				count = lenght
				label = val

		n.attribute = val
		n.isLeaf = True
		return n 

	## Split by that
	n.attribute = attribute_name
	n.attribute_id = attribute_id

	## Remove the attribute we are splitting by from the list
	attribute_list = filter(lambda item: item[0] != attribute_id, attribute_list)
	for val in attribute_splits:
		child = id3(attribute_splits[val], attribute_list, target_attribute_index)
		n.children.append((val, child))

	return n

"""
Split a list of rows (which are themselves lists) by the value of the attribute at index i

Returns a dict keyed by the values of attribute i, each key containing a list of tubles which have the value of key in attribute i

rows - A list of lists
i - The index of the attribute to split on
"""
def split_by_value(rows, i):
	ret = {}

	for row in rows:
		val = row.attributes[i]
		if val in ret:
			ret[val].append(row)
		else:
			ret[val] = [row]


	return ret


# Info(D)
def entrophy(classes, num_rows):
	sum = 0
	for klass in classes:
		p = len(classes[klass]) / float(num_rows)
		sum = sum - p * log(p, 2)

	return sum

# Info_a(D)
def info_needed(splits, num_rows):
	sum = 0.0
	for val in splits:
		rows = splits[val]
		
		target_split = split_by_value(rows, target_idx)

		sum = sum + float(len(rows)) / float(num_rows) * entrophy(target_split, len(rows))
	
	return sum

def classify(classifier, sample):
	if len(classifier.children) > 0:
		val = sample.attributes[classifier.attribute_id]
		for child_val, child in classifier.children:
			if val == child_val:
				return classify(child, sample)
	else:
		return classifier.attribute
	

rows = []
attribute_list = [] 
with open(sys.argv[1], 'r') as f:
	data = csv.reader(f, delimiter=';')

	headers = data.next()
	target_idx = len(headers) - 1 ## Loves javascript is always the last attribute

	i = 0
	for header in headers:
		if (i != target_idx):
			attribute_list.append((i, header))
		i = i+1

	for row in data:
		rows.append(Row(row[target_idx], row))

## Shuffle rows before splitting them into training and test sets
random.shuffle(rows)

split = int(len(rows) / 5)
training_set = rows[:split]
test_set = rows[split:]

classifier = id3(training_set, attribute_list, target_idx)
classifier.toPNG()

tp = tn = fp = fn = 0
for test_data in test_set:
	actual_class = test_data.label
	predicted_class = classify(classifier, test_data)

	if actual_class == 'True':
		if predicted_class == 'True':
			tp += 1
		else:
			fn += 1
	else:
		if predicted_class == 'True':
			fp += 1
		else:
			tn += 1

print "Total: ", len(rows)
print "Training data: ", len (training_set)
print "Test data: ", len(test_set)
print "TP: ", tp
print "FP: ", fp
print "TN: ", tn
print "FN: ", fn
print "Precision: ", (float(tp)/(tp + fp))
print "Recall: ", (float(tp)/(tp + fn))