# Kari Green
# cngreen
# crawler.py
#----------------------------------------
import sys
import os
import re

from bs4 import BeautifulSoup
from collections import deque

import urllib2
import urlparse

def normalize_URL(input, url):
	# normalizes the URL

	if input.startswith('/'): # relative path, joins to url of currently crawled page
		input = urlparse.urljoin(url, input)
		
		if input.endswith('/'): # removes ending /
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

def visit_URL(URLs_to_visit, visited_URLs, URL_count, max_URLs):
	url = URLs_to_visit.popleft() # first URL in queue

	#print "***visiting: ", url #used to see which URL is being crawled in testing

	# attempt to visit the url
	try: r = urllib2.urlopen(url) 
	except: return URL_count # if unsuccessful, don't crawl

	if (r.code == 200): # if successful, crawl it

		r = r.read()

		URL_count += 1 # a URL has been visited
		visited_URLs.append(url)

		#print "to visit: ", len(URLs_to_visit), " visited: ", len(visited_URLs)

		#if (len(URLs_to_visit) + len(visited_URLs)) < max_URLs: 
		# the queue is too short, need to find more URLs to search

		#r = urllib2.urlopen(url).read()
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

def main():

	URL_count = 0
	URL_seed = ''
	visited_URLs = []
	URLs_to_visit = deque()
	
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


	# *** STEP THREE: ----------------------------------------------------------
	#Prepare and print output
	output = ''

	for url in visited_URLs:
		output += url + '\n'

	output_filename = 'crawler.output'

	targetFile = open(output_filename, 'w+')
	targetFile.write(output)




if __name__ == "__main__": 
	main()