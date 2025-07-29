#!/usr/bin/python
import sys
import pandas as pd
import pysam 
import re 
import numpy as np
from collections import defaultdict, Counter
import optparse
import logging


def read_filtering(pysam_read):
    if pysam_read.is_unmapped:
        return False
    if pysam_read.is_secondary:
        return False
    if pysam_read.is_supplementary:
        return False
    if pysam_read.is_duplicate:
        return False
    if pysam_read.is_qcfail:
        return False
    return True


def determine_strand(read, strandedness):
	if strandedness == 'fr-firststrand':
		strand1, strand2 = '-', '+'
	elif strandedness == 'fr-secondstrand':
		strand1, strand2 = '+', '-'
	elif strandedness == 'unstranded':
		strand1, strand2 = '.', '.'
	else:
		raise ValueError("\nStrandedness not valid")

	strand = ''
	if   read.is_read1 and not read.is_reverse:
		strand = strand1
	elif read.is_read1 and read.is_reverse:
		strand = strand2
	elif read.is_read2 and read.is_reverse:
		strand = strand1
	elif read.is_read2 and not read.is_reverse:
		strand = strand2
	else:
		if not read.is_reverse:
			strand = strand1
		elif read.is_reverse:
			strand = strand2

	return strand


def splicing_type(jun5ss_counter, jun3ss_counter, strand):

	if len(jun5ss_counter) == 0 and len(jun3ss_counter) == 0:
		exon_type = 'not_spliced'
	
	elif len(jun5ss_counter) > 0 and len(jun3ss_counter) == 0 and strand == '-':
		exon_type = 'first_exon'
	elif len(jun5ss_counter) == 0 and len(jun3ss_counter) > 0 and strand == '+':
		exon_type = 'first_exon'

	elif len(jun5ss_counter) > 0 and len(jun3ss_counter) == 0 and strand == '+':
		exon_type = 'last_exon'
	elif len(jun5ss_counter) == 0 and len(jun3ss_counter) > 0 and strand == '-':
		exon_type = 'last_exon'
	
	elif len(jun5ss_counter) > 0 and len(jun3ss_counter) == 0 and strand == '.':
		exon_type = 'end_exon'
	elif len(jun5ss_counter) == 0 and len(jun3ss_counter) > 0 and strand == '.':
		exon_type = 'end_exon'

	elif len(jun5ss_counter) > 0 and len(jun3ss_counter) > 0:
		exon_type = 'middle_exon'
	else:
		exon_type = 'unknown'
		# raise Exception(f"Unknown exon type {len(jun5ss_counter)} {len(jun3ss_counter)} {strand}")
	return exon_type



def get_coverage(chrom, start, end, strand, bh, strandedness, min_overlap = 5, PADDING = 10):

	RL_counter = Counter()
	jun5ss_counter = Counter()
	jun3ss_counter = Counter()
	inclusion_n = 0

	for read in bh.fetch(chrom, start, end + 1):
		
		if not read_filtering(read):
			continue

		if read.get_overlap(start, end) < min_overlap:
			continue	

		r_strand = determine_strand(read, strandedness)
		
		if r_strand != strand:
			continue

		inclusion_n += 1

		map_blocks = read.get_blocks()

		for j in range(0, len(map_blocks) - 1):
			jun5ss = map_blocks[j][1] # exon ends 
			jun3ss = map_blocks[j + 1][0] # exon starts 

			if jun5ss >= (end - PADDING) and jun5ss <= (end + PADDING):
				jun5ss_counter[jun5ss] += 1

			if jun3ss >= (start - PADDING) and jun3ss <= (start + PADDING):
				jun3ss_counter[jun3ss] += 1

		RL_counter[len(read.query_sequence)] += 1

	if not RL_counter:
		RL = np.nan
	else:
		RL = RL_counter.most_common()[0][0]

	label = splicing_type(jun5ss_counter, jun3ss_counter, strand)

	max_junc_count = max(list(jun5ss_counter.values()) + list(jun3ss_counter.values()) + [0])

	return (inclusion_n, label, RL, max_junc_count)



def calculate_psi(inclusion_n, exclusion_n, len_intron, RL):
	intron_norm = inclusion_n/(len_intron + RL)
	intron_norm = intron_norm - (intron_norm % 0.01)

	ex_norm = exclusion_n/RL
	ex_norm = ex_norm - (ex_norm % 0.01)

	try:
		PSI = round(intron_norm/(intron_norm + ex_norm) , 2)
	except:
		PSI = np.nan

	return PSI


