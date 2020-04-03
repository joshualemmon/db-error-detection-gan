from xml.etree import ElementTree
import os
import csv
import argparse
import numpy as np


def get_xml_vals(infile):
	tree = ElementTree.parse(infile)
	root = tree.getroot()
	item = ""
	attr = []
	# Get attribute names
	for r in root:
		item = r.tag
		for c in r:
			attr.append(c.tag)
	attr = set(attr)

	# Get attribute values for each item
	vals = []
	for p in list(root):
		v = []
		for a in attr:
			v.append(p.find(a).text)
		vals.append(v)

	return vals

def add_attributes(xml_data):
	data = []
	# Load possible interests and countries
	interests = [i.rstrip('\n') for i in open('interests.txt', 'r').readlines()]
	countries = [c.rstrip('\n') for c in open('countries.txt', 'r').readlines()]
	# Generate random valid values for each tuple
	for x in xml_data:
		x.append(gen_age())
		x.append(gen_salary())
		x.append(gen_height())
		x.append(gen_interest(interests))
		x.append(gen_country(countries))
		x.append(0)
		data.append(x)
	return data

def gen_age(mean=30, std=15, max_age=120, min_age=18):
	age = int(np.random.normal(mean, std, 1))
	if age < min_age:
		return min_age
	elif age > max_age:
		return max_age
	else:
		return age

def gen_salary(mean=50000, std=10000, max_sal=100000, min_sal=20000):
	sal = int(np.random.normal(mean, std, 1))
	if sal < min_sal:
		return min_sal
	elif sal > max_sal:
		return max_sal
	else:
		return sal

def gen_height(mean=168, std=10, max_height=200, min_height=155):
	height = int(np.random.normal(mean, std, 1))
	if height < min_height:
		return min_height
	elif height > max_height:
		return max_height
	else:
		return height

def gen_interest(ints):
	return ints[np.random.randint(low=0, high=len(ints))]

def gen_country(countries):
	return countries[np.random.randint(low=0, high=len(countries))]

def main(args):
	infile = args.infile
	out = args.out

	# Read XML data
	xml_data = get_xml_vals(infile)

	full_data = add_attributes(xml_data)

	with open(out, 'w') as f:
		writer = csv.writer(f, delimiter=',')
		# f_name, l_name, email, age, salary, height, interest, country, clean/dirty
		writer.writerow(['l_name', 'email', 'f_name', 'age', 'salary', 'height', 'interest', 'country', 'is_dirty'])
		writer.writerows(full_data)

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument('--infile', '-i', type=str, required=True)
	ap.add_argument('--out', '-o', type=str, required=True)

	main(ap.parse_args())