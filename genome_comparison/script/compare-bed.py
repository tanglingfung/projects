#!/usr/bin/python
"""
Example from the manuscript; see sh_ms_example.sh for the shell script \
equivalent.

Prints the names of genes that are <5000 bp away from intergenic SNPs.
"""
from os import path
from pybedtools import BedTool
import pybedtools

def main():
	
	error_site = BedTool('/home/kwoklab-user/Error_exome_all.bed')
#	protein_coding_site = BedTool('/home/kwoklab-user/Shared_resources/gemini/data/gencode15.protein_coding.20130131.hg19.bed')
	gemini_data_dir = "/home/kwoklab-user/Shared_resources/gemini/data"

	dbsnp_137_site = BedTool('/home/kwoklab-user/Shared_resources/gemini/data/dbsnp.137.vcf.gz')
	#https://code.google.com/p/discovering-cse/
	cse_site = BedTool('/home/kwoklab-user/Shared_resources/gemini/data/cse-hiseq-8_4-2013-02-20.bed.gz')
#	gms_site = BedTools( path.join(gemini_data_dir, 'GRCh37-gms-mappability.vcf.gz'))
	rmsk_site = BedTool(path.join(gemini_data_dir, 'hg19.rmsk.bed.gz'))
	segdup_site = BedTool(path.join(gemini_data_dir, 'hg19.segdup.bed.gz'))
	clinvar_site = BedTool(path.join(gemini_data_dir,'clinvar_20130118.vcf.gz'))
	dgv_site = BedTool(path.join(gemini_data_dir,'hg19.dgv.bed.gz'))
	CpG_site = BedTool(path.join(gemini_data_dir,'hg19.CpG.bed.gz'))
	
	print "total error sites %d" % error_site.count()
	print "error in cse site %d" % (error_site+cse_site).count()
	print "error in dbsnp137 site %d" %(error_site+dbsnp_137_site).count()
	print "errors in repeat mask region %d" % (error_site+rmsk_site).count()
	print "errors in segdup %d" % (error_site+segdup_site).count()
	print "errors in Clinvar %d" % (error_site+clinvar_site).count()
	print "errors in dgv %d" % (error_site+dgv_site).count()
	print "errors in CpG %d" % (error_site+CpG_site).count()
#    print resources
    
   #  bedtools_dir = path.split(__file__)[0]
#     snps = BedTool(path.join(bedtools_dir, '../test/data/snps.bed.gz'))
#     genes = BedTool(path.join(bedtools_dir, '../test/data/hg19.gff'))
# 
#     intergenic_snps = (snps - genes)
# 
#     nearby = genes.closest(intergenic_snps, d=True, stream=True)
# 
#     for gene in nearby:
#         if int(gene[-1]) < 5000:
#             print gene.name

if __name__ == "__main__":
    main()