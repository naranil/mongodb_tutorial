# -*- coding: utf-8 -*-
import os

DATADIR = ""
DATAFILE = "data/beatles-diskography.csv"

def parse_file(datafile):
	data = []
	with open(datafile, "rb") as f:
		header = next(f).split(',')
		for line in f:
			dictionnary = {}
			line_split = line.split(',')
			for i in range(len(header)):
				dictionnary[header[i].strip()] = line_split[i].strip() # strip to remove the white spaces
			
			# add the processed line as a dictionnary
			data.append(dictionnary) 
	return data

def test():
	# test of the csv parsing implementation
	datafile = os.path.join(DATADIR, DATAFILE)
	d = parse_file(datafile)
	firstline = {'Title': 'Please Please Me','Released': '22 March 1963','Label': 'Parlophone(UK)','UK Chart Position': '1', 'US Chart Position': '-', 'BPI Certification': 'Gold', 'RIAA Certification': 'Platinum'}
	tenthline = {'Title': '','Released': '10 July 1964','Label': 'Parlophone(UK)','UK Chart Position': '1', 'US Chart Position': '-', 'BPI Certification': 'Gold', 'RIAA Certification': ''}

	# Check if the parse_file function is working
	assert d[0] == firstline
	assert d[9] == tenthline

# Run the test
test()