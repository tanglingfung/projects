import sys
import argparse
import os
import glob
import shutil
import datetime
import re
import gzip #potential increase in speed (havne't implement yet)
from mako.template import Template
import subprocess

def process_sample(sdir, fdir):
#pre: 	it's a PE flowcell
#		lane is not considered here
#       one sample has one index
	today = datetime.date.today().strftime("%Y%m%d")
	
	for root, dirs, files in os.walk(sdir):
		if 'SampleSheet.csv' in files:
			samplesheet  = samplesheetReader(os.path.join(root, 'SampleSheet.csv'))
			sampleID = samplesheet['SampleID']
			sampleID = sampleID.replace('_', '-')
			sampleID = sampleID.replace('.', '-')
			flowcell = samplesheet['FCID']
			barcode = samplesheet['Index']
			description = samplesheet['Description']
			if description == '': 
				description = sampleID
			else:
				description = sampleID + '_' + description
			Recipe = samplesheet['Recipe']
			projectID = samplesheet['SampleProject']
			dir_id = "%s-%s-%s" % (today, projectID, sampleID)
			work_dir = os.path.join(fdir, sampleID)
			upload_dir = '/media/KwokRaid02/pipeline-output/%s' % (dir_id)
			if not 	os.path.exists(upload_dir):
				os.makedirs(upload_dir)
			#add a safe mkdir dir
			if not os.path.exists(work_dir):
				os.makedirs(work_dir)
			if get_fs_freespace(work_dir) < 300*1024*1024*1024:
				print "not enough space"
				break
			r1 = sorted(glob.glob(root+"/*R1*"))
						
			#generate three commands
			zcat_r1, r1_fastq = generate_zcat_command(r1, work_dir, sampleID, flowcell, 'R1.fastq')

			tmpl= Template(_run_info_template)
			run_info = tmpl.render(sampleID=sampleID, today=today, flowcell=projectID, upload_dir=upload_dir, fastq1 = r1_fastq, description=description)
			run_info_file = os.path.join(upload_dir, dir_id + '_run_info.yaml')
			with open(run_info_file, "w") as out_handle:
				out_handle.write(run_info)

 			
			os.system('source ~/nextgen-python2.7/bin/activate')
			bcbio_command = "bcbio_nextgen.py ~/nextgen-python2.7/bcbio-nextgen/bcbio_system.yaml %s %s -n 8 " % (work_dir, run_info_file)
			command_log_file = os.path.join(upload_dir, dir_id + '_command.log')
			with open(command_log_file, 'w') as out_handle:
				out_handle.write(zcat_r1 + "\n")
				out_handle.write(bcbio_command + "\n")
				
			os.chdir(work_dir)					
			_do_run(zcat_r1)
			_do_run(bcbio_command)
			#shutil.rmtree(work_dir)

def _do_run(cmd):
    """Perform running and check results, raising errors for issues.
    """
    print "running " + cmd
    subprocess.call(cmd, shell=True)			
    
_run_info_template=r"""

fc_date: ${today}
fc_name: ${flowcell}
upload:
  dir: ${upload_dir}
details:
  - files: [${fastq1}]
    description: ${description}
    analysis: RNA-seq
    genome_build: mm9
    lane: ${sampleID}
    algorithm:
      aligner: bwa
      trim_reads: read_through
      adapters: [truseq, polya]
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

