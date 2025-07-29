# -*- coding: utf-8 -*-

"""
Base Classes and field validators that are used in the snowprofile, classes, profiles
stability_tests packages.
"""

import datetime
import typing
import logging
import re
import sys

import pydantic
import pydantic.json_schema
import pandas as pd
import numpy as np


class AdditionalData(pydantic.BaseModel):
    data: typing.Any
    origin: typing.Optional[str] = None


def force_utc(value: str | datetime.datetime | None) -> typing.Optional[datetime.datetime]:
    """
    Parse to a datetime object and force the tzinfo to be defined in a python datetime object.

    In case the tzinfo is not provided, assume UTC.
    """
    if value is None:
        return None
    if isinstance(value, str):
        if sys.version_info.major == 3 and sys.version_info.minor < 11:
            # On python <= 3.10, datetime.fromisoformat have troubles with decimal seconds as
            # prodived by some other libraries such as NiViz. Get rid of this unnecessary precision.
            m = re.match(r'([0-9]{4}-[0-9]{2}-[0-9]{2}[ T]?[0-9]{2}:[0-9]{2}:[0-9]{2})\.[0-9]*', value)
            if m is not None:
                value = m.group(1) + value[m.span(0)[1]:]
        value = datetime.datetime.fromisoformat(value)
    if value.tzinfo is None:
        return value.replace(tzinfo=datetime.timezone.utc)
    return value


def serialize_datetime(value: typing.Optional[datetime.datetime]) -> typing.Optional[str]:
    """
    Serialize datetime objects to string (with iso format).
    """
    if value is None:
        return None
    else:
        return value.isoformat(sep=' ', timespec='seconds')


datetime_with_tz = typing.Annotated[datetime.datetime,
                                    pydantic.BeforeValidator(force_utc),
                                    pydantic.PlainSerializer(serialize_datetime, return_type=typing.Optional[str])]


def force_utc_tuple(value: tuple) -> tuple:
    """
    Same as force_utc but for all elements of a tuple.
    """
    if value is None:
        return (None, None)
    r = []
    for i in range(len(value)):
        r.append(force_utc(value[i]))
    return tuple(value)


def serialize_datetime_tuple(value) -> typing.Optional[typing.List[typing.Optional[str]]]:
    """
    """
    if value is None:
        return None
    r = []
    for i in range(len(value)):
        r.append(serialize_datetime(value[i]))
    return r


datetime_tuple_with_tz = typing.Annotated[typing.Tuple[typing.Optional[datetime.datetime],
                                                       typing.Optional[datetime.datetime]],
                                          pydantic.BeforeValidator(force_utc_tuple),
                                          pydantic.PlainSerializer(
                                              serialize_datetime_tuple,
                                              return_type=typing.Optional[typing.List[typing.Optional[str]]])]


