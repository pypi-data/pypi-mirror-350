""" Utility functions related to dagsim output conversions """
from typing import Any, Dict, List
import pandas as pd


def dagsim_data_to_dict_of_dict(
        dagsim_data: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
    """ Takes the dictionary generate by dagsim and transforms it

    Parameters
    ----------
    dagsim_data:
        dictionary from the Dagsim output

    Return
    ------
    transformed_data_dict: Dict[int, Dict[str, Any]]
        Dictionary of dictionary, where the outer key  are unique \
        identifiers to each simulated sequence and each dictionary \
        contains all the information to that sequence.
    """
    data_pd = pd.DataFrame(dagsim_data)
    transformed_data_dict = data_pd.to_dict(orient='index')

    return transformed_data_dict


def label_fasta_seq(
        dagsim_data: Dict[str, Any],
        no_motif_seq: List[str]) -> Dict[str, str]:
    """ Harmonize background names between motif-in-seq and empty seq

    Parameters
    ----------
    dagsim_data: Dict[str, Any]
        dictionary from the Dagsim output
    no_motif_seq: List[str]
        List of non-unique comma separated background IDs and sequences

    Return
    ------
    unique_id_seq_dict: Dict[str, str]
        Dictionary of sequences with unique IDs (both with and wo motif in)
    """
    unique_id_seq_dict = {}
    transformed_data_dict = dagsim_data_to_dict_of_dict(
        dagsim_data=dagsim_data)
    unique_id = -1
    for unique_id, info_dict in transformed_data_dict.items():
        identifier = str(unique_id) + "_" + info_dict["backgrounds"]
        motif_in_seq = info_dict["motif_in_seq"]
        unique_id_seq_dict[identifier] = motif_in_seq
    for empty_sequence in no_motif_seq:
        unique_id += 1
        identifier = str(unique_id) + "_" + empty_sequence.split(',')[0]
        unique_id_seq_dict[identifier] = empty_sequence.split(',')[1]
    return unique_id_seq_dict


def extract_info_for_bed(
        dagsim_data: Dict[str, Any]) -> List[str]:
    """ Extract information from dagsim output for creating bed files

    Parameters
    ----------
    dagsim_data: Dict[str, Any]
        dictionary from the Dagsim output

    Return
    ------
    line_list: List[str]
        List of lines in bed file
    """
    line_list = []
    transformed_data_dict = dagsim_data_to_dict_of_dict(
        dagsim_data=dagsim_data)

    for unique_id, info_dict in transformed_data_dict.items():
        num_instances = info_dict["num_instances"]
        positions = info_dict["positions"]
        orientations = info_dict["orientations"]
        names = info_dict["selected_motifs"]
        instances = info_dict["instances"]
        identifier = str(unique_id) + "_" + info_dict["backgrounds"]

        for instances_index in range(num_instances):
            orientation = \
                '+' if orientations[instances_index] == 1 else '-'
            line_list.append(
                f"{identifier}" +
                f"\t{positions[instances_index][0]}" +
                f"\t{positions[instances_index][1]}\t" +
                f"{names[instances_index]}_" +
                f"{instances[instances_index]}" +
                "\t." +
                f"\t{orientation}"
            )
    return line_list
