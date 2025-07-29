#!/usr/bin/python
import sys
import pysam 
import pandas as pd
from collections import defaultdict, Counter
import optparse
import subprocess
import multiprocessing as mp
import logging
import os


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


def extract_jxns_from_bam(bam_file, star_file, sample_name, strandedness, overhang_minimum = 8):
    
    junctions_bam = defaultdict(int)

    if not os.path.exists(star_file):
        logging.info(f"[Warning] STAR juncion file {star_file} does not exist. Counting junctions from bam file {bam_file}")

        # extract splice junctions_bam from bam file
        bh = pysam.AlignmentFile(bam_file, "rb")
        for r in bh:

            if not read_filtering(r):
                continue

            r_strand = determine_strand(r, strandedness)

            map_blocks = r.get_blocks()
            chrom = r.reference_name
            
            for j in range(0, len(map_blocks) - 1):
                jun5ss = map_blocks[j][1] # 0 -base
                jun3ss = map_blocks[j + 1][0] # 1 - base

                if jun3ss - jun5ss > 20:
                    junctions_bam[(chrom, jun5ss, jun3ss, r_strand)] += 1

    else:
        df = pd.read_csv(star_file, header = None, sep = '\t')
        df.columns = ['chrom', 'jxn_s', 'jxn_e', 'strand', 'motif', 'annotated', 'n_uniq', 'n_multi', 'max_ov']
        df = df[df.max_ov >= overhang_minimum]

        for row in df.itertuples():
            if row.strand == 1:
                strand = '+'
            elif row.strand == 2:
                strand = '-'
            elif row.strand == 0:
                strand = '.'
            else:
                raise ValueError(f"Strand not valid {row.strand}")

            jxn = (row.chrom, row.jxn_s - 1, row.jxn_e, strand)
            junctions_bam[jxn] = row.n_uniq 

    return (sample_name, junctions_bam)


def main():
    args = sys.argv

    logging.basicConfig(level = logging.INFO, format = '%(filename)s %(asctime)s %(levelname)s:\t%(message)s')

    # option parser
    usage_instructions = f"""CryEx_junctions -f fofn -o output_file"""

    parser = optparse.OptionParser(usage = usage_instructions)
    parser.add_option('-f', dest='fofn', \
        help = 'Metadata file [required]', default = None)
    parser.add_option('-s', dest='strandedness', \
        help = 'Library strandedness [optional]', default = 'fr-firststrand')
    parser.add_option('-o', dest='output', \
        help = 'Output File [required]', default = None)

    options, args = parser.parse_args()


    logging.info(f'bam file strandedness = {options.strandedness}')

    METADATA = pd.read_csv(options.fofn, sep = '\t')

    pool = mp.Pool(processes = 10)

    args = [(row.BAM, row.STAR_SJ_OUT, row.SAMPLE, options.strandedness) for row in METADATA.itertuples()]

    results = pool.starmap_async(extract_jxns_from_bam, args)    

    jxn_merged = defaultdict(lambda : defaultdict(lambda : 0))
    for (sm , jxn_dict) in results.get():
        for jxn, n in jxn_dict.items():
            jxn_merged[jxn][sm] = n


    outf = open(options.output, 'w')
       
    for jxn in jxn_merged:
        chrom, jxn_s, jxn_e, strand = jxn 

        s = ','.join(map(str, METADATA.SAMPLE))

        n = [jxn_merged[jxn][sm] for sm in METADATA.SAMPLE]
        n = ','.join(map(str, n))

        outf.write(f'{chrom}\t{jxn_s}\t{jxn_e}\t{s}\t{n}\t{strand}\n')

    outf.close()

    # process jxn file
    COMMAND_SORT = f"less {options.output} | sort -k1,1V -k2,2n -k3,3n | bgzip -c > {options.output}.gz"
    mycmd = subprocess.getoutput(COMMAND_SORT)
    logging.info(mycmd)

    COMMAND_SORT = f"tabix -f {options.output}.gz"
    mycmd = subprocess.getoutput(COMMAND_SORT)
    logging.info(mycmd)


    logging.info(f'job finished')


if __name__ == "__main__":
    main()
