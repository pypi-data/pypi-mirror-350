""" Data storage for positioning parameters """
from typing import List
from dataclasses import dataclass


@dataclass
class PositionParams:
    """ Class for keeping track of parameters for positioning"""
    position_type: str
    position_means: List[int]
    position_variances: List[float]
    to_replace: bool

    def __post_init__(self):
        if self.position_type is None:
            self.position_type = "uniform"
