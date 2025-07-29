# -*- coding:  utf-8 -*-

import numpy as np

grain_color = {
    'PP': 'lime',
    'MM': 'gold',
    'DF': 'forestgreen',
    'RG': 'lightpink',
    'FC': 'lightblue',
    'DH': 'blue',
    'SH': 'fuchsia',
    'MF': 'red',
    'IF': 'cyan',
    'PPhl': 'grey',
    'PPgp': 'lime'}

grain_text = {
    "PP": "a",
    "DF": "c",
    "RG": "d",
    "FC": "e",
    "DH": "f",
    "MF": "h",
    "IF": "i",
    "SH": "g",
    "PPhl": "o",
    "RGwp": "y",
    'PPgp': 'a'}

hardness_index = {
    'F': 1,
    'F-4F': 1.5,
    '4F': 2,
    '4F-1F': 2.5,
    '1F': 3,
    '1F-P': 3.5,
    'P': 4,
    'P-K': 4.5,
    'K': 5,
    'K-I': 5.5,
    'I': 6,
    'F-': 0.7,
    'F+': 1.3,
    '4F-': 1.7,
    '4F+': 2.3,
    '1F-': 2.7,
    '1F+': 3.3,
    'P-': 3.7,
    'P+': 4.3,
    'K-': 4.7,
    'K+': 5.3,
    'I-': 5.7,
    'I+': 6.3}

hardness_base_index = {
    'F': 1,
    '4F': 2,
    '1F': 3,
    'P': 4,
    'K': 5,
    'I': 6}

hardness_values = {  # N
    0: 0,
    1: 20,
    2: 100,
    3: 250,
    4: 500,
    5: 1000,
    6: 1500}

hardness_str_values = {key: hardness_values[value] for key, value in hardness_base_index.items()}


def hardness_index_to_value(index: float) -> float:
    """
    Return a mean value in N from the hardness index
    """
    return np.interp(index, list(hardness_values.keys()), list(hardness_values.values()))


def get_grain_text(grain_type, default=''):
    if grain_type in grain_text:
        return grain_text[grain_type]
    else:
        return default


def get_grain_color(grain_type, default='white'):
    if grain_type in grain_color:
        return grain_color[grain_type]
    elif len(grain_type) > 2 and grain_type[:2] in grain_color:
        return grain_color[grain_type[:2]]
    else:
        return default


def get_hardness_index(hardness, default=1):
    """
    Get the hardness index from hardness text-code (F, 4F, 1F...).
    """
    if hardness in hardness_index:
        return hardness_index[hardness]
    else:
        return default


def get_hardness_value(hardness, default=1):
    """
    Get the mean hardness value from hardness text-code (F, 4F, 1F...).
    """
    return hardness_index_to_value(get_hardness_index(hardness))