def get_dataframe_checker(_mode='Layer', **kwargs):
    """
    Checker for pandas DataFrame to be put in a ``data`` field.

    :param _mode: Point or Layer or Spectral
    :param kwargs: dict:
        keys : list of columns ot be accepted
        values : dict with constraints on the content of the columns, keys are:
            - translate: dict of replacement for values.
            - type: data type (float, int, str, etc.)
            - optional (bool): Optional or not (default is False)
            - min: for numeric types, the minimum value possible (included)
            - max: for numeric types, the maximim value possible (included)
            - nan_allowed: for numeric types, allow nan or not (default is False)
            - values: the list of accepted values
    """
    def check_dataframe(value, cls=None):
        # Check type -> ensure we have a pandas DataFrame
        if isinstance(value, dict):
            value = pd.DataFrame(value)
        elif isinstance(value, pd.DataFrame):
            value = value.copy()
        else:
            raise ValueError('data key should be a pandas DataFrame or a python dictionnary.')

        # Check columns
        columns = set(value.columns)
        if _mode == 'Layer':
            two_of_three = set(['top_height', 'bottom_height', 'thickness'])
            if len(columns.intersection(two_of_three)) == 3:
                if not (value['top_height'] - value['thickness'] == value['bottom_height']).all():
                    raise ValueError('Provided top_height, bottom_height and thickness that are inconsistent.')
            elif len(columns.intersection(two_of_three)) != 2 and columns != ('top_height'):
                raise ValueError(f'Should have 2 of three in {", ".join(two_of_three)}.')
            accepted_columns_min = set([])
            accepted_columns_max = set(['top_height', 'bottom_height', 'thickness'])
        elif _mode == "Spectral":
            accepted_columns_min = set(['min_wavelength', 'max_wavelength'])
            accepted_columns_max = accepted_columns_min
        elif _mode == 'Point':
            accepted_columns_min = set(['height'])
            accepted_columns_max = set(['height'])
        elif _mode == 'None':
            accepted_columns_min = set()
            accepted_columns_max = set()
        else:
            raise ValueError(f'Mode {_mode} unknown. The data model is ill-defined.')

        columns_min = []
        for k, v in kwargs.items():
            if 'optional' in v and v['optional']:
                continue
            else:
                columns_min.append(k)
        columns_min = set(columns_min) | accepted_columns_min
        columns_max = set(kwargs.keys()) | accepted_columns_max
        if not columns.issuperset(columns_min):
            raise ValueError(f'The data should contain at least the following columns: {", ".join(columns_min)}.')
        if not columns.issubset(columns_max):
            raise ValueError(f'The data should contain at most the following columns: {", ".join(columns_max)}.')

        # Depths processing
        # - Ensure types
        if _mode == 'Layer':
            height_keys = ['top_height', 'bottom_height', 'thickness']
        elif _mode == "Point":
            height_keys = ['height']
        elif _mode == "Spectral":
            height_keys = ['min_wavelength', 'max_wavelength']
        else:
            height_keys = []
        for key in height_keys:
            if key in columns:
                value[key] = value[key].astype('float')
        # - Completion of columns to ensure that top_height, bottom_height an dthickess are defined and coherent
        if _mode == 'Layer':
            # TODO: Reconstruct thickness from top_depth or bottom_depth if there is nan inside
            # or if only top_height is provided
            # (thickness is optional in a CAAML file)
            if 'top_height' not in columns:
                value['top_height'] = value['bottom_height'] + value['thickness']
            if 'bottom_height' not in columns:
                value['bottom_height'] = value['top_height'] - value['thickness']
            if 'thickness' not in columns:
                value['thickness'] = value['top_height'] - value['bottom_height']
        # - Ensure reasonnable values and no nan
        for key in height_keys:
            if pd.isna(value[key]).any():
                raise ValueError(f'Nan values are not allowed in {key} field')
            # For CAAML format we need to accept negative height values
            # if value[key].min() < 0:
            #     raise ValueError(f'Negative values for {key} is not accepted.')
            if _mode in ['Point', 'Layer'] and value[key].max() > 10:
                logging.warning(f'Values above 10m for {key}. Please check your data !')

        # Check other data
        for key, d in kwargs.items():
            if key not in value.columns:
                continue
            # Replace values if needed
            if 'translate' in d:
                value[key] = value[key].replace(d['translate'])
            # Check type
            _type = d['type'] if 'type' in d else 'float'
            value[key] = value[key].astype(_type)
            # Check min/max and nan presence for numeric types
            if np.issubdtype(value[key].dtype, np.number):
                # Check min/max
                if pd.isna(value[key].min()):
                    logging.warning(f'Data from key {key} is empty !')
                if 'min' in d:
                    _min = d['min']
                    if not pd.isna(value[key].min()) and value[key].min() < _min:
                        raise ValueError(f'Data from key {key} has unaccepted values (below {_min}).')
                if 'max' in d:
                    _max = d['max']
                    if not pd.isna(value[key].max()) and value[key].max() > _max:
                        raise ValueError(f'Data from key {key} has unaccepted values (above {_max}).')
                # Check nan presence
                nan_allowed = d['nan_allowed'] if 'nan_allowed' in d else False
                if not nan_allowed and pd.isna(value[key]).any():
                    raise ValueError(f'Nan values are not allowed in {key} field')
            # Check fixed allowed values if needed
            if 'values' in d:
                if not set(value[key].values).issubset(set(d['values'])):
                    raise ValueError(f'Unauthorized value for key {key}')

        if len(height_keys) > 0:
            value = value.sort_values(height_keys[0], ascending=False)

        return value

    return check_dataframe


class BaseData:
    """
    Base for classes with a data attribute of pandas DataFrame type.

    Manage the necessary functions to read, edit and dump/reload
    the data stored in the pandas DataFrame.
    """
    _data = typing.Optional[pd.DataFrame]

    @property
    def data(self) -> typing.Optional[pd.DataFrame]:
        """
        The profile data in the form of a Pandas Dataframe
        """
        if self._data is not None:
            return self._data.copy()
        else:
            return None

    @data.setter
    def data(self, value):
        checker = get_dataframe_checker(**self._data_config)
        self._data = checker(value)

    @data.deleter
    def data(self):
        self._data = None

    @pydantic.computed_field(alias='data', repr=True)
    @property
    def data_dict(self) -> typing.Optional[dict]:
        """
        The data in the form of a dictionnary.

        Useful for instance for JSON serialization
        """
        if self._data is None:
            return None
        return self._data.to_dict('list')

    @data_dict.setter
    def data_dict(self, value):
        self.data = value

    @data_dict.deleter
    def data_dict(self):
        del self.data


