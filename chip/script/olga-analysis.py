import yaml
#import homer
import sys
import argparse
import os
import glob
import shutil
import datetime
import re
#import metaseq


def subset(dataset, type):
	selected = []
	for i in dataset:
		if type in i['type']: 
			selected.append(i)
	return selected

def process_data(dataMap):
	#print dataMap
	dataset = dataMap["chip-seq"]#.get("num_cores")	
	
	#get the datasets
	H3K4me3 = subset(dataset, 'H3K4me3')
	H3K4me1 = subset(dataset, 'H3K4me1')
	Pbx1 = subset(dataset, 'Pbx1')
	HDAC2 = subset(dataset, 'HDAC2')
	
	# 1. use HOMER to 
	# a)define peaks
	# http://biowhat.ucsd.edu/homer/ngs/peaks.html
	# b) Motif analysis (findMotifsGenome.pl)
	# c) Annotation of Peaks (annotatePeaks.pl)
	# for all four factors
	
	# 2. overlay the effect of knockout of Pbx1 with H3K4me1, H3K4me3 and HDAC2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='analyze chipseq dataset from Olga')
    parser.add_argument('-d', dest='data', help='data file', default = 'data.yaml')
    options = parser.parse_args()
    with open(options.data) as in_handle:
    	dataMap = yaml.safe_load(in_handle)
    	in_handle.close()
    process_data(dataMap)
#    process_sample(options.source, options.dest, options.exome_target)

