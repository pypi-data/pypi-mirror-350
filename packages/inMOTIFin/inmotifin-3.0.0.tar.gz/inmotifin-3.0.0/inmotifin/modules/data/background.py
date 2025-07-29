""" Data class for backgrounds """
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class Backgrounds:
    """ Class for keeping track of backgrounds

    Class parameters
    ----------------
    backgrounds: Dict[str, str]
        Dictionary of background IDs and sequences
    background_ids: List[str]
        List of background IDs (automatically extracted from \
        background dictionary)
    """
    backgrounds: Dict[str, str]
    background_ids: List[str] = field(init=False)

    def __post_init__(self):
        """ Define background ids as a list """
        self.background_ids = sorted(self.backgrounds.keys())
