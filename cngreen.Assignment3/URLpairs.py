# Kari Green
# cngreen
# URLpairs.py
#----------------------------------------

# This file is used to generate an output file called URL_pairs.output
# This output file creates a map of the links within the 2000 links collected in crawler.py


import sys
import os
import re

from bs4 import BeautifulSoup

from sets import Set

import urllib2
import urlparse

def normalize_URL(input, url):
	# normalizes the URL

	if input.startswith('/'): # relative path, joins to url of currently crawled page
		input = urlparse.urljoin(url, input)
		if input.endswith('/'):
			input = input[:-1]
		input = input.lower()
		return input

	input = re.sub(r'http://', '', input)
	input = re.sub(r'https://', '', input)
	input = re.sub(r'www.', '', input) # removes www.

	if input.endswith('/'): # removes ending /
		input = input[:-1]

	input = "http://" + input # http:// and https:// => http://

	input = input.lower()
 
	if '#' in input: # removes # parameters
		x = input.split('#')
		input = x[0]

	return input

def html_format(input):
	# tests if the link is .html format
	input = re.sub(r'http://eecs.umich.edu', '', input)
	find = input.split('.')

	if find is not None and len(find) >= 2: 
		test = find[1]

		if len(test) > 3:
			if test[:4] == 'html':
				return True

		return False # has an extension, is not html

	return True # has no extension, normal link


def identify_URL_pairs(url, visited_URLs, outputURLs):
	# print (url) used to see which URL is visited in testing
	r = urllib2.urlopen(url) 

	if (r.code == 200): # if successful, crawl it

		r = r.read()
		soup = BeautifulSoup(r, "html.parser")

		for link in soup.find_all('a'):
			next_url = link.get('href')
			if next_url is not None:
				if next_url.startswith('/') or "eecs.umich.edu" in next_url:
					# either a relative path or in the eecs.umich.edu domain
					next_url = normalize_URL(next_url, url)

					if next_url in visited_URLs: 
					# only want to create mappings between URLs that are in the 2000
						if next_url != url: # no self links
							if next_url not in outputURLs: # no multiple links
								outputURLs.add(next_url)


def main():

	visited_URLs = []

	try: 
		crawler_output_file = str(sys.argv[1])
	except:
		sys.exit("ERROR: input format not correct, expecting: \n [crawler_output_file]")


	# *** STEP ONE: ----------------------------------------------------------
	# open the file containing the URLs
	path = os.path.join(os.getcwd(), crawler_output_file)

	for line in open(path):
		line = line.rstrip('\n')
		visited_URLs.append(line)


	# PREPARE AND PRINT URL PAIRS:
	output_filename = 'URL_pairs.output'
	# this is a file that contains URL source and URL pairs
	# the file is formatted such that each line has a pair, separated by a space
	# [URL source] [URL]
	output = ''

	i = 0
	for url in visited_URLs:
		print (i) # used to visualize progress
		i += 1
		outputURLs = Set()
		identify_URL_pairs(url, visited_URLs, outputURLs) 

		for o in outputURLs: # contains the URLs that a page links to
			output += url + ' ' + o + '\n'
			#print url + ' ' + o 

	targetFile = open(output_filename, 'w+')
	targetFile.write(output)




if __name__ == "__main__": 
	main()