class BaseProfile(pydantic.BaseModel, BaseData):
    """
    Base class used for all profiles (stratigraphy, density, etc.)

    See the child class BaseProfile2 for all profiles except stratigraphy.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid',
        arbitrary_types_allowed=True)

    id: typing.Optional[str] = pydantic.Field(
        None,
        description="Unique identifier of the profile [A-Za-z0-9-]")
    name: typing.Optional[str] = pydantic.Field(
        None,
        description="Name/short description of the profile")
    related_profiles: typing.List[str] = pydantic.Field(
        [],
        description="id of related profiles")
    comment: typing.Optional[str] = pydantic.Field(
        None,
        description="General comment associated to the profile")
    record_time: typing.Optional[datetime_with_tz] = pydantic.Field(
        None,
        description="Time at which the profile was done (python datetime object).")
    record_period: datetime_tuple_with_tz = pydantic.Field(
        (None, None),
        description="Time period during which the profile was done "
        "(tuple of two python datetime object representing the begin time and end time).")
    profile_depth: typing.Optional[float] = pydantic.Field(
        None, ge=0,
        description="Total snow depth at the profile location, "
        "only if different from the general total snow depth reported in the metadata (m)")
    profile_swe: typing.Optional[float] = pydantic.Field(
        None, ge=0,
        description="SWE at the profile location, "
        "only if specific measurement at the precise location of the profile (mm or kg/m2)")
    additional_data: typing.Optional[AdditionalData] = pydantic.Field(
        None,
        description="Field to store additional data for CAAML compatibility (customData), do not use.")

    def __init__(self, data=None, data_dict=None, **kwargs):
        super().__init__(**kwargs)
        checker = get_dataframe_checker(**self._data_config)
        if data is not None:
            self._data = checker(data)
        elif data_dict is not None:
            self._data = checker(data_dict)
        else:
            raise ValueError('data key is required')


class BaseProfile2(BaseProfile):
    """
    Base class for all profiles except stratigraphy
    """
    quality_of_measurement: typing.Optional[typing.Literal[
        'Good', 'Uncertain', 'Low', 'Bad']] = pydantic.Field(
            None,
            description="Quality flag of the entire profile. See :ref:`uncertainty` for details.")
    uncertainty_of_measurement: typing.Optional[float] = pydantic.Field(
        None,
        gt = 0,
        description="Quantitative uncertainty of the entire profile (same units as ``data``). "
        "See :ref:`uncertainty` for details.")
    profile_nr: typing.Optional[int] = pydantic.Field(
        None, ge=0,
        description="Profile number (the lower is the higher priority)")


class BaseMergeable:
    """
    Implement a merge method for the pydantic data class.
    """
    def merge(self, other) -> None:
        """
        Function to merge with an object of the same type.

        Raise warnings when inconsistent data are encountered.

        Does not create a copy of the object.

        :param other: Other object of the same type
        :returns: None (merge done in-place)
        """
        # Loop on attributes
        for attr_name, attr_specs in type(self).model_fields.items():
            self._merge_attr(other, attr_name)

        # Special case of the _data key
        if hasattr(self, '_data'):
            self._merge_attr(other, '_data')

    def _merge_attr(self, other, attr_name):
        v_self = getattr(self, attr_name)
        v_other = getattr(other, attr_name)
        # 0. If all None, skip
        if v_self is None and v_other is None:
            return

        # 0. If other is None, keep the value of the reference (self)
        if v_other is None:
            return

        # 1. If one is None, use the other value
        if v_self is None and v_other is not None:
            setattr(self, attr_name, v_other)
            return

        # 2a. Special case: concatenate comments
        if 'comment' in attr_name:
            if isinstance(v_self, str) and isinstance(v_other, str):
                if v_self == v_other:
                    return

                v_new = v_self + '\n' + v_other
                setattr(self, attr_name, v_new)

        # 2b. Special case: _data key
        if attr_name == '_data' and isinstance(v_self, pd.DataFrame) and isinstance(v_other, pd.DataFrame):
            if v_self.equals(v_other):
                return
            elif len(v_other) == 0:
                return
            elif len(v_self) == 0:
                setattr(self, attr_name, v_other)
            else:
                logging.warning(f'Inconsistent data during merge between {self.__class__.__name__}.{attr_name}. '
                                'Possible data loss (not merged).')
            return

        # 3. Treatements based on type.
        # Raise warning if values are different and are merged with loss of data
        if isinstance(v_self, str) \
                or isinstance(v_self, int) or isinstance(v_self, float) \
                or isinstance(v_self, tuple) \
                or isinstance(v_self, datetime.datetime):
            if v_self == v_other:
                return  # This equality test could not be done on all data types, be careful.
            else:
                logging.warning(f'Inconsistent data during merge between {self.__class__.__name__}.{attr_name}. '
                                f'Values differ: {v_self} (reference) != {v_other} (merged)')
                return
        elif isinstance(v_self, list) and isinstance(v_other, list):
            v_new = v_self + v_other
            setattr(self, attr_name, v_new)
        elif hasattr(v_self, 'merge') and callable(v_self.merge):
            v_self.merge(v_other)
        else:
            logging.warning(f'Merge: Could not compare values of {self.__class__.__name__}.{attr_name}. '
                            'Possible data loss (not merged).')
            return
