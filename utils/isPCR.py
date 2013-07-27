import urllib
import re
import sys, getopt


def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	out_f = open(outputfile, 'w')
	with open(inputfile) as f:
		for line in f:
			primers = line.strip().split()
			size = get_amplicon_size(primers[0], primers[1])
			out_f.write("\t".join([primers[0], primers[1], size]) + "\n")

def get_amplicon_size(forward, reserve):
	params = urllib.urlencode({'hgsid': 334012725, 'org': 'Human', 'db': 'hg19', 'wp_target':'genome', 'wp_f': forward , 'wp_r': reserve })
	f = urllib.urlopen("http://genome.ucsc.edu/cgi-bin/hgPcr?%s" % params)
	for aLine in f.readlines():
		match = re.search("chr[0-9|'X'|'Y']{1,2}:[0-9]+-[0-9]+.* ([0-9]+)bp", aLine)
		if match:
			return match.group(1)

if __name__ == "__main__":
   main(sys.argv[1:])



# match = re.search("chr([0-9|'X'|'Y']{1,2})", test); #print chr
# if match:
#    print match.group(1)
# 
# match = re.search("chr[0-9|'X'|'Y']{1,2}:([0-9]+)-([0-9]+)", test); #print pos
# if match:
#    print match.group(1)
#    print match.group(2)
# 
# match = re.search("chr[0-9|'X'|'Y']{1,2}:[0-9]+-[0-9]+.* ([0-9]+)bp",
# test); #print bp
# if match:
#    print match.group(1)