class myparser():

	def __init__(self, line):
		contig, jxn_s, jxn_e, samples, counts, strand = line.split('\t')
		self.jxn_s = int(jxn_s)
		self.jxn_e = int(jxn_e)
		self.contig = contig
		
		if strand == '1':
			jxn_strand = '+'
		elif strand == '2':
			jxn_strand = '-'
		elif strand == '0':
			jxn_strand = '.'
		else:
			jxn_strand = strand

		self.strand = jxn_strand 
		self.len = self.jxn_e - self.jxn_s + 1
		self.samples = samples.split(',')	
		self.counts  = map(int, counts.split(','))
		self.sm_count = dict(zip(self.samples, self.counts))




def main():

	args = sys.argv
	PADDING = 10
	logging.basicConfig(level = logging.INFO, format = '%(filename)s %(asctime)s %(levelname)s:\t%(message)s')

	usage_instructions = f"""CryEx_psi_calculator -f fofn -e exon_coordinates -o output_file"""

	parser = optparse.OptionParser(usage = usage_instructions)

	parser.add_option('-f', dest='fofn', \
        help = 'Metadata file [required]', default = None)
	parser.add_option('-j', dest='jxn_file', \
		help = 'Exons Coords File')
	parser.add_option('-e', dest='exons_file', \
		help = 'Exons Coords File')
	parser.add_option('-s', dest='strandedness', \
        help = 'Library strandedness [optional]', default = 'fr-firststrand')
	parser.add_option('-o', dest='output_file', \
		help = 'Output File')

	options, args = parser.parse_args()

	### jxn file
	tbx = pysam.TabixFile(options.jxn_file)

	### write output file
	outf = open(options.output_file, 'w')
	outf.write(f"exon_type\tchrom\texon_3ss\texon_5ss\tstrand\tinclusion_n\tjxn_inc_n\texc_5ss\texc_3ss\texclusion_n\tSAMPLE\tPSI\n")


	### read metadata
	METADATA = pd.read_csv(options.fofn, sep = '\t')

	bh_list = []
	for row in METADATA.itertuples():
		bh = pysam.AlignmentFile(row.BAM, 'rb') 
		bh_list.append([row.SAMPLE, bh])

	### read exon file
	df = pd.read_csv(options.exons_file, sep='\t', header=None, comment='#')
	df.columns = ['chrom', 'source', 'type', 'start', 'end', 'score', 'strand', 'frame', 'attributes']
	df = df[df['type'] == 'exon']
	df = df[['chrom', 'start', 'end', 'strand']].drop_duplicates()

	logging.info(f'Calculating psi of exons')

	for e_j, exon in enumerate(df.itertuples()):

		INFO = {}
		for sample_name, bh in bh_list:
			vals = get_coverage(exon.chrom, exon.start, exon.end, exon.strand, bh, options.strandedness)
			INFO[sample_name] = vals

		exon_len = (exon.end - exon.start + 1)

		for line in tbx.fetch(exon.chrom, exon.start, exon.end):

			line = myparser(line)

			if line.jxn_s < exon.start and exon.end < line.jxn_e:
				
				for sample_name, exclusion_n in line.sm_count.items():
					(inclusion_n, exon_type, RL, max_jxn_n) = INFO[sample_name]

					psi = calculate_psi(inclusion_n, exclusion_n, exon_len, RL)

					outline_1 = [exon_type, exon.chrom, exon.start, exon.end, exon.strand]
					outline_2 = [inclusion_n, max_jxn_n, line.jxn_s, line.jxn_e, exclusion_n, sample_name, psi]
					outf.write('\t'.join(map(str, outline_1 + outline_2)) + '\n')

		if e_j % int(1e3) == 0:
			logging.info(f'\tprocessed {e_j:,} exons')

	logging.info(f'Calculating psi of introns')

	for i_j, row in enumerate(tbx.fetch()):
		
		line = myparser(row)

		if line.len < 20: 
			continue

		INFO = {}
		for sample_name, bh in bh_list:
			vals = get_coverage(line.contig, line.jxn_s, line.jxn_e, line.strand, bh)
			INFO[sample_name] = vals

		for sample_name, exclusion_n in line.sm_count.items():

			(inclusion_n, exon_type, RL, max_jxn_n) = INFO[sample_name]

			psi = calculate_psi(inclusion_n, exclusion_n, line.len, RL)

			### Direct output to STDOUT
			outline_1 = ['intron', line.contig, line.jxn_s, line.jxn_e, line.strand]
			outline_2 = [inclusion_n, max_jxn_n, '.', '.', exclusion_n, sample_name, psi]
			outf.write('\t'.join(map(str, outline_1 + outline_2)) + '\n')
		
		if i_j % int(1e4) == 0:
			logging.info(f'\tprocessed {i_j:,} introns')

	outf.close()




if __name__ == "__main__":
	main()
