""" Data storage for motif parameters """
from typing import List, Dict
from dataclasses import dataclass
import numpy as np


@dataclass
class MotifParams:
    """ Class for keeping track of parameters for motifs"""
    dirichlet_alpha: np.ndarray
    number_of_motifs: int
    length_of_motifs_min: int
    length_of_motifs_max: int
    m_alphabet: List[str]
    m_alphabet_pairs: Dict[str, str]
    motif_files: List[str]
    jaspar_db_version: str

    def __post_init__(self):
        if self.dirichlet_alpha is None:
            self.dirichlet_alpha = [1, 1, 1, 1]
        if self.number_of_motifs is None:
            self.number_of_motifs = 10
        if self.length_of_motifs_min is None:
            self.length_of_motifs_min = 5
        if self.length_of_motifs_max is None:
            self.length_of_motifs_max = self.length_of_motifs_min
        else:
            assert self.length_of_motifs_min <= self.length_of_motifs_max, \
                "length_of_motifs_min (default=5) should not be more than \
                length_of_motifs_max"
        if self.m_alphabet is None:
            self.m_alphabet = "ACGT"
        if self.m_alphabet_pairs is None:
            self.m_alphabet_pairs = {"A": "T", "C": "G", "T": "A", "G": "C"}
