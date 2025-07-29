""" Data storage for dimer parameters """
from typing import List
from dataclasses import dataclass


@dataclass
class DimerParams:
    """ Class for keeping track of parameters for dimers"""
    motif_files: List[str]
    jaspar_db_version: str
    dimerisation_rule_path: str
