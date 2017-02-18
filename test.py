# Kari Green
# cngreen
# crawler.py
#----------------------------------------
import sys
import os
import re

from bs4 import BeautifulSoup
import urllib

def find_format(input):
	input = re.sub(r'http://eecs.umich.edu', '', input)
	find = input.split('.')
	test = find[1]

	if len(test) > 3:
		if test[:4] == 'html':
			return True

	return False



def main():
	inputa = 'http://eecs.umich.edu/eecs/etc/people/byalpha.cgi'
	inputb = 'http://eecs.umich.edu/eecs/students/students.html'
	inputc = 'http://eecs.umich.edu/eecs/research/area.html?r_id=2'
	inputd = 'http://eecs.umich.edu/cse/about/by-the-numbers.html#programs'
	inpute = 'http://eecs.umich.edu/eecs/etc/events/showevent.cgi?4215'

	find_format(inputa)
	find_format(inputb)
	find_format(inputc)
	find_format(inputd)
	find_format(inpute)




if __name__ == "__main__": 
	main()