#!/usr/bin/python
import sys
import pandas as pd
import pysam 
import re 
import numpy as np
from collections import defaultdict, Counter
from scipy.stats import betabinom, chi2
from statsmodels.stats.multitest import multipletests
import optparse
import logging



def beta_binomial_llr(grp1_lst, grp2_lst):
    # row.PSI, row.jxn_inc_n, row.exclusion_n, cov

    mean_psi_grp1 = np.nanmean([x[1]/x[3] for x in grp1_lst])
    stdv_psi_grp1 = np.nanstd([x[1]/x[3] for x in grp1_lst])

    alpha_grp1 = mean_psi_grp1/stdv_psi_grp1
    beta_grp1 = (1 - mean_psi_grp1)/stdv_psi_grp1


    mean_psi_grp2 = np.nanmean([x[1]/x[3] for x in grp2_lst])
    stdv_psi_grp2 = np.nanstd([x[1]/x[3] for x in grp2_lst])

    alpha_grp2 = mean_psi_grp2/stdv_psi_grp2
    beta_grp2 = (1 - mean_psi_grp2)/stdv_psi_grp2

    LL_A = 0

    for (psi, inclusion_n, exclusion_n, n) in grp1_lst:
        p = betabinom.logcdf(inclusion_n, n, alpha_grp1, beta_grp1, loc = 0)
        LL_A += p

    for (psi, inclusion_n, exclusion_n, n) in grp2_lst:
        p = betabinom.logcdf(inclusion_n, n, alpha_grp2, beta_grp2, loc = 0)
        LL_A += p

    mean_psi_null = np.nanmean([x[1]/x[3] for x in grp1_lst + grp2_lst])
    stdv_psi_null = np.nanstd([x[1]/x[3] for x in grp1_lst + grp2_lst])

    alpha_null = mean_psi_null/stdv_psi_null
    beta_null = (1 - mean_psi_null)/stdv_psi_null

    LL_O = 0
    for (psi, inclusion_n, exclusion_n, n) in grp1_lst + grp2_lst:
        p = betabinom.logcdf(inclusion_n, n, alpha_null, beta_null, loc = 0)
        LL_O += p

    # chi-square p-value from log likelihood ratio
    LL_R = LL_A - LL_O

    chi = 2 * LL_R    
    pval = 1 - chi2.cdf(chi, 1)

    return LL_R, pval


def main():

    args = sys.argv
    logging.basicConfig(level = logging.INFO, format = '%(filename)s %(asctime)s %(levelname)s:\t%(message)s')

    usage_instructions = f"""CryEx_psi_calculator -f fofn -e exon_coordinates -o output_file"""

    parser = optparse.OptionParser(usage = usage_instructions)

    parser.add_option('-f', dest='fofn', \
        help = 'Metadata file [required]', default = None)
    parser.add_option('-p', dest='input_PSI_file', \
        help = 'Input PSI file [required]')
    parser.add_option('-o', dest='output_file', \
        help = 'Output File')
    parser.add_option('--min_delta_psi', dest='min_delta_psi', \
        help = 'Minimum Abs PSI difference [Default=0.1]', default = 0.1, type = float)
    parser.add_option('--min_llr', dest='min_llr', \
        help = 'Minimum Log Likelihood Ratio [Default=2.0]', default = 2.0, type = float)
    parser.add_option('--min_cov', dest='min_cov', \
        help = 'Minimum coverage per sample to consider an exon [Default=10]', default = 10, type = int)

    options, args = parser.parse_args()
    RL = 100

    ### read metadata
    METADATA = pd.read_csv(options.fofn, sep = '\t')
    unique_group_values = METADATA['GROUP'].unique()

    assert len(unique_group_values) == 2, "Only two groups are allowed"

    GROUPS = {}
    for row in METADATA.itertuples():
        GROUPS[row.SAMPLE] = row.GROUP


    ### read psi file
    EXONS = defaultdict(lambda: defaultdict(list))
    psi = pd.read_csv(options.input_PSI_file, sep = '\t')
    for row in psi.itertuples():
        exon  = (row.exon_type, row.chrom, row.exon_3ss, row.exon_5ss, row.strand, row.exc_5ss, row.exc_3ss)
        exon_length = row.exon_5ss - row.exon_3ss + 1
        group = GROUPS[row.SAMPLE]        

        inc, exc =  row.jxn_inc_n + 1, row.exclusion_n + 1
        cov = inc + exc

        EXONS[exon][group].append((row.PSI, inc, exc,cov))


    ### diff splicing

    GRP1, GRP2 = unique_group_values



    outlines = []

    for exon, group_dict in EXONS.items():

        covs_r = [x[3] for x  in group_dict[GRP1] + group_dict[GRP2]]
        covs = np.array(covs_r) >= options.min_cov
        
        if np.any(covs == False):
            logging.info(f"Skipping {exon} due to low coverage {covs_r}")
            continue
        
        llr, pval = beta_binomial_llr(group_dict[GRP1], group_dict[GRP2])

        if np.isnan(llr):
            logging.info(f"Skipping {exon} cannot calculate llr")
            continue
        
        psi_grp1_lst = ','.join(map(str, [x[0] for x in group_dict[GRP1]]))
        psi_grp2_lst = ','.join(map(str, [x[0] for x in group_dict[GRP2]]))

        cov_grp1 = ','.join(map(str, [x[3] for x in group_dict[GRP1]]))
        cov_grp2 = ','.join(map(str, [x[3] for x in group_dict[GRP2]]))

        delta_psi = np.mean([x[0] for x in group_dict[GRP1]]) - np.mean([x[0] for x in group_dict[GRP2]])

        grp_diff  = f"{GRP1}-{GRP2}"
        exon = "{}\t{}:{}-{}:{}\t{},{}".format(*exon)

        if llr >= options.min_llr and abs(delta_psi) > options.min_delta_psi:
            SIG = True
        else:
            SIG = False

        outline = exon.split('\t') + [round(llr, 3), pval, SIG, round(delta_psi, 2), grp_diff, psi_grp1_lst, psi_grp2_lst, cov_grp1, cov_grp2]
        outlines.append(outline)

    COLUMNS = ['exon_type', 'exon_coords', 'flanking_jxns', 'LLR', 'Pvalue', 'Sig', 'DeltaPSI', 'DIFF', 'PSIGroup1', 'PSIGroup2', 'CovGroup1', 'CovGroup2']
    outlines_df = pd.DataFrame(outlines, columns = COLUMNS)
    rejected, adjusted_p_values, _, _ = multipletests(outlines_df.Pvalue , method='fdr_bh')

    outlines_df['Pvalue_Adj'] = adjusted_p_values
    outlines_df['Pvalue']     = outlines_df['Pvalue'].apply(lambda x: f'{x:.2e}')
    outlines_df['Pvalue_Adj'] = outlines_df['Pvalue_Adj'].apply(lambda x: f'{x:.2e}')

    outlines_df.to_csv(options.output_file, sep = '\t', index = False)
        
    logging.info(f'Calculating psi of introns')

	



if __name__ == "__main__":
	main()
