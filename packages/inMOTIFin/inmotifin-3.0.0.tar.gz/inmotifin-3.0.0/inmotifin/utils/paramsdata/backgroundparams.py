""" Data storage for background parameters """
from typing import List
from dataclasses import dataclass
import numpy as np


@dataclass
class BackgroundParams:
    """ Class for keeping track of parameters for background"""
    b_alphabet: List[str]
    b_alphabet_prior: np.ndarray
    number_of_backgrounds: int
    length_of_backgrounds: int
    background_files: List[str]
    shuffle: str
    number_of_shuffle: int

    def __post_init__(self):
        if self.b_alphabet is None:
            self.b_alphabet = "ACGT"
        if self.b_alphabet_prior is None:
            self.b_alphabet_prior = [0.25, 0.25, 0.25, 0.25]
        if self.number_of_backgrounds is None:
            self.number_of_backgrounds = 100
        if self.length_of_backgrounds is None:
            self.length_of_backgrounds = 50
        if self.shuffle is None:
            self.shuffle = "none"
