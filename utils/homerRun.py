"""Work with HOMER at Glass lab at UCSD
Heinz S, Benner C, Spann N, Bertolino E et al. Simple Combinations of Lineage-Determining Transcription Factors Prime cis-Regulatory Elements Required for Macrophage and B Cell Identities. Mol Cell 2010 May 28;38(4):576-589. PMID: 20513432

"""

import sys
import os
import subprocess


def create_tag(bam, options, out_dir=None):
    #makeTagDirectory <Output Directory Name> [options] <alignment file1> [alignment file 2] ...
    #Clonal Tag Distribution
	#tagCountDistribution.txt - File contains a histogram of clonal read depth, showing the number of reads per unique position.  If an experiment is "over-sequenced", you start seeing the same reads over and over instead of unique reads.  Sometimes this is a sign there was not enough starting material for sequencing library preparation.  Below are examples of ideal and non-ideal results - in the case of the non-ideal experiment, you probably don't want to sequence that library anymore.

    cmd = ["makeTagDirectory", out_dir, bam]
  	_do_run(' '.join(cmd))
	return out_dir

def findPeaks(test_tag_dir, style, control_tag_dir):
Recommend Parameters for fixed width peaks (i.e. for motif finding):
findPeaks Macrophage-H3K4me1/ -i Macrophage-IgG -size 1000 -minDist 2500 > output.txt

Recommend Parameters for variable length peaks (H3K4me1 at least).
findPeaks Macrophage-H3K4me1/ -i Macrophage-IgG -region -size 1000 -minDist 2500 > output.txt


	cmd = ["findPeaks", test_tag_dir, "-style", style, "-o auto", "-i", control_tag_dir]
	_do_run(' '.join(cmd))
	if style == 'factor':
		return os.path.join(test_tag_dir, "peaks.txt")
	if style == 'histone':
		return os.path.join(test_tag_dir, "regions.txt")
	if style == 'groseq':
		return os.path.join(test_tag_dir, "transcripts.txt")
#To run findPeaks, you will normally type:  

#findPeaks <tag directory> -style <factor|histone|groseq> -o auto -i <control tag directory>

# for factor chip
#getFocalPeaks.pl <peak file> <focus % threshold> > focalPeaksOutput.txt

i#.e. getFocalPeaks.pl ERpeaks.txt 0.90 > ERfocalPeaks.txt

#i.e. findPeaks ERalpha-ChIP-Seq/ -style factor -o auto -i Control-ChIP-Seq/

pos2bed.pl peakfile.txt > peakfile.bed

#Where the first argument must be the tag directory (required).  The other options are not required.  The "-style <...>" option can be either "factor", "histone", or "groseq".  Use the "-i" option to specify a control experiment tag directory (good idea when doing ChIP-Seq).
#Output files

#Use the "-o <filename>" to specify where to send the resulting peak file.  If "-o" is not specified, the peak file will be written to stdout.  

#If "-o auto" is specified, the peaks will be written to:
#"<tag directory>/peaks.txt" (-style factor)
#"<tag directory>/regions.txt" (-style histone)
#"<tag directory>/transcripts.txt" and "<tag directory>/transcripts.gtf" (-style groseq)


	# findPeaks <tag directory> -style <factor|histone|groseq> -o auto -i <control tag directory>
	#
	#Column 1: PeakID - a unique name for each peak (very important that peaks have unique names...)
	#Column 2: chr - chromosome where peak is located
	#Column 3: starting position of peak
	#Column 4: ending position of peak
	#Column 5: Strand (+/-)
	#Column 6: Normalized Tag Counts - number of tags found at the peak, normalized to 10 million total mapped tags (or defined by the user)
	#Column 7: (-style factor): Focus Ratio - fraction of tags found appropriately upstream and downstream of the peak center. (see below)
	#                 (-style histone/-style groseq): Region Size - length of enriched region
	#Column 8: Peak score (position adjusted reads from initial peak region - reads per position may be limited)
	#Columns 9+: Statistics and Data from filtering

#		
	def findMotifsGenome (bed_file, genome, out_dir, bg_bed_file=None):
	
	#findMotifsGenome.pl <peak/BED file> <genome> <output directory> [options]

