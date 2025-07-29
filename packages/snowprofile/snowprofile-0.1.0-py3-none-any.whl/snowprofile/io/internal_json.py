# -*- coding: utf-8 -*-

import json
import logging


def to_dict(snowprofile):
    """
    Dump of a SnowProfile object into a JSON-serializable object
    (combination of dict, list and str).

    :param snowprofile: The SnowProfile object to dump
    :type snowprofile: `:py:class:snowprofile.SnowProfile` object
    :returns: JSON-serializable object (dict)
    """
    return snowprofile.model_dump()


def to_json(snowprofile, **kwargs) -> str:
    """
    Dump of a SnowProfile object into a JSON-encoded string

    :param snowprofile: The SnowProfile object to dump
    :type snowprofile: `:py:class:snowprofile.SnowProfile`
    :param kwargs: Arguments to be passed to the json.dumps function (standard library)
    :returns: JSON-serialized string
    :rtype: str
    """
    return json.dumps(to_dict(snowprofile), **kwargs)


def from_json(json):
    """
    Create a SnowProfile object from a JSON-encoded string.

    :param json: The JSON-encoded string
    :type json: str
    :returns: The corresponding SnowProfile object
    :rtype: `:py:class:snowprofile.SnowProfile`
    """
    from snowprofile import SnowProfile
    new = SnowProfile.model_validate_json(json)
    return new


def write_internal_json(snowprofile, filename, **kwargs):
    """
    Write the SnowProfile object into an internal JSON representation

    :param snowprofile: The SnowProfile object
    :type snowprofile: `:py:class:snowprofile.SnowProfile`
    :param filename: The filename/filepath to write
                     (warning: any existing file with the same name will be overwritten with no confirmation).
    :type filename: str or path-like object
    :param kwargs: Arguments to be passed to the json.dump function (standard library)
    :returns: The written filename
    :rtype: str
    """
    with open(filename, 'w') as ff:
        json.dump(to_dict(snowprofile), ff, **kwargs)
    logging.info(f'Written to {filename}')
    return filename


def read_internal_json(filename):
    """
    Read from an internal JSON representation to create a SnowProfile object.

    :param filename: The filename/filepath to read.
    :type filename: str or path-like object
    :param kwargs: Arguments to be passed to the json.load function (standard library)
    :returns: The corresponding SnowProfile object
    :rtype: `:py:class:snowprofile.SnowProfile`
    """
    with open(filename, 'r') as ff:
        j = json.load(ff)
    return from_json(json.dumps(j))
