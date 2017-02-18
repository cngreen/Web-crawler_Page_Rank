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
	
	try: 
		URL_file = str(sys.argv[1])
		convergence = float(sys.argv[2])
	except:
		sys.exit("ERROR: input format not correct, expecting: \n [URL_file] [convergence threshold]")


	# *** STEP ONE: ----------------------------------------------------------
	# open the file containing the URLs
	path = os.path.join(os.getcwd(), URL_file)

	for line in open(path):
		print(URL)


	#Prepare and print output --------------------------------------------------------------------
	output = 'i am the output'

	output_filename = 'pagerank.output'

	targetFile = open(output_filename, 'w+')
	targetFile.write(output)



if __name__ == "__main__": 
	main()