# Kari Green
# cngreen
# pagerank.py
#----------------------------------------
import sys
import os
import re

from bs4 import BeautifulSoup
from queue import *
# from sets import *
import urllib


def main():

	URLs = {}

	link_pairs = {}
	
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
		URLs[line] = [0, 0]

	#print (URLs)

	path2 = os.path.join(os.getcwd(), 'URL_pairs.output')
	for line in open(path2):
		line = line.rstrip('\n')
		a = line.split(' ')

		if a[0] not in link_pairs.keys():
			link_pairs[a[0]] = []
		link_pairs[a[0]].append(a[1])

		URLs[a[0]][0] += 1 #out links, source page
		URLs[a[1]][1] += 1 #in links, linked to
	
	#print(lines)

	print (URLs) 
	print(link_pairs['http://eecs.umich.edu'])
	print(URLs['http://eecs.umich.edu'])


	#Prepare and print output --------------------------------------------------------------------
	output = 'i am the output'

	output_filename = 'pagerank.output'

	targetFile = open(output_filename, 'w+')
	targetFile.write(output)



if __name__ == "__main__": 
	main()