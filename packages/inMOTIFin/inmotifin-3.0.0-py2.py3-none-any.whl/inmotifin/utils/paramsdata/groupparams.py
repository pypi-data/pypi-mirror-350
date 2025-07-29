""" Data storage for group parameters """
from typing import List
from dataclasses import dataclass
import math


@dataclass
class GroupParams:
    """ Class for keeping track of parameters for groups"""
    number_of_groups: int
    max_group_size: int
    group_size_binom_p: float
    group_motif_assignment_file: List[str]

    def __post_init__(self):
        if self.number_of_groups is None:
            self.number_of_groups = 1
        if self.max_group_size is None:
            self.max_group_size = math.inf
        if self.group_size_binom_p is None:
            self.group_size_binom_p = 1
