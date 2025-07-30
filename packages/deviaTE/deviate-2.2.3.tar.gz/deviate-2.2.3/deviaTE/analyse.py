import logging
import re
from typing import Any
from collections import defaultdict

import numpy as np
from numpy.typing import NDArray

import deviaTE.paf
from deviaTE.utils import reverse_complement, find_blocks_generic



incr_type = defaultdict[Any, list]


class CoverageConverter:

    def __init__(self, qt: int = 0):
        """
        Class that handles the conversion of read mappings to coverage counts of nucleotides
        :param qt: Minimum quality threshold to count observations
        """
        # set up translation dict for bases
        transDict = {'A': '0', 'C': '1', 'G': '2', 'T': '3', 'N': '4'}
        self.base2int = str.maketrans(transDict)
        # translation dict for qualities (phred encoded)
        transDict_qual = {chr(min(126, q + 33)): f'{q},' for q in range(94)}
        self.qual2int = str.maketrans(transDict_qual)
        # and a translation dict for the cigar ops
        transDict_cig = {'M': '0', 'D': '1', 'I': '2', 'S': '3', 'N': '4'}
        self.cig2int = str.maketrans(transDict_cig)
        # compile regex for cigar ops
        self.cigar_regex = re.compile("(\d+)([MIDNSHP=XB])")
        # quality threshold
        self.qt = qt



    def convert_records(
            self,
            paf_dict: deviaTE.paf.paf_dict_type,
            ) -> incr_type:
        """
        Convert mappings to coverage counts
        :param paf_dict: Dict of mappings
        :return: Defaultdict of lists of coverage counts per target seq
        """
        # container to collect increments per contig
        increments = defaultdict(list)
        # loop through all reads
        read_ids = list(paf_dict.keys())
        for rid in read_ids:
            # grab paf records
            recs = paf_dict[rid]
            for rec in recs:
                # range of coverage of the mapping
                start = min(rec.tstart, rec.tend)
                end = max(rec.tstart, rec.tend)
                # handle strands
                if rec.rev:   # reverse
                    seq = reverse_complement(rec.seq)
                    qual = rec.qual[::-1]
                    offcut = rec.qlen - rec.qend
                else:
                    seq = rec.seq
                    qual = rec.qual
                    offcut = rec.qstart
                # get array of counts for each base and indels
                query_arr, qual_arr = self._parse_cigar(
                    cigar_string=rec.cigar,
                    read_string=seq,
                    qual_string=qual,
                    offcut=offcut
                )
                # make sure the arrays are the correct length
                assert (end - start) == query_arr.shape[0]
                assert (end - start) == qual_arr.shape[0]
                # eliminate low qual coverage
                addition = np.ones(shape=query_arr.shape[0])
                addition[np.where(qual_arr < self.qt)] = 0
                # collect increments
                increments[rec.tname].append((start, end, query_arr, addition))
        return increments



    def _parse_cigar(
            self,
            cigar_string: str,
            read_string: str,
            qual_string: str,
            offcut: int
            ) -> tuple[NDArray, NDArray]:
        """
        Parse cigar string to integer base observations
        :param cigar_string: A CIGAR string
        :param read_string: Read that the CIGAR string describes
        :param qual_string: string of base qualities (phred)
        :param offcut: piece of the read at the start, which did not map. Offset for the query_pos
        :return: tuple of integerised base and quality arrays of query at each pos
        """
        # translate sequence and qualities to integers
        read_integer = read_string.translate(self.base2int)
        int_seq = np.frombuffer(read_integer.encode(), 'u1') - ord('0')
        if not qual_string:
            qual_string = '~' * len(read_string)
        qual_integer = qual_string.translate(self.qual2int)
        # int_qual = np.frombuffer(qual_integer.encode(), 'u1') - ord('0')
        int_qual = np.array(qual_integer.split(',')[:-1], dtype="uint8")
        # split up the cigar
        lengths, ops = self._prep_cigar(cigar_string)
        # loop cigar operators
        query_array, qual_array = self._loop_cigar(
            cigar_lengths=lengths,
            cigar_ops=ops,
            int_seq=int_seq,
            int_qual=int_qual,
            qpos=offcut
        )
        return np.array(query_array), np.array(qual_array)



    def _prep_cigar(self, cigar_string: str) -> tuple[NDArray, NDArray]:
        """
        Get arrays for lengths and codes of cigar ops
        :param cigar_string: CIGAR string of an alignment
        :return: Tuple of arrays for lengths and codes of cigar operations
        """
        # takes a cigar string and returns arrays for lengths and opcodes
        # first split cigar into tuples of length, opcode
        parts = self.cigar_regex.findall(cigar_string)
        # cast into lists
        lengths, ops = zip(*parts)
        # convert to array
        lengths_arr = np.array(lengths, dtype=np.uint32)
        # for the opcodes, first put them into a string and translate to integers
        ops_seq = ''.join(ops)
        ops_tr = ops_seq.translate(self.cig2int)
        opsSeq = np.frombuffer(ops_tr.encode(), 'u1') - ord('0')
        return lengths_arr, opsSeq



    #@njit
    def _loop_cigar(
            self,
            cigar_lengths: NDArray,
            cigar_ops: NDArray,
            int_seq: NDArray,
            int_qual: NDArray,
            qpos: int
            ) -> tuple[list, list]:
        """
        Parse a cigar string given it's deconstructed components
        :param cigar_lengths: Array of length of operations
        :param cigar_ops: Array of cigar operations
        :param int_seq: Interget sequence of read
        :param int_qual: Integer quality of read
        :param qpos: Offcut length
        :return: Tuple of query and quality lists
        """
        query = []
        qual = []
        for count, operation in zip(cigar_lengths, cigar_ops):
            # MATCH
            if operation == 0:
                query.extend(int_seq[qpos: qpos + count])
                qual.extend(int_qual[qpos: qpos + count])
                qpos += count
            # GAP
            elif operation == 1 or operation == 4:
                query.extend([4] * count)
                qual.extend([20] * count)
            # INSERTION
            elif operation == 2:
                # query.extend([5] * count)
                # qual.extend([20] * count)
                qpos += count
            # OTHER, e.g. softclip
            elif operation == 3:
                # query.extend([6] * count)
                # qual.extend([20] * count)
                qpos += count
            else:
                logging.info(f'Invalid cigar operation {operation}')
        return query, qual





