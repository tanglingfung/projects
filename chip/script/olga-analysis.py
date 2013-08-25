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
sys.path.insert(0, '../../utils/')
import homer


def subset(dataset, type):
	selected = []
	for i in dataset:
		if type in i['type']: 
			selected.append(i)
	return selected

def process_data(dataMap):
	#print dataMap
	histone = dataMap["histone"]
	factor = dataMap["factor"]	
	
	#get the datasets
#(this is one of the methylation marks on histones: Tri-methyl-K4) has wt, mut and input.
#We wanted to compare if there is any difference in peak profiles between mut and wt)
	H3K4me3 = subset(histone, 'H3K4me3')
	print H3K4me1
#(this is another one of the methylation marks on histones: Mono-methyl-K4) has wt, mut and input.
#We wanted to compare if there is any difference in peak profiles between mut and wt)	
	H3K4me1 = subset(histone, 'H3K4me1')
#Data has two wt, two mut ( Pbx1 mutant)  and two inputs ( one for wt and one for mut sample) 
#We wanted to compare of there is any difference in peak profiles between mut and wt. 
	acetyl = subset(histone, 'acetyl-K27')
	
	Pbx1 = subset(factor, 'Pbx1')
	today = datetime.date.today().strftime("%Y%m%d")

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

