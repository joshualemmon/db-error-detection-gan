import numpy as np
import argparse
from string import ascii_letters
import csv
import random
import pandas as pd

ascii_letters = ascii_letters[:26]

def make_dirty(vals):
	dirty = []
	for v in vals:
		ind = int(np.random.randint(0, len(v)-1))
		if isinstance(v[ind], str):
			if v[ind].isnumeric():
				val = to_numeric(v[ind])
				v[ind] = dirty_numeric(val)
			else:
				v[ind] = dirty_categorical(v[ind])
		else:
			v[ind] = dirty_numeric(v[ind])
		v[-1] = 1
		dirty.append(v)
	return dirty

# Convert numeric string to int or float based on value
def to_numeric(v):
	a = int(v)
	b = float(v)
	if a == b:
		return int(v)
	else:
		return float(v)

# Randomly negate or scale number by factor of 10
def dirty_numeric(val):
	i = np.random.randint(0,3)
	# Negate value
	if i == 0:
		return -1*val
	# Multiply value by 10
	elif i == 1:
		return 10*val
	# Divide value by 10
	elif i == 2:
		return int(val/10)

# Randomly change character, swap characters or insert character
def dirty_categorical(val):
	if len(val) == 0:
		val = random.choice(ascii_letters)
	elif len(val) == 1:
		i = np.random.randint(0,2)
		if i == 0:
			val = random.choice(ascii_letters)
		if i == 1:
			val += random.choice(ascii_letters)
	else:
		i = np.random.randint(0,4)
		val = list(val)
		#change random character in string to random letter
		if i == 0:
			ind = np.random.randint(0,len(val))
			val[ind] = random.choice(ascii_letters)
		# Randomly swap two adjacent characters
		if i == 1:
			ind = np.random.randint(0, len(val)-1)
			c = val[ind]
			val[ind] = val[ind+1]
			val[ind+1] = c
		# Insert random letter into string
		if i == 2:
			ind = np.random.randint(0, len(val))
			val = val[:ind] + [random.choice(ascii_letters)] + val[ind:]
		# Randomly delete character
		if i == 3:
			ind = np.random.randint(0, len(val))
			val = val[:ind] + val[ind:]
		val = "".join(val)
	return val

def main(args):
	infile = args.infile
	out = args.out
	perc = args.percent
	head = args.header
	df = args.dataframe

	if df:
		d = pd.read_csv(infile)
		data = d.values.tolist()
		headers = d.columns.values.tolist()
	else:
		data = [l.rstrip('\n').split(',') for l in open(infile, 'r').readlines()]
		if head:
			headers = data[0]
			data = data[1:]

	split_index = int(len(data)*(perc/100))
	clean = data[:-split_index]
	dirty = data[-split_index:]
	# print(len(clean), len(dirty))
	dirty = make_dirty(dirty)

	with open(out, 'w') as f:
		writer = csv.writer(f, delimiter=',')
		if head:
			writer.writerow(headers)
		writer.writerows(clean)
		writer.writerows(dirty)


if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument('--infile', '-i', type=str, required=True)
	ap.add_argument('--out', '-o', type=str, required=True)
	ap.add_argument('--percent', '-p', type=int, required=True)
	ap.add_argument('--header', '-head', type=bool, default=True)
	ap.add_argument('--dataframe', '-df', type=bool, default=False)
	main(ap.parse_args())