#     def get_summary_metrics(self, align_metrics, dup_metrics,
#             insert_metrics=None, hybrid_metrics=None, vrn_vals=None,
#             rnaseq_metrics=None):
#         """Retrieve a high level summary of interesting metrics.
#         """
#         with open(align_metrics) as in_handle:
#             align_vals = self._parse_align_metrics(in_handle)
#         if dup_metrics:
#             with open(dup_metrics) as in_handle:
#                 dup_vals = self._parse_dup_metrics(in_handle)
#         else:
#             dup_vals = {}
#         (insert_vals, hybrid_vals, rnaseq_vals) = (None, None, None)
#         if insert_metrics and file_exists(insert_metrics):
#             with open(insert_metrics) as in_handle:
#                 insert_vals = self._parse_insert_metrics(in_handle)
#         if hybrid_metrics and file_exists(hybrid_metrics):
#             with open(hybrid_metrics) as in_handle:
#                 hybrid_vals = self._parse_hybrid_metrics(in_handle)
#         if rnaseq_metrics and file_exists(rnaseq_metrics):
#             with open(rnaseq_metrics) as in_handle:
#                 rnaseq_vals = self._parse_rnaseq_metrics(in_handle)
# 
#         return self._tabularize_metrics(align_vals, dup_vals, insert_vals,
#                 hybrid_vals, vrn_vals, rnaseq_vals)
# 
# 
# 
#     def _tabularize_metrics(self, align_vals, dup_vals, insert_vals,
#                             hybrid_vals, vrn_vals, rnaseq_vals):
#         out = []
#         # handle high level alignment for paired values
#         paired = insert_vals is not None
# 
#         total = align_vals["TOTAL_READS"]
#         align_total = int(align_vals["PF_READS_ALIGNED"])
#         out.append(("Total", _add_commas(str(total)),
#                     ("paired" if paired else "")))
#         out.append(self._count_percent("Aligned",
#                                        align_vals["PF_READS_ALIGNED"], total))
#         if paired:
#             out.append(self._count_percent("Pairs aligned",
#                                            align_vals["READS_ALIGNED_IN_PAIRS"],
#                                            total))
#             align_total = int(align_vals["READS_ALIGNED_IN_PAIRS"])
#             dup_total = dup_vals.get("READ_PAIR_DUPLICATES")
#             if dup_total is not None:
#                 out.append(self._count_percent("Pair duplicates",
#                                                dup_vals["READ_PAIR_DUPLICATES"],
#                                                align_total))
#             std = insert_vals.get("STANDARD_DEVIATION", "?")
#             std_dev = "+/- %.1f" % float(std.replace(",", ".")) if (std and std != "?") else ""
#             out.append(("Insert size",
#                 "%.1f" % float(insert_vals["MEAN_INSERT_SIZE"].replace(",", ".")), std_dev))
#         if hybrid_vals:
#             out.append((None, None, None))
#             out.extend(self._tabularize_hybrid(hybrid_vals))
#         if vrn_vals:
#             out.append((None, None, None))
#             out.extend(self._tabularize_variant(vrn_vals))
#         if rnaseq_vals:
#             out.append((None, None, None))
#             out.extend(self._tabularize_rnaseq(rnaseq_vals))
#         return out
# 
#     def _tabularize_variant(self, vrn_vals):
#         out = []
#         out.append(("Total variations", vrn_vals["total"], ""))
#         out.append(("In dbSNP", "%.1f\%%" % vrn_vals["dbsnp_pct"], ""))
#         out.append(("Transition/Transversion (all)", "%.2f" %
#             vrn_vals["titv_all"], ""))
#         out.append(("Transition/Transversion (dbSNP)", "%.2f" %
#             vrn_vals["titv_dbsnp"], ""))
#         out.append(("Transition/Transversion (novel)", "%.2f" %
#             vrn_vals["titv_novel"], ""))
#         return out
#         	
# def _do_run(cmd):
#     """Perform running and check results, raising errors for issues.
#     """
#     print "running " + cmd
#     subprocess.call(cmd, shell=True)
# 
# 
