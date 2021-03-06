"""
Tests samutils module(s)
"""

from wgbs_tools import samutils
import os
import gzip


def test_chr_bam_to_permeth(test_bam, tmpdir, correct_chr1bed):
    """Tests bam_to_permeth in samutils"""
    chrom = 'chr1'
    bed_prefix = 'test_'
    out_bed = '{}{}_{}.bed.gz'.format(str(tmpdir), bed_prefix, chrom)
    genome = 'mm10'
    meth_type = 'CG'
    strand_type = 'both'
    max_dup_reads = 1
    chrom_length = 99999999
    samutils.chr_bam_to_permeth(test_bam, out_bed, bed_prefix, genome,
                                meth_type, strand_type, max_dup_reads, chrom,
                                chrom_length)
    with gzip.open(out_bed, 'r') as content_file:
        testcontent = content_file.read()
        assert testcontent == correct_chr1bed, \
            'BAM to Percent Methylation conversion is not working correctly.'


def test_bam_to_permeth(test_bam, tmpdir, correct_chr1bed,
                        correct_chr2bed, correct_chrNHbed):
    """Tests multiprocessing of sam to permethbed conversion"""
    chroms = {'chr1': 99999999, 'chr2': 99999999, 'chrNH': 5}
    bed_prefix = 'test_'
    out_prefix = os.path.join(str(tmpdir), bed_prefix)
    # out_prefix = 'test_'
    genome = 'mm10'
    meth_type = 'CG'
    strand_type = 'both'
    max_dup_reads = 1
    threads = 1
    samutils.bam_to_permeth(test_bam, out_prefix, bed_prefix, genome, meth_type,
                            strand_type, max_dup_reads, chroms, threads)
    out_bed = '{}chr1.bed.gz'.format(out_prefix)
    with gzip.open(out_bed, 'r') as content_file:
        testcontent = content_file.read()
        assert testcontent == correct_chr1bed, \
            'BAM to Percent Methylation conversion is not working correctly, ' \
            'Bed file: {}'.format(out_bed)
    out_bed = '{}chr2.bed.gz'.format(out_prefix)
    with gzip.open(out_bed, 'r') as content_file:
        testcontent = content_file.read()
        assert testcontent == correct_chr2bed, \
            'BAM to Percent Methylation conversion is not working correctly ' \
            'for multiprocessing.'
    out_bed = '{}chrNH.bed.gz'.format(out_prefix)
    with gzip.open(out_bed, 'r') as content_file:
        testcontent = content_file.read()
        assert testcontent == correct_chrNHbed, \
            'Multiprocess permeth creation not working for empty chromosome ' \
            'information.'

def test_bam_to_permeth_pe(testpe_bam, tmpdir, correctpe_chr1bed,
                           correctpe_chr2bed, correctpe_chrNHbed):
    """Tests sam to permethbed conversion of paired end reads"""
    chroms = {'1': 99999999, '2': 99999999, 'chrNH': 5}
    bed_prefix = 'test_'
    out_prefix = os.path.join(str(tmpdir), bed_prefix)
    genome = 'bosTau6'
    meth_type = 'CG'
    strand_type = 'both'
    max_dup_reads = 1
    threads = 1
    samutils.bam_to_permeth(testpe_bam, out_prefix, bed_prefix, genome,
                            meth_type, strand_type, max_dup_reads, chroms,
                            threads)
    out_bed = '{}1.bed.gz'.format(out_prefix)
    with gzip.open(out_bed, 'r') as content_file:
        testcontent = content_file.read()
        assert testcontent == correctpe_chr1bed, \
            'BAM to Percent Methylation conversion is not working correctly.'
    out_bed = '{}2.bed.gz'.format(out_prefix)
    with gzip.open(out_bed, 'r') as content_file:
        testcontent = content_file.read()
        assert testcontent == correctpe_chr2bed, \
            'BAM to Percent Methylation conversion is not working correctly ' \
            'for multiprocessing.'
    out_bed = '{}chrNH.bed.gz'.format(out_prefix)
    with gzip.open(out_bed, 'r') as content_file:
        testcontent = content_file.read()
        assert testcontent == correctpe_chrNHbed, \
            'Multiprocess permeth creation not working for empty chromosome ' \
            'information.'
