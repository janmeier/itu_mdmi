import csv
import sys
import re

from datetime import datetime
import parsedatetime.parsedatetime as pdt

from time import mktime
from datetime import datetime

with open(sys.argv[1], 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=';', quotechar=None)
	headers = reader.next()

	column = {}
	for h in headers:
		if len(h):
			column[h] = []

	for row in reader:
		for h, v in zip(headers, row):
			if len(h):
				column[h].append(v)

parsed = {}

hasCharacters = re.compile('[a-zA-Z]')
toSlash = re.compile('(\ |\.|-)+')

cal = pdt.Calendar()
parsed['DOB'] = []
for date in column['DOB']:
	if (hasCharacters.search(date)):
		try:
			parsed['DOB'].append(mktime(cal.parseDateText(date)))
		except KeyError:
			# print "problem parsing ", date, "as datetext"
			parsed['DOB'].append(None)
	else:
		date = toSlash.sub('/', date)
		try:
			parsed['DOB'].append(mktime(cal.parseDate(date)))
		except ValueError:
			# print "problem parsing ", date, "as date"
			parsed['DOB'].append(None)

	print date
	print parsed['DOB'][-1]
	print "\n"

parsed['age'] = []
for age in column['age']:
	if age:
		parsed['age'].append(int(age))
	else:
		parsed['age'].append(None)

print parsed