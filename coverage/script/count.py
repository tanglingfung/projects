import subprocess
import os
import argparse
import shutil
import sys
from bcbio.distributed.transaction import file_transaction
from bcbio import broad
from bcbio.pipeline.config_utils import load_config
from bcbio.pipeline.alignment import sam_to_querysort_sam

#samtools view file.bam | htseq-count (options) - GTF > counts.txt
def count(bam_file):
    bed_file = '/media/KwokRaid02/nina/ISMB2013/bed_files/auto_exon.bed' 
    ref_file = '/media/KwokRaid01/biodata/genomes/Hsapiens/GRCh37/seq/GRCh37.fa'
    config_file = '/home/kwoklab-user/nextgen-python2.7/bcbio-nextgen/bcbio_system.yaml'
    gene_file = '/home/kwoklab-user/nina/ISMB2013/bed_files/geneTrack.ensembl_mergedSorted_noChrMnumericCHR.txt'
    work_dir = '/media/KwokData02/ISMB2013-analysis'
    config = load_config(config_file)
    broad_runner = broad.runner_from_config(config)
    base, _ = os.path.splitext(os.path.basename(bam_file))

#    gtf_file = '/media/KwokRaid01/biodata/genomes/Hsapiens/GRCh37/ref-transcripts.gtf'    
#    out_file = os.path.join( work_dir , base + ".counts")
#    htseq = 'htseq-count'
#    in_file = sam_to_querysort_sam(bam_file, config)    
#    with file_transaction(out_file) as tmp_out_file:
#        htseq_cmd = ("{htseq} --mode=union --stranded=no --type=exon --idattr=gene_id {in_file}  {gtf_file} > {tmp_out_file}")
#        cmd = htseq_cmd.format(**locals())
#        print cmd
#        subprocess.check_call(cmd, shell=True)
		
    depth_of_coverage_file = os.path.join( work_dir , base + '.doc' )
    params = [ "-R", ref_file]
    params += ["-T", "DepthOfCoverage", "-o", depth_of_coverage_file, "-I", bam_file, "-L", bed_file, "-geneList",gene_file]
    broad_runner.run_gatk(params)
    #     diagnose_file = os.path.join( work_dir , base + '.DiagnoseTargets.vcf')
#     params = [ "-R", ref_file]
#     params += ["-T", "DiagnoseTargets", "-o", diagnose_file, "-I", bam_file, "-L", bed_file]
#     broad_runner.run_gatk(params)
#     
    
    callable_file = os.path.join( work_dir , base + '.callable.bed')
    params = [ "-R", ref_file]
    params += ["-T", "CallableLoci", "-o", callable_file, "-I", bam_file, "-L", bed_file]
    broad_runner.run_gatk(params)
    
    GCcontent_file = os.path.join( work_dir , base + '.GCcontent.bed')
    params = [ "-R", ref_file]
    params += ["-T", "GCContentByInterval", "-o", GCcontent_file, "-L", bed_file]
    broad_runner.run_gatk(params)
    return True

          
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='gene count')
    parser.add_argument('-i', dest='source', help='bam source')
    options = parser.parse_args()
    count(options.source)

