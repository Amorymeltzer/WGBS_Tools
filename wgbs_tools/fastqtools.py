"""
Module containing all scripts that process and manipulate fastq files.
"""

import subprocess
import logging
import gzip


def qual_filter_fastq(in_fastq, out_fastq):
    """
    Filters a fastq file based on the Y/N flag in the header line of each read.

    :param in_fastq: Input fastq file name. If ends in .gz, assumed gzipped.
    Otherwise, it is assumed unzipped.
    :param out_fastq: Output fastq file name. If ends in .gz, it will zip the
    resulting file. Otherwise, it is left unzipped.
    :return: String denoting completion of function or if the fastq file did
    not have a field for Illumina quality calls in the header lines.
    """

    # Checks to see if the fastq file has Illumina quality calls
    if out_fastq.endswith('.gz'):
        with gzip.open(in_fastq, 'r') as infq:
            first_line = infq.readline()
    else:
        with open(in_fastq, 'r') as infq:
            first_line = infq.readline()
    if ':Y:' not in first_line and ':N:' not in first_line:
        logging.info('no_qual_field')
        return

    # Filters fastq file
    if in_fastq.endswith(".gz"):
        if out_fastq.endswith(".gz"):
            command = 'gunzip -c {} | grep -A 3 \'^@.* [^:]*:N:[^:]*:\' |   ' \
                      'grep -v "^--$" | gzip > {}'.format(in_fastq, out_fastq)
        else:
            command = 'gunzip -c {} | grep -A 3 \'^@.* [^:]*:N:[^:]*:\' |   ' \
                      'grep -v "^--$" > {}'.format(in_fastq, out_fastq)
    else:
        if out_fastq.endswith(".gz"):
            command = 'cat {} | grep -A 3 \'^@.* [^:]*:N:[^:]*:\' |   ' \
                      'grep -v "^--$" | gzip > {}'.format(in_fastq, out_fastq)
        else:
            command = 'cat {} | grep -A 3 \'^@.* [^:]*:N:[^:]*:\' |   ' \
                      'grep -v "^--$" > {}'.format(in_fastq, out_fastq)
    logging.info(command)
    subprocess.check_call(command, shell=True)


def adapter_remove(in_fastq, noadap_fq, adaptrim_fq, adap_seq, chew_length=10,
                   min_seqlength=35):
    """
    Separates fastq files for those with and without adapter sequence.

    If the reads did not contain adapter sequence, they are trimmed back
    chew_length bases. Otherwise, the reads that have adapter sequence are
    cut at the sequence and then trimmed back chew_length bases.

    :param in_fastq: input fastq file (can be .gz or uncompressed)
    :param noadap_fq: output fastq file name containing all reads without
    adapter sequence in them. Trimmed back chew_length.
    :param adaptrim_fq: output fastq file name containing all reads that had
    adapter sequence in them. The sequence was trimmed out and trimmed back
    chew_length.
    :param adap_seq: Sequence of adapter that is used to filter for
    adapter contamination.
    :param chew_length: Length of read that gets removed after adapter
    sequence is found.
    :param min_seqlength: Minimum sequence length the read must be in order
    to be kept. Any read shorter than this length will be thrown out before
    writing to the adaptrim_fq file.
    :return:
    """
    #Opens write files (in either normal or compressed format)
    if noadap_fq.endswith('.gz'):
        noadap_outfile = gzip.open(noadap_fq, 'wb')
    else:
        noadap_outfile = open(noadap_fq, 'wb')
    if adaptrim_fq.endswith('.gz'):
        trimmed_outfile = gzip.open(adaptrim_fq, 'wb')
    else:
        trimmed_outfile = open(adaptrim_fq, 'wb')
    with open(in_fastq, 'r') as fastq_in_file:
        for header_line in fastq_in_file:
            seq_line = next(fastq_in_file)
            seq_line = seq_line[:-1]
            third_line = next(fastq_in_file)
            qual_line = next(fastq_in_file)
            qual_line = qual_line[:-1]
            seq_trimmed = seq_line.split(adap_seq)
            if len(seq_trimmed[0]) == len(seq_line):
                noadap_outfile.write(header_line)
                noadap_outfile.write('{}\n'.format(seq_line[:-chew_length]))
                noadap_outfile.write(third_line)
                noadap_outfile.write('{}\n'.format(qual_line[:-chew_length]))
            else:
                trimmed_seq_line = seq_trimmed[0][:-chew_length]
                if len(trimmed_seq_line) >= min_seqlength:
                    qline_len = len(trimmed_seq_line)
                    trimmed_outfile.write(header_line)
                    trimmed_outfile.write('{}\n'.format(trimmed_seq_line))
                    trimmed_outfile.write(third_line)
                    trimmed_outfile.write('{}\n'.format(qual_line[:qline_len]))
    noadap_outfile.close()
    trimmed_outfile.close()

