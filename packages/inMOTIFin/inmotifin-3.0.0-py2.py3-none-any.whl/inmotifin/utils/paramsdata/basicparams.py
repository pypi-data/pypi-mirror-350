""" Data storage for basic parameters """
from dataclasses import dataclass


@dataclass
class BasicParams:
    """ Class for keeping track of basic parameters
    """
    title: str
    workdir: str
    seed: int

    def __post_init__(self):
        if self.workdir is None:
            self.workdir = '.'
