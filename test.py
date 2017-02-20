# Kari Green
# cngreen
# crawler.py
#----------------------------------------
import sys
import os
import re

from bs4 import BeautifulSoup
from queue import *
from sets import *
import urllib
import urlparse

def normalize_URL(input, url):
	if input.startswith('/'): # relative path
		input = urlparse.urljoin(url, input)

	if 'eecs.umich.edu' not in input: # don't need to normalize, won't crawl this
		return input

	input = re.sub(r'http://', '', input)
	input = re.sub(r'https://', '', input)
	input = re.sub(r'www.', '', input)

	if input.endswith('/'):
		input = input[:-1]

	input = "http://" + input

	input.lower()

	if '#' in input:
		x = input.split('#')
		input = x[0]

	return input

def main():

	# inputa = 'eecs.umich.edu/cse/videos/index.html#DLS'
	# normalize_URL(inputa)
	# inputb = 'http://eecs.umich.edu/cse/giving/index.html'
	# normalize_URL(inputb)
	# inputc = 'eecs.umich.edu/cse/about/by-the-numbers.html#programs'
	# normalize_URL(inputc)

	# inputd = 'eecs.umich.edu/ece/'
	# inputd = normalize_URL(inputd)

	#output = urlparse.urljoin(inputd, '/eecs/staff.html')

	test = "http://www.youtube.com"
	x = normalize_URL(test, 'http://eecs.umich.edu')
	print(x)

	output = normalize_URL('/eecs/staff.html', 'http://eecs.umich.edu/ece')
	print (output)

	y = normalize_URL('eecs.umich.edu', '')
	print(y)






if __name__ == "__main__": 
	main()