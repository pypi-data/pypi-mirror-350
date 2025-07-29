# -*- coding: utf-8 -*-

import datetime
import re
import sys
import os.path
import configparser
import logging


def _parsematch(d, default=None):
    """
    Private function to deal with defined or undefined groups in
    regex match for the `check_and_convert_date` function.
    """
    if d is None:
        return default
    else:
        return int(d)


def check_date(date) -> datetime.datetime:
    """
    Check an input date string and return a
    `bronx.stdtypes.date.Date` object

    Accepted date formats:

    * YYYY[MM[DD[HH[MM[SS]]]]]
    * YYYY-MM-DD[ HH:MM]
    * YYYY-MM-DDTHH:MM:SS
    * Etc (exact regex in the code).

    :param date: Date to be parsed
    :type date: str
    """

    if isinstance(date, datetime.datetime):
        return date
    elif isinstance(date, str):
        # the regex that parses date format
        f1 = re.match('([0-9]{4})[-]?([0-9]{2})?[-]?([0-9]{2})?[ T]?([0-9]{2})?[ :hH]?([0-9]{2})?[ :mM]?([0-9]{2})?',
                      date)
        if f1 is None:
            raise ValueError(f'Could not parse date {date}')
        return datetime.datetime(
            _parsematch(f1.group(1)),             # Year
            _parsematch(f1.group(2), default=8),  # Month
            _parsematch(f1.group(3), default=1),  # Day
            _parsematch(f1.group(4), default=6),  # Hour
            _parsematch(f1.group(5), default=0),  # Min
            _parsematch(f1.group(6), default=0))  # Sec
    else:
        raise ValueError(f'Date should be a datetime object or a date-parseable string. Cannot parse {date}.')


def get_config():
    """
    Get a ConfigParser object of snowprofile configuration.

    Location of configuration file:

    - On UNIX systems, the config file is located in ~/.config/snowprofile.ini
    - On Windows systems, the config file is directly in user home directory
    """
    config = configparser.ConfigParser()
    if sys.platform in ['linux', 'darwin']:
        path_config = os.path.expanduser('~/.config/snowprofile.ini')
    elif sys.platform in ['win32']:
        path_config = os.path.expanduser('~/snowprofile.ini')
    else:
        return config

    if os.path.isfile(path_config):
        try:
            config.read(path_config)
        except Exception as e:
            logging.error(f'Could not load configuration file {path_config}: {e}')

    return config


def get_default_observer(key='DEFAULT'):
    """
    Parse observer details and return an Observer object
    """
    from snowprofile.classes import Observer, Person
    conf = get_config()
    observer = Observer()

    v = conf.get(key, 'observer_id', fallback=None)
    if v is not None:
        observer.source_id = v

    v = conf.get(key, 'observer_name', fallback=None)
    if v is not None:
        observer.source_name = v

    v = conf.get(key, 'observer_comment', fallback=None)
    if v is not None:
        observer.source_comment = v

    cp_id = conf.get(key, 'contact_person_id', fallback=None)
    cp_na = conf.get(key, 'contact_person_name', fallback=None)
    cp_cc = conf.get(key, 'contact_person_comment', fallback=None)
    if cp_na is not None:
        contact_person = Person(id=cp_id, name=cp_na, comment=cp_cc)
        observer.contact_persons = [contact_person, ]

    return observer
