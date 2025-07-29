# -*- coding: utf-8 -*-

"""
Various constants and common definitions.
"""

cloudiness_attribution = {
    0: 'CLR',
    1: 'FEW',
    2: 'FEW',
    3: 'SCT',
    4: 'SCT',
    5: 'BKN',
    6: 'BKN',
    7: 'BKN',
    8: 'OVC',
    -1: 'X'}
""" Conversion table between cloudinessiness and METAR """

QUALITY_FLAGS = ['Good', 'Uncertain', 'Low', 'Bad']

GRAIN_SHAPES = ["PP", "PPco", "PPnd", "PPpl", "PPsd", "PPir", "PPgp", "PPhl", "PPip", "PPrm",
                "MM", "MMrp", "MMci",
                "DF", "DFdc", "DFbk",
                "RG", "RGsr", "RGlr", "RGwp", "RGxf",
                "FC", "FCso", "FCsf", "FCxr",
                "DH", "DHcp", "DHpr", "DHch", "DHla", "DHxr",
                "SH", "SHsu", "SHcv", "SHxr",
                "MF", "MFcl", "MFpc", "MFsl", "MFcr",
                "IF", "IFil", "IFic", "IFbi", "IFrc", "IFsc"]

MANUAL_WETNESS = ['D', 'D-M', 'M', 'M-W', 'W', 'W-V', 'V', 'V-S', 'S']

manual_wetness_attribution = {
    1: 'D',
    '1': 'D',
    1.5: 'D-M',
    '1.5': 'D-M',
    2: 'M',
    '2': 'M',
    2.5: 'M-W',
    '2.5': 'M-W',
    3: 'W',
    '3': 'W',
    3.5: 'W-V',
    '3.5': 'W-V',
    4: 'V',
    '4': 'V',
    4.5: 'V-S',
    '4.5': 'V-S',
    5: 'S',
    '5': 'S'}

MANUAL_HARDNESS = ['F', 'F-4F', '4F', '4F-1F', '1F', '1F-P', 'P', 'P-K', 'K', 'K-I', 'I',
                   'F-', 'F+', '4F-', '4F+', '1F-', '1F+', 'P-', 'P+', 'K-', 'K+', 'I-', 'I+']

manual_hardness_attribution = {
    1: 'F',
    '1': 'F',
    1.5: 'F-4F',
    '1.5': 'F-4F',
    2: '4F',
    '2': '4F',
    2.5: '4F-1F',
    '2.5': '4F-1F',
    3: '1F',
    '3': '1F',
    3.5: '1F-P',
    '3.5': '1F-P',
    4: 'P',
    '4': 'P',
    4.5: 'P-K',
    '4.5': 'P-K',
    5: 'K',
    '5': 'K',
    5.5: 'K-I',
    '5.5': 'K-I',
    6: 'I',
    '6': 'I'}

aspects = {'N': 0, 'NE': 45, 'E': 90, 'SE': 135, 'S': 180,
                   'SW': 225, 'W': 270, 'NW': 315, 'n/a': None}  # degrees
wind_speed = {'C': 0, 'L': 13.5, 'M': 34.2, 'S': 51.3, 'X': 72}  # m/s

grain_sizes = {'very fine': 0.1, 'fine': 0.35, 'medium': 0.75, 'coarse': 1.5,
               'very coarse': 3.5, 'extreme': 6}  # mm

CT_scores = {'CTV': 0, 'CTE': 5, 'CTM': 14, 'CTH': 24}