def get_internal_deletions(paf_dict: deviaTE.paf.paf_dict_type) -> defaultdict:
    """
    Find internal deletions in the alignments
    :param paf_dict: Input paf dictionary
    :return: internal deletion ranges
    """
    # container to collect the deletions
    internal_deletions = defaultdict(list)

    for rid, rec_list in paf_dict.items():
        # nothing to do if there is only one record
        if len(rec_list) == 1:
            continue

        # double check that we have only mappings on one contig and strand
        targets = set([rec.tname for rec in rec_list])
        assert len(targets) == 1
        strands = set([rec.strand for rec in rec_list])
        assert len(strands) == 1

        # fill an array so that we can get the gaps
        tranges = [(rec.tstart, rec.tend) for rec in rec_list]
        tstarts = [rec.tstart for rec in rec_list]
        tends = [rec.tend for rec in rec_list]

        tranges_arr = np.zeros(shape=max(tends) + 1)
        # fill up until the first alignment
        tranges_arr[0: min(tstarts)] = 1
        # fill the alignments
        for start, end in tranges:
            tranges_arr[start:end] = 1

        # find the blocks of deletions
        blocks = find_blocks_generic(tranges_arr, 0, 20)
        for bstart, bend in blocks:
            internal_deletions[rec_list[0].tname].append((bstart, bend))

    return internal_deletions



def collapse_internal_deletions(int_dels: defaultdict) -> defaultdict:
    """
    Collapse internal deletions that have almost the same coordinates

    :param int_dels: defaultdict of internal deletions per contig
    :return: collapsed internal deletions
    """
    # loop the contigs
    int_dels_coll = defaultdict(list)

    for contig, dels in int_dels.items():
        # sort the deletions
        dels.sort(key=lambda x: x[0])
        # add counts to increment after
        for i in range(len(dels)):
            dels[i] = (dels[i][0], dels[i][1], 1)

        # loop the deletions
        i = 0
        while i < len(dels) - 1:
            # check if the next deletion is almost the same
            if abs(dels[i + 1][0] - dels[i][0]) < 5:
                # merge the deletions
                dels[i] = (dels[i][0], dels[i][1], dels[i][2] + 1)
                # remove the next deletion
                dels.pop(i + 1)
            else:
                i += 1

        int_dels_coll[contig] = dels

    return int_dels_coll


