"""Work with HOMER at Glass lab at UCSD
Heinz S, Benner C, Spann N, Bertolino E et al. Simple Combinations of Lineage-Determining Transcription Factors Prime cis-Regulatory Elements Required for Macrophage and B Cell Identities. Mol Cell 2010 May 28;38(4):576-589. PMID: 20513432

"""

import os
import subprocess
from bcbio.provenance import do
from bcbio.utils import curdir_tmpdir


class Homer:
    """Simplify running Broad commandline tools.
    """
    def __init__(self, config):
#        resources = config_utils.get_resources("gatk", config)
        self._config = config
        self._resources = resources
        self._homer_version = None
        
    def run(self, command, options, pipe=False, get_stdout=False):
        """Run a Picard command with the provided option pairs.
        """
        cl = self.cl_picard(command, options)
        if pipe:
            subprocess.Popen(cl)
        elif get_stdout:
            p = subprocess.Popen(cl, stdout=subprocess.PIPE)
            stdout = p.stdout.read()
            p.wait()
            p.stdout.close()
            return stdout
        else:
            do.run(cl, "Picard {0}".format(command), None)

    def get_homer_version(self, command):
#         if os.path.isdir(self._picard_ref):
#             picard_jar = self._get_jar(command)
#             cl = ["java", "-Xms5m", "-Xmx5m", "-jar", picard_jar]
#         else:
#             cl = [self._picard_ref, command]
#         cl += ["--version"]
#         p = subprocess.Popen(cl, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#         version = float(p.stdout.read().split("(")[0])
#         p.wait()
#         p.stdout.close()
#         return version


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
		