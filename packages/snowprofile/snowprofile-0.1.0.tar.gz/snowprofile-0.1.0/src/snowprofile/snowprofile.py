# -*- coding: utf-8 -*-

import typing

import pydantic

from snowprofile.classes import Time, Observer, Location, Weather, SurfaceConditions, Environment
from snowprofile.profiles import Stratigraphy, TemperatureProfile, DensityProfile, LWCProfile, \
    SSAProfile, SSAPointProfile, HardnessProfile, HardnessPointProfile, \
    StrengthProfile, ImpurityProfile, ScalarProfile, VectorialProfile
from snowprofile.stability_tests import CTStabilityTest, ECTStabilityTest, RBStabilityTest, PSTStabilityTest, \
    ShearFrameStabilityTest
from snowprofile._base_classes import AdditionalData, BaseMergeable

__all__ = ['SnowProfile']


class SnowProfile(pydantic.BaseModel, BaseMergeable):

    """
    The base class for representing and handling a snow profile.

    Data content
    ^^^^^^^^^^^^

    General information on snow profile and snow pit
    ''''''''''''''''''''''''''''''''''''''''''''''''

    id
      A unique id to identify the snow profile (optional, str, only [a-zA-Z0-9-])

    comment
      General comment on the overall measurement (optional, str)

    profile_comment
      General comment on the snow profile (optional, str)

    time
      Time of observation (:py:class:`snowprofile.classes.Time` object)

    observer
      Observer information (:py:class:`snowprofile.classes.Observer` object)

    location
      Location information (:py:class:`snowprofile.classes.Location` object)

    weather
      Weather observations (:py:class:`snowprofile.classes.Weather` object)

    surface_conditions
      Surface conditions (penetration depths, surface features, wind surface features, etc.)
      (:py:class:`snowprofile.classes.SurfaceConditions` object)

    profile_depth
      Depth of the profile (m)

    profile_depth_std
      Standard deviation of the profile depth around the snow pit (in case of multiple measurements, m)

    profile_swe
      Total SWE (mm or kg/m2)

    profile_swe_std
      Standard deviation of the total SWE (in case of mutilple measurements, mm or kg/m2)

    new_snow_24_depth
      Depth of the new snow from the past 24h (m)

    new_snow_24_depth_std
      Standard deviation of the depth of new snow (in case of multiple measurements, m)

    new_snow_24_swe
      SWE of the new snow from the past 24h (mm or kg/m2)

    new_snow_24_swe_std
      Standard deviation of the SWE of the new snow from the past 24h (in case of mutilple measurements, mm or kg/m2)

    snow_transport
      Presence and type of snow transport
       - No snow transport
       - Modified saltation: snow transport that remains confined close to the ground
       - Drifting snow: transport up to 6ft/2m
       - Blowing snow: transport above 6ft/2m

    snow_transport_occurence_24: typing.Optional[float] = pydantic.Field(None, ge=0, le=100)

    Profiles data
    '''''''''''''

    stratigraphy_profile
      The stratigraphy profile (unique, :py:class:`snowprofile.profiles.Stratigraphy` object)

    temperature_profiles:
      Temperature profiles (list of :py:class:`snowprofile.profiles.TemperatureProfile` objects)

    density_profiles:
      Density profiles (list of :py:class:`snowprofile.profiles.DensityProfile` objects)

    lwc_profiles:
      LWC profiles (list of :py:class:`snowprofile.profiles.LWCProfile` objects)

    ssa_profiles:
      SSA profiles (list of :py:class:`snowprofile.profiles.SSAProfile` or
      :py:class:`snowprofile.profiles.SSAPointProfile` objects)

    hardness_profiles:
      Hardness profiles (list of :py:class:`snowprofile.profiles.HardnessProfile` or
      :py:class:`snowprofile.profiles.HardnessPointProfile` objects)

    strength_profiles:
      Strength profiles (list of :py:class:`snowprofile.profiles.StrengthProfile` objects)

    impurity_profiles:
      Impurity profiles (list of :py:class:`snowprofile.profiles.ImpurityProfile` objects)

    stability_tests: List of stabilty tests. See :ref:`Stability tests` for details.

    Other data
    ''''''''''

    application
      Information on the application or code that generated the profile (optional, str)

    application_version
      Version of the application or code that generated the profile (optional, str)

    profiles_comment
      Comment associated to profiles, for CAAML compatibility only, do not use (str)

    additional_data and profile_additional_data
      Room to store additional data for CAAML compatibility (customData), do not use.

    """

    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    id: typing.Optional[str] = None
    comment: typing.Optional[str] = None
    profile_comment: typing.Optional[str] = None
    time: Time = Time()
    observer: Observer = Observer()
    location: Location = Location(name='Unknown')
    environment: Environment = Environment()
    application: typing.Optional[str] = 'snowprofile'
    application_version: typing.Optional[str] = None
    profile_depth: typing.Optional[float] = pydantic.Field(None, ge=0)
    profile_depth_std: typing.Optional[float] = pydantic.Field(None, ge=0)
    profile_swe: typing.Optional[float] = pydantic.Field(None, ge=0)
    profile_swe_std: typing.Optional[float] = pydantic.Field(None, ge=0)
    new_snow_24_depth: typing.Optional[float] = pydantic.Field(None, ge=0)
    new_snow_24_depth_std: typing.Optional[float] = pydantic.Field(None, ge=0)
    new_snow_24_swe: typing.Optional[float] = pydantic.Field(None, ge=0)
    new_snow_24_swe_std: typing.Optional[float] = pydantic.Field(None, ge=0)
    snow_transport: typing.Optional[typing.Literal[
        'No snow transport',
        'Modified saltation',
        'Drifting snow',
        'Blowing snow']] = None
    snow_transport_occurence_24: typing.Optional[float] = pydantic.Field(None, ge=0, le=100)
    weather: Weather = Weather()
    surface_conditions: SurfaceConditions = SurfaceConditions()
    stratigraphy_profile: typing.Optional[Stratigraphy] = None
    temperature_profiles: typing.List[TemperatureProfile] = []
    density_profiles: typing.List[DensityProfile] = []
    lwc_profiles: typing.List[LWCProfile] = []
    ssa_profiles: typing.List[SSAProfile | SSAPointProfile] = []
    hardness_profiles: typing.List[HardnessProfile | HardnessPointProfile] = []
    strength_profiles: typing.List[StrengthProfile] = []
    impurity_profiles: typing.List[ImpurityProfile] = []
    other_scalar_profiles: typing.List[ScalarProfile] = []
    other_vectorial_profiles: typing.List[VectorialProfile] = []
    stability_tests: typing.List[
        CTStabilityTest | ECTStabilityTest | RBStabilityTest | PSTStabilityTest | ShearFrameStabilityTest] = []
    additional_data: typing.Optional[AdditionalData] = None
    profile_additional_data: typing.Optional[AdditionalData] = None
