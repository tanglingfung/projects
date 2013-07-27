
import subprocess
import os
import argparse
import shutil
import sys
from bcbio.distributed.transaction import file_transaction
from bcbio import broad
from bcbio.pipeline.config_utils import load_config



#gatk command: -R /home/kwoklab-user/Shared_resources/biodata/genomes/Hsapiens/GRCh37/seq/GRCh37.fa
# -T DepthOfCoverage 
# -o whole_genome_coverage_SeqCap.txt 
#-I NA12878.mapped.ILLUMINA.bwa.CEU.high_coverage.20120522.bam 
#-L SeqCap_EZ_v3_low_coverage_GRC37.bed 

def coverage(align_bam):                     
    config_file = '/home/kwoklab-user/nextgen-python2.7/bcbio-nextgen/bcbio_system.yaml'
    ref_file = '/media/KwokRaid01/biodata/genomes/Hsapiens/GRCh37/seq/GRCh37.fa'
    bed_file = '/media/KwokRaid02/nina/ISMB2013/bed_files/capture_regions/130214_HG19_Cardiac_RD_EZ.GRCh37.target.bed' 
    config = load_config(config_file) 
    broad_runner = broad.runner_from_config(config)#    broad_runner.run_fn("picard_index_ref", ref_file)
    broad_runner.run_fn("picard_index", align_bam)
    broad_runner = broad.runner_from_config(config)
    config = load_config(config_file) 
    base, _ = os.path.splitext(os.path.basename(align_bam))
    work_dir =  os.path.dirname(align_bam)
    out_file = os.path.join( work_dir , base )
    params = [ "-R", ref_file]
#    with file_transaction(out_file) as tx_out_file:
    params += ["-T", "DepthOfCoverage", "-o", out_file, "-I", align_bam, "-L", bed_file]
    broad_runner.run_gatk(params)
    return out_file
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='gene count')
    parser.add_argument('-i', dest='source', help='bam source')
    options = parser.parse_args()
    coverage(options.source)
    
    
    #CallableLoci
    #DiagnoseTargets
