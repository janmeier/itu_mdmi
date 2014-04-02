import csv
import math

# Discretization and removal of bogus values
with open('../data_mining_2014_dataset_merged.csv', 'r') as f:
	data = csv.reader(f, delimiter=';')

	headers = data.next()

	final_data = []

	for row in data:
		age = row[0]
		if (age.isdigit()):
			age = int(age)
			if (age <= 20):
				age = 'young'
			elif (age <= 25):
				age = 'slightlyyoung'
			elif (age <= 30):
				age = 'meh'
			else:
				age = 'old'
		else:
			continue

		prog_skill = row[1]
		try:
		 	prog_skill = float(prog_skill)
		except ValueError:
			continue

		uni_years = row[2]
		try:
		 	uni_years = float(uni_years)
		except ValueError:
			continue

		os = row[3].lower()
		if (os.find('windows')):
			os = 'win'
		elif (os.find('mac') or os.find('os')):
			os = 'mac'
		elif (os.find('nix') or os.find('linux') or os.find('ubuntu')) or os.find('debian'):
			os = 'unix'
		else:
			continue

		loves_javascript = row[4].lower().find('javascript') != -1
		row[4] = loves_javascript

		english_skill = row[5]
		try:
		 	english_skill = float(english_skill)
		except ValueError:
			continue

		fav_animal = row[6].lower()
		if fav_animal.find('elephant'):
			fav_animal = 'elephant'
		elif fav_animal.find('zebra'):
			fav_animal = 'zebra'
		elif fav_animal.find('asparagus'):
			fav_animal = 'asparagus'
		else:
			continue

		mountains = row[7].lower()
		if mountains.find('no'):
			mountains = 'no'
		else:
			mountains = 'yes'

		winter = row[8].lower()
		if winter.find('no'):
			winter = 'no'
		else:
			winter = 'yes'

		fav_color = row[13].lower()
		if fav_color.find('green'):
			fav_color = 'green'
		elif fav_color.find('blue'):
			fav_color = 'blue'
		elif fav_color.find('red'):
			fav_color = 'red'
		elif fav_color.find('orange'):
			fav_color = 'orange'
		elif fav_color.find('black'):
			fav_color = 'black'
		elif fav_color.find('yellow'):
			fav_color = 'yellow'
		elif fav_color.find('purple'):
			fav_color = 'purple'
		else:
			fav_color = 'none'

		neural_network = row[14].lower()
		if neural_network != 'yes':
			neural_network = 'no'

		svm = row[15].lower()
		if svm != 'yes':
			svm = 'no'

		sql = row[16].lower()
		if sql != 'yes':
			sql = 'no'

		apriori = row[18].lower()
		if apriori.find('no'):
			apriori = 'no'
		else:
			apriori = 'yes'

		final_data.append([
			age,
			prog_skill,
			# uni_years,
			os,
			# english_skill,
			fav_animal,
			mountains,
			winter,
			neural_network,
			svm,
			apriori,
			sql,
			loves_javascript,
		])

# Normalization
def mean(a):
	return sum(a)/len(a)

def std_dev(a):
	m = mean(a)

	variance = mean(map(lambda x: (x - m)**2, a))
	return math.sqrt(variance)

def column(matrix, i):
    return [row[i] for row in matrix]

def z_score(v, mean, std_dev):
	return (v - mean) / std_dev

for column_to_normalize in [1]:
	col = column(final_data, column_to_normalize)
	m = mean(col)
	s = std_dev(col)

	for i in range(len(final_data)):
		v = final_data[i][column_to_normalize]
		z = z_score(v, m, s)
		final_data[i][column_to_normalize] = str("%.1f" % round(z,1))
		

with open('../data_mining_2014_dataset_clean.csv', 'w') as f2:
	writer = csv.writer(f2, delimiter=';')
	writer.writerow([
		'age',
		'prog_skill',
		# 'uni_years',
		'os',
		# 'english_skill',
		'fav_animal',
		'mountains',
		'winter',
		'neural_network',
		'svm',
		'apriori',
		'sql',
		'loves_javascript',
	])
	writer.writerows(final_data)