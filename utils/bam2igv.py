import sys
import argparse
import os
import glob
import shutil
import datetime
import re
import gffutils
import pybedtools

def prep_mpileup(align_bams, ref_file, max_read_depth, config,
                 target_regions=None, want_bcf=True):
    cl = [config_utils.get_program("samtools", config), "mpileup",
          "-f", ref_file, "-d", str(max_read_depth), "-L", str(max_read_depth),
          "-m", "3", "-F", "0.0002"]
    if want_bcf:
        cl += ["-D", "-S", "-u"]
    if target_regions:
        str_regions = bamprep.region_to_gatk(target_regions)
        if os.path.isfile(str_regions):
            cl += ["-l", str_regions]
        else:
            cl += ["-r", str_regions]
    cl += align_bams
    return " ".join(cl)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='analyze chipseq dataset from Olga')
    parser.add_argument('-d', dest='data', help='data file', default = 'data.yaml')
    options = parser.parse_args()
    with open(options.data) as in_handle:
    	dataMap = yaml.safe_load(in_handle)
    	in_handle.close()
    process_data(dataMap)
#    process_sample(options.source, options.dest, options.exome_target)

