"""Class to add motif instance(s) to sequences
author: Kata Ferenc
email: katalitf@uio.no
"""
from typing import List, Tuple


class Inserter:
    """Class to add motif instance(s) to sequences

    Class parameters
    ----------------
    to_replace: bool
        Whether the motif instance replaces background bases, \
        alternative is to insert by extending the bakground
    """

    def __init__(self, to_replace: bool) -> None:
        """Initialize inserter

        Parameters
        ----------
        to_replace: bool
            Value whether to replace background letters with motif instances. \
            If false: insert the instances and extend the sequence
        """
        self.to_replace = to_replace

    def add_single_instance(
            self,
            sequence: str,
            motif_instance: str,
            position: int) -> str:
        """Adds a given motif_instance in a background sequence by replacing \
        existing bases or by increasing the length

        Parameters
        ----------
        sequence: str
            String of the sequence used as background
        motif_instance: str
            motif instance to insert
        position: int
            the start location where the motif to be inserted within the
            background sequence

        Return
        ------
        new_sequence: str
            Sequence with instance inserted
        """
        str_seq = list(sequence)
        if self.to_replace:
            str_seq = str_seq[0:position] + \
                list(motif_instance) + \
                str_seq[position+len(motif_instance):]
        else:
            str_seq = str_seq[:position] + \
                list(motif_instance) + \
                str_seq[position:]
        new_sequence = ''.join(str_seq)
        return new_sequence

    def generate_motif_in_sequence(
            self,
            sequence: str,
            motif_instances: List[str],
            positions: List[Tuple[int]]) -> str:
        """Function to insert all motif_instances into a background

        Parameters
        ----------
        sequence: str
            String of a background sequence to insert motif_instances to
        motif_instances: List[str]
            List of motif instance sequences
        positions: List[Tuple[int]]
            List of (start, end) position tuples. Same as \
            self.positions.positions but needed here for dagsim connections

        Return
        ------
        motived_sequence: str
            Sequence with motif instances inserted
        """
        if not self.to_replace:
            # reverse the positions to insert from the end
            # when bases are not replaced to avoid overwriting
            # the positions of the already inserted motifs
            positions.sort(reverse=True)

        for idx, motif_inst in enumerate(motif_instances):
            sequence = self.add_single_instance(
                sequence=sequence,
                motif_instance=motif_inst,
                position=positions[idx][0])
        return sequence
