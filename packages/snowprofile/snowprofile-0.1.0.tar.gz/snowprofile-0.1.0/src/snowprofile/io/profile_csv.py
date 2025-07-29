# -*- coding: utf-8 -*-

import pandas as pd

from snowprofile import SnowProfile
from snowprofile.profiles import DensityProfile, TemperatureProfile, HardnessPointProfile, \
    HardnessProfile, LWCProfile, SSAProfile, SSAPointProfile, StrengthProfile, ImpurityProfile, \
    ScalarProfile, VectorialProfile


def get_mapped_values(df, key, mapping):
    if "column" in mapping:
        return df[mapping["column"]] * mapping.get("scale_factor", 1)
    elif "value" in mapping:
        return mapping["value"]


class_mapper = {
    "DensityProfile": dict(classname=DensityProfile, destination = "density_profiles"),
    "TemperatureProfile": dict(classname=TemperatureProfile, destination = "temperature_profiles"),
    "HardnessPointProfile": dict(classname=HardnessPointProfile, destination = "hardness_profiles"),
    "HardnessProfile": dict(classname=HardnessProfile, destination = "hardness_profiles"),
    "LWCProfile": dict(classname=LWCProfile, destination = "lwc_profiles"),
    "SSAProfile": dict(classname=SSAProfile, destination = "ssa_profiles"),
    "SSAPointProfile": dict(classname=SSAPointProfile, destination = "ssa_profiles"),
    "StrengthProfile": dict(classname=StrengthProfile, destination = "strength_profiles"),
    "ImpurityProfile": dict(classname=ImpurityProfile, destination = "impurity_profiles"),
    "ScalarProfile": dict(classname=ScalarProfile, destination = "other_scalar_profiles"),
    "VectorialProfile": dict(classname=VectorialProfile, destination = "other_vectorial_profiles")
}


def read_csv_profile(filename, mapper={}, profile_class=None, metadata={}, **kwargs):
    """
    Read from a CSV file to create a SnowProfile object, containing the specified single profile.

    The profile is as string refering to a classe defined in the snowprofile.profiles module, namely:

     - DensityProfile :py:class:`snowprofile.profiles.DensityProfile`
     - TemperatureProfile :py:class:`snowprofile.profiles.TemperatureProfile`
     - HardnessPointProfile :py:class:`snowprofile.profiles.HardnessPointProfile`
     - HardnessProfile :py:class:`snowprofile.profiles.HardnessProfile`
     - LWCProfile :py:class:`snowprofile.profiles.LWCProfile`
     - SSAProfile :py:class:`snowprofile.profiles.SSAProfile`
     - SSAPointProfile :py:class:`snowprofile.profiles.SSAPointProfile`
     - StrengthProfile :py:class:`snowprofile.profiles.StrengthProfile`
     - ImpurityProfile :py:class:`snowprofile.profiles.ImpurityProfile`
     - ScalarProfile :py:class:`snowprofile.profiles.ScalarProfile`
     - VectorialProfile :py:class:`snowprofile.profiles.VectorialProfile`

    Example code for reading a density profile from a CSV file containing some comments at the
    begining (8 lines to skip), seperated by tabs.

    .. code-block:: python

       from snowprofile.io.profile_csv import read_csv_profile

       path_density = "densitydata_20240420.txt"

       density_mapper = dict(
           top_height = dict(
               column = "Heigth[cm]",
               scale_factor = 0.01),
           thickness = dict(
               value = 0.025
           ),
           density = dict(
               column = "Density[kg/m3]",
               scale_factor = 1)
       )

       sp = read_csv_profile(
           filename=path_density,
           sep="\\t",
           skiprows=8,
           mapper=density_mapper,
           metadata=dict(
               method_of_measurement="Snow Cutter"),
           profile_class="DensityProfile")


    Each key of the mapper dictionary should map to a key in the data argument of the profile class,
    and the corresponding dictionary should provide:

     - column: the name of the column containing the data in the CSV file
     - scale_factor: a factor to multiply the values in the column (default=1)
     - value: a constant value to be used for all the rows of the profile (alternative to column)

    metadata is a dictionary containing additional information to be added to the profile
    (it's mandatory to provide the parameter and unit keys for ScalarProfile and VectorialProfile
    for example, and when it's not mandatory, it can still be useful).

    :param filename: The filename/filepath to read.
    :type filename: str or path-like object
    :param mapper: A dictionary mapping the keys of the profile to the columns of the CSV file.
    :type mapper: dict
    :param profile_class: The class of the profile to be created
    :type profile_class: str
    :param metadata: Metadata to be added to the profile
    :param kwargs: additional arguments to be passed to the pandas.read_csv function (standard library)
    :returns: The corresponding SnowProfile object
    :rtype: `:py:class:snowprofile.SnowProfile`
    """
    # Checks
    if profile_class is None or profile_class not in class_mapper:
        raise ValueError('Should provide a valid profile_class. '
                         f'Got {profile_class} while accepted values are {", ".join(class_mapper.keys())}')

    # Parsing CSV
    df = pd.read_csv(filename, **kwargs)
    data = pd.DataFrame()
    for key, mapping in mapper.items():
        data[key] = get_mapped_values(df, key, mapping)

    # Creating SnowProfile object
    sp = SnowProfile()
    profile = class_mapper[profile_class]["classname"](data = data, **metadata)
    getattr(sp, class_mapper[profile_class]["destination"]).append(profile)

    return sp
