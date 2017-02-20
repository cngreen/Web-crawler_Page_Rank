# Kari Green
# cngreen
# crawler.py
#----------------------------------------
import sys
import os
import re

from bs4 import BeautifulSoup
from queue import *
# from sets import *
import urllib
import urlparse

def normalize_URL(input, url):
	if input.startswith('/'): # relative path
		input = urlparse.urljoin(url, input) # join it with the url we are currently searching
		if input.endswith('/'):
			input = input[:-1]
		input.lower()
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

def html_format(input):
	input = re.sub(r'http://eecs.umich.edu', '', input)
	find = input.split('.')

	if find is not None and len(find) >= 2:
		test = find[1]

		if len(test) > 3:
			if test[:4] == 'html':
				return True

		return False # has an extension, is not html

	return True # has no extension, normal link

def visit_URL(URLs_to_visit, visited_URLs, URL_count, max_URLs):
	url = URLs_to_visit.pop(0) # first URL in queue

	#print "***visiting: ", url #used to see which URL is being crawled in testing
	URL_count += 1 # a URL has been visited
	visited_URLs.append(url)

	if (len(URLs_to_visit)) < max_URLs: 
	# the queue is too short, need to find more URLs to search

		r = urllib.urlopen(url).read()
		soup = BeautifulSoup(r, "html.parser")

		for link in soup.find_all('a'):
			next_url = link.get('href')
			if next_url is not None:
				if next_url.startswith('/') or "eecs.umich.edu" in next_url:
					# either a relative path or in the eecs.umich.edu domain
					next_url = normalize_URL(next_url, url)
					
					if html_format(next_url):
						if str(next_url) not in visited_URLs:
							if str(next_url) not in URLs_to_visit:
								URLs_to_visit.append(next_url) # add URL to queue

	return URL_count


def identify_URL_pairs(url, visited_URLs, outputURLs):
	r = urllib.urlopen(url).read()
	soup = BeautifulSoup(r, "html.parser")

	for link in soup.find_all('a'):
		next_url = link.get('href')
		if next_url is not None:
			if next_url.startswith('/') or "eecs.umich.edu" in next_url:
				# either a relative path or in the eecs.umich.edu domain
				next_url = normalize_URL(next_url, url)

				if next_url in visited_URLs:
					if next_url != url:
						if next_url not in outputURLs:
							outputURLs.append(next_url)


def main():

	URL_count = 0
	URL_seed = ''
	visited_URLs = []
	URLs_to_visit = []
	
	try: 
		seed_URL_file = str(sys.argv[1])
		max_URLs = int(sys.argv[2])
	except:
		sys.exit("ERROR: input format not correct, expecting: \n [seed_URL_file] [max_URLs]")


	# *** STEP ONE: ----------------------------------------------------------
	# open the file containing the seed URL
	# the file will only contain one seed
	path = os.path.join(os.getcwd(), seed_URL_file)

	for line in open(path):
		URL_seed = str(line)

	URL_seed = normalize_URL(URL_seed, '')

	# add the seed to the queue of URLs to visit
	URLs_to_visit.append(URL_seed)


	# *** STEP TWO: ----------------------------------------------------------
	# start with http://www.eecs.umich.edu (from URL_seed)

	while len(URLs_to_visit) > 0 and URL_count < max_URLs: 
	# while there are URLs to visit and we haven't visited the max number of URLs
		URL_count = visit_URL(URLs_to_visit, visited_URLs, URL_count, max_URLs) # visit the URL
		print URL_count # used to keep track of progress of the running program

	#print visited_URLs

	#Prepare and print output --------------------------------------------------------------------
	output = ''

	visited_URLs = visited_URLs[:max_URLs]

	for url in visited_URLs:
		output += url + '\n'

	output_filename = 'crawler.output'

	targetFile = open(output_filename, 'w+')
	targetFile.write(output)



	# PREPARE AND PRINT URL PAIRS:
	output_filename2 = 'URL_pairs.output'
	output2 = ''

	i = 0
	for url in visited_URLs:
		print (i)
		i += 1
		outputURLs = []
		identify_URL_pairs(url, visited_URLs, outputURLs)

		for o in outputURLs:
			output2 += url + ' ' + o + '\n'

	targetFile2 = open(output_filename2, 'w+')
	targetFile2.write(output2)




if __name__ == "__main__": 
	main()