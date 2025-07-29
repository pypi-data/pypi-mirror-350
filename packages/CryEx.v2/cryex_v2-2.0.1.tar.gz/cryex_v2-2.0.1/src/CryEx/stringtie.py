#!/usr/bin/python
import sys
import pandas as pd
import os
import subprocess
import logging
import optparse


def main():
    args = sys.argv

    logging.basicConfig(level = logging.INFO, format = '%(filename)s %(asctime)s %(levelname)s:\t%(message)s')

    # option parser
    usage_instructions = f"""CryEx_stringtie -f fofn -o output_file"""

    parser = optparse.OptionParser(usage = usage_instructions)
    parser.add_option('-f', dest='fofn', \
        help = 'Metadata file [required]', default = None)
    parser.add_option('-s', dest='strandedness', \
        help = 'Library strandedness [optional]', default = 'fr-firststrand')
    parser.add_option('-o', dest='output', \
        help = 'Output File [required]', default = None)

    options, args = parser.parse_args()

    logging.info(f'assumed strandedness for bam file = {options.strandedness}')

    METADATA = pd.read_csv(options.fofn, sep = '\t')

    if options.strandedness == 'fr-firststrand':
        strand_param = '--rf'
    elif options.strandedness == 'fr-secondstrand':
        strand_param = '--fr'
    elif options.strandedness == 'unstranded':
        strand_param = ''

 
    for row in METADATA.itertuples():
        STRINGTIE_COMMAND = f"stringtie {row.BAM} -j 2 -f 0.05 -g 10 {strand_param} > {options.output}.{row.SAMPLE}.gtf"
        try:
            result = subprocess.run(STRINGTIE_COMMAND,
                shell = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text = True,
                check = True)
            logging.info(f"Command output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed with return code: {e.returncode}")
            logging.error(f"Error message: {e.stderr}")
            

        

    STRINGTIE_COMMAND = f"cat {options.output}.*.gtf | sort -k1,1V -k4,4n -k5,5n > {options.output}"
    mycmd = subprocess.getoutput(STRINGTIE_COMMAND)

    logging.info(mycmd)

if __name__ == "__main__":
    main()