#
# def pe_adapter_remove(fin_fastq, fnoadap_fq, fadaptrim_fq, fadap_seq,
#                       rin_fastq, rnoadap_fq, radaptrim_fq, radap_seq,
#                       chew_length=10, min_seqlength=35):
#     """
#     Separates fastq files for those with and without adapter sequence.
#
#     If the reads did not contain adapter sequence, they are trimmed back
#     chew_length bases. Otherwise, the reads that have adapter sequence are
#     cut at the sequence and then trimmed back chew_length bases.
#
#     :param in_fastq: input fastq file (can be .gz or uncompressed)
#     :param noadap_fq: output fastq file name containing all reads without
#     adapter sequence in them. Trimmed back chew_length.
#     :param adaptrim_fq: output fastq file name containing all reads that had
#     adapter sequence in them. The sequence was trimmed out and trimmed back
#     chew_length.
#     :param adap_seq: Sequence of adapter that is used to filter for
#     adapter contamination.
#     :param chew_length: Length of read that gets removed after adapter
#     sequence is found.
#     :param min_seqlength: Minimum sequence length the read must be in order
#     to be kept. Any read shorter than this length will be thrown out before
#     writing to the adaptrim_fq file.
#     :return:
#     """
#     #Opens write files (in either normal or compressed format)
#     if noadap_fq.endswith('.gz'):
#         noadap_outfile = gzip.open(noadap_fq, 'wb')
#     else:
#         noadap_outfile = open(noadap_fq, 'wb')
#     if adaptrim_fq.endswith('.gz'):
#         trimmed_outfile = gzip.open(adaptrim_fq, 'wb')
#     else:
#         trimmed_outfile = open(adaptrim_fq, 'wb')
#     with open(in_fastq, 'r') as fastq_in_file:
#         for header_line in fastq_in_file:
#             seq_line = next(fastq_in_file)
#             seq_line = seq_line[:-1]
#             third_line = next(fastq_in_file)
#             qual_line = next(fastq_in_file)
#             qual_line = qual_line[:-1]
#             seq_trimmed = seq_line.split(adap_seq)
#             if len(seq_trimmed[0]) == len(seq_line):
#                 noadap_outfile.write(header_line)
#                 noadap_outfile.write('{}\n'.format(seq_line[:-chew_length]))
#                 noadap_outfile.write(third_line)
#                 noadap_outfile.write('{}\n'.format(qual_line[:-chew_length]))
#             else:
#                 trimmed_seq_line = seq_trimmed[0][:-chew_length]
#                 if len(trimmed_seq_line) >= min_seqlength:
#                     qline_len = len(trimmed_seq_line)
#                     trimmed_outfile.write(header_line)
#                     trimmed_outfile.write('{}\n'.format(trimmed_seq_line))
#                     trimmed_outfile.write(third_line)
#                     trimmed_outfile.write('{}\n'.format(qual_line[:qline_len]))
#     noadap_outfile.close()
#     trimmed_outfile.close()
#     import multiprocessing as mp
#     import time
#
#     fn = 'c:/temp/temp.txt'
#
#     def worker(arg, q):
#         '''stupidly simulates long running process'''
#         start = time.clock()
#         s = 'this is a test'
#         txt = s
#         for i in xrange(200000):
#             txt += s
#         done = time.clock() - start
#         with open(fn, 'rb') as f:
#             size = len(f.read())
#         res = 'Process' + str(arg), str(size), done
#         q.put(res)
#         return res
#
#     def listener(q):
#         '''listens for messages on the q, writes to file. '''
#
#         f = open(fn, 'wb')
#         while 1:
#             m = q.get()
#             if m == 'kill':
#                 f.write('killed')
#                 break
#             f.write(str(m) + '\n')
#             f.flush()
#         f.close()
#
#     def main():
#         # must use Manager queue here, or will not work
#         manager = mp.Manager()
#         q = manager.Queue()
#         pool = mp.Pool(mp.cpu_count() + 2)
#
#         # put listener to work first
#         watcher = pool.apply_async(listener, (q,))
#
#         # fire off workers
#         jobs = []
#         for i in range(80):
#             job = pool.apply_async(worker, (i, q))
#             jobs.append(job)
#
#         # collect results from the workers through the pool result queue
#         for job in jobs:
#             job.get()
#
#         # now we are done, kill the listener
#         q.put('kill')
#         pool.close()
