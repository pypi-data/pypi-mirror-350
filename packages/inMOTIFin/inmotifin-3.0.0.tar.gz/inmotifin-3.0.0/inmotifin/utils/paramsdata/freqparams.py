""" Data storage for group and motif frequency parameters """
from dataclasses import dataclass


@dataclass
class FreqParams:
    """ Class for keeping track of parameters for group and motif frequencies
    """
    group_frequency_type: str
    group_frequency_range: int
    motif_frequency_type: str
    motif_frequency_range: int
    group_group_type: str
    concentration_factor: float
    group_freq_file: str
    motif_freq_file: str
    group_group_file: str

    def __post_init__(self):
        if self.group_frequency_type is None:
            self.group_frequency_type = "uniform"
        if self.motif_frequency_type is None:
            self.motif_frequency_type = "uniform"
        if self.group_group_type is None:
            self.group_group_type = "uniform"
        if self.concentration_factor is None:
            self.concentration_factor = 1
