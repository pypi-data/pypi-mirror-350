"""Utility functions related to sequences"""
from typing import List, Dict
import numpy as np


def onehot_to_str(alphabet: List[chr], motif_onehot: List[np.array]) -> str:
    """Convert one-hot encoded motif into a string motif

    Parameters
    ----------
    alphabet: List[chr]
        Allowed characters in the sequence (eg [A, C, G, T] or 'ACGT')
    motif_onehot: List[np.array]
        One-hot encoded motif

    Return
    ------
    motif: str
        Motif in string format
    """
    motif_list = []
    for base in motif_onehot:
        motif_list.append(alphabet[np.where(base == 1)[0][0]])
    motif = "".join(motif_list)
    return motif


def create_reverse_complement(
        alphabet: Dict[chr, chr],
        motif_instance: str) -> str:
    """Translate sequence to its reverse complement. Case sensitive

    Parameters
    ----------
    alphabet: Dict[chr, chr]
        Pairs of characters and their complementary pairs
        e.g. {'A':'T', 'C':'G', 'T':'A', 'G':'C'}
    motif_instance: str
        Motif sequence

    Return
    ------
    revcomp: str
        Reverse complement of motif sequence
    """
    comp_list = []
    for base in str(motif_instance):
        if base not in alphabet.keys():
            raise AssertionError(
                f"{base} is not present in the provided \
                    alphabet {alphabet}")
        comp_list.append(alphabet[base])
    revcomp_list = comp_list[::-1]
    revcomp = "".join(revcomp_list)
    return revcomp
