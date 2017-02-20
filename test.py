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

def normalize_URL(input):
	input = re.sub(r'http://', '', input)
	input = re.sub(r'https://', '', input)
	input = re.sub(r'www.', '', input)

	if input.startswith('/'):
		input = "eecs.umich.edu" + input

	if input.endswith('/'):
		input = input[:-1]

	input = "http://" + input

	input.lower()

	if '#' in input:
		x = input.split('#')
		input = x[0]

	print input

	return input

def main():

	inputa = 'eecs.umich.edu/cse/videos/index.html#DLS'
	normalize_URL(inputa)
	inputb = 'http://eecs.umich.edu/cse/giving/index.html'
	normalize_URL(inputb)
	inputc = 'eecs.umich.edu/cse/about/by-the-numbers.html#programs'
	normalize_URL(inputc)




if __name__ == "__main__": 
	main()