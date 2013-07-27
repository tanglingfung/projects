import sys
import argparse
import os
import glob
import shutil
import datetime
import gzip #potential increase in speed (havne't implement yet)
from mako.template import Template

def process_sample(sdir, fdir):
#pre: 	it's a PE flowcell
#		lane is not considered here
#       one sample has one index
	today = datetime.date.today().strftime("%Y%m%d")
	upload_dir = '/media/KwokRaid02/pipeline-output'
	for root, dirs, files in os.walk(sdir):
		if 'SampleSheet.csv' in files:
			samplesheet  = samplesheetReader(os.path.join(root, 'SampleSheet.csv'))
			sampleID = samplesheet['SampleID']
			sampleID = sampleID.replace('_', '-')
			flowcell = samplesheet['FCID']
			barcode = samplesheet['Index']
			description = sampleID + '_' + samplesheet['Description']
			Recipe = samplesheet['Recipe']
			projectID = samplesheet['SampleProject']
			work_dir = os.path.join(fdir, sampleID)			
			#add a safe mkdir dir
			if not os.path.exists(work_dir):
				os.makedirs(work_dir)
			if get_fs_freespace(work_dir) < 300*1024*1024*1024:
				print "not enough space"
				break
			r1 = glob.glob(root+"/*R1*")
			r2 = glob.glob(root+"/*R2*")
			zcat_r1, r1_fastq = generate_zcat_command(r1, work_dir, sampleID, flowcell, 'R1.fastq')
			zcat_r2, r2_fastq = generate_zcat_command(r2, work_dir, sampleID, flowcell, 'R2.fastq')
			print zcat_r1
			print zcat_r2
			os.system(zcat_r1)
			os.system(zcat_r2)
			tmpl= Template(_run_info_template)
			run_info = tmpl.render(sampleID=sampleID, today=today, flowcell=projectID, upload_dir=upload_dir, fastq1 = r1_fastq, fastq2=r2_fastq, description=description)
			run_info_file = os.path.join(work_dir, sampleID + '_' + flowcell + '_run_info.yaml')
			with open(run_info_file, "w") as out_handle:
				out_handle.write(run_info)
			os.chdir(work_dir)	
			os.system("bcbio_nextgen.py ~/nextgen-python2.7/bcbio-nextgen/bcbio_system.yaml %s %s -n 4" % (work_dir, run_info_file))
			shutil.rmtree(work_dir)
			
        
_run_info_template=r"""

fc_date: ${today}
fc_name: ${flowcell}
upload:
  dir: ${upload_dir}
details:
  - files: [${fastq1}, ${fastq2}]
    description: ${description}
    analysis: variant
    genome_build: GRCh37
    algorithm:
      aligner: bwa
      recalibrate: true
      realign: true
      variantcaller: gatk
      coverage_interval: exome
      coverage_depth: high
      variant_regions: /home/kwoklab-user/Shared_resources/oligos/Kidney_exome_v4_UTR_custom.GRCh37.bed 
      hybrid_bait: /home/kwoklab-user/Shared_resources/oligos/Kidney_exome_v4_UTR_custom.GRCh37.bed 
      hybrid_target: /home/kwoklab-user/Shared_resources/oligos/Kidney_exome_v4_UTR_custom.GRCh37.bed 
      lane: ${sampleID}
"""
def get_fs_freespace(pathname):
	"Get the free space of the filesystem containing pathname"
	stat= os.statvfs(pathname)
	# use f_bfree for superuser, or f_bavail if filesystem
	# has reserved space for superuser
	return stat.f_bfree*stat.f_bsize

def generate_zcat_command(files, dest_path, sampleID, flowcell, suffix):
	cmd = 'zcat '
	final_fastq = dest_path +'/'+ sampleID + '_' + flowcell + '_' + suffix
	for file in files:
		cmd += file +' '
	cmd += ' > ' + final_fastq
	return (cmd, final_fastq)
			

def samplesheetReader(samplesheet):
	f = open(samplesheet, "r")
	while True:
		keys = f.readline().strip().split(',')
		values = f.readline().strip().split(',')
		break
	dictionary = dict(zip(keys, values))
	return dictionary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='concat and decompress fastq files')
    parser.add_argument('-i', dest='source', help='fastq source')
    parser.add_argument('-o', dest='dest', help='fastq destination', default="/media/KwokRaid01/pipeline_tmp")
    options = parser.parse_args()
    process_sample(options.source, options.dest)

