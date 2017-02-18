# Kari Green
# cngreen
# pagerank.py
#----------------------------------------
import sys
import os
import re
import operator
import math

from bs4 import BeautifulSoup
from queue import *
# from sets import *
import urllib

def update_page_rank(url, URLs, link_pairs, page_rank):
	d = 0.85

	new_rank = (1 - d)/len(URLs)

	for link in link_pairs[url]:
		if (URLs[link][0] > 0): #outlinks
			new_rank += d * (page_rank[link]/URLs[link][0])

	page_rank[url] = new_rank

	#print "new_rank", new_rank


def main():

	URLs = {}
	link_pairs = {}
	page_rank = {}
	
	try: 
		URL_file = str(sys.argv[1])
		convergence = float(sys.argv[2])
	except:
		sys.exit("ERROR: input format not correct, expecting: \n [URL_file] [convergence threshold]")


	# *** STEP ONE: ----------------------------------------------------------
	# open the file containing the URLs
	path = os.path.join(os.getcwd(), URL_file)

	lines = [line.rstrip('\n') for line in open(path)]
	for line in lines:
		URLs[line] = [0, 0] # [number of out links, number of in links]
		page_rank[line] = 0.25 # initial page rank value, from spec
		link_pairs[line] = [] # will contain a list of all pages that link to this page

	path2 = os.path.join(os.getcwd(), 'URL_pairs.output')
	for line in open(path2):
		line = line.rstrip('\n')
		a = line.split(' ')

		link_pairs[a[1]].append(a[0])

		URLs[a[0]][0] += 1 #out links, source page
		URLs[a[1]][1] += 1 #in links, linked to

	average_diff = 1000000000
	number_iterations = 0
	while math.fabs(average_diff) > convergence:
		
		old_rank = page_rank.copy()

		for url in URLs.keys():
			update_page_rank(url, URLs, link_pairs, page_rank)

		#print(page_rank)

		average_diff = 0.0

		for p in page_rank.keys():
			diff = old_rank[p] - page_rank[p]
			average_diff += diff

		print(average_diff)
		average_diff = average_diff/len(URLs)

		print(average_diff)

		number_iterations += 1

	
	# sorts the page_rank highest to lowest
	sorted_pr = sorted(page_rank.iteritems(), key=operator.itemgetter(1), reverse=True)


	#Prepare and print output --------------------------------------------------------------------
	output = ''

	for s in sorted_pr:
		output += s[0] + ' ' + str(s[1]) + '\n'

	output_filename = 'pagerank.output'

	targetFile = open(output_filename, 'w+')
	targetFile.write(output)



if __name__ == "__main__": 
	main()