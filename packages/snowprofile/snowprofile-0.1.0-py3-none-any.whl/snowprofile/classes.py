# -*- coding: utf-8 -*-

import typing
import datetime

import pydantic

from snowprofile._constants import cloudiness_attribution, QUALITY_FLAGS
from snowprofile._base_classes import AdditionalData, BaseData, BaseMergeable, \
    datetime_with_tz, datetime_tuple_with_tz, get_dataframe_checker
from snowprofile._utils import get_config

__all__ = ['Person', 'Time', 'Observer', 'Location', 'Weather', 'SurfaceConditions',
           'Environment', 'SolarMask', 'SpectralAlbedo']

conf = get_config()


class Person(pydantic.BaseModel):
    """
    Class to describe a contact person
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    id: typing.Optional[str] = None
    name: typing.Optional[str] = None
    website: typing.Optional[str] = None
    comment: typing.Optional[str] = None
    additional_data: typing.Optional[AdditionalData] = None


class Time(pydantic.BaseModel, BaseMergeable):
    """
    Class to store the date and time of observation (and additional date/time considerations)

    If left empty, the time zone will be automatically filled and the time zone is assumed to be UTC.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    record_time: datetime_with_tz = pydantic.Field(
        datetime.datetime.now(),
        description="Time of the observation or measurement (python datetime object).")
    record_period: datetime_tuple_with_tz = pydantic.Field(
        (None, None),
        description="Time period of the observation "
        "(tuple of two python datetime objects giving the start time and the end time).")
    report_time: typing.Optional[datetime_with_tz] = pydantic.Field(
        None,
        description="Reporting time of the observation (python datetime object).")
    last_edition_time: typing.Optional[datetime_with_tz] = pydantic.Field(
        None,
        description="Last edition time of the observation (python datetime object).")
    comment: typing.Optional[str] = pydantic.Field(
        None,
        description="Comment on the date and time of observation (str)")
    additional_data: typing.Optional[AdditionalData] = pydantic.Field(
        None,
        description="Field to store additional data for CAAML compatibility (customData), do not use.")


class Observer(pydantic.BaseModel, BaseMergeable):
    """
    Class to store information about the observer and about the institution / lab.

    ``source`` refers to the observation institution and ``person`` to the
    observer.

    ``source_id``
      Unique identifier of the observation institution

    ``source_name``
      Name of the observation institution

    ``source_comment``
      Comment on the observation institution

    ``contact_persons``
      The list of contact persons (or observers)

    ``additional_data``
      Field to store additional data for CAAML compatibility (customData), do not use.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    source_id: typing.Optional[str] = conf.get('DEFAULT', 'observer_id', fallback=None)
    source_name: typing.Optional[str] = conf.get('DEFAULT', 'observer_name', fallback=None)
    source_website: typing.Optional[str] = None
    source_comment: typing.Optional[str] = conf.get('DEFAULT', 'observer_comment', fallback=None)
    source_additional_data: typing.Optional[AdditionalData] = None

    contact_persons: typing.List[Person] = pydantic.Field([Person(
        name=conf.get('DEFAULT', 'contact_person_name', fallback=None),
        id=conf.get('DEFAULT', 'contact_person_id', fallback=None),
        comment=conf.get('DEFAULT', 'contact_person_comment', fallback=None)), ], min_length=1)


class Location(pydantic.BaseModel, BaseMergeable):
    """
    Class to store information on the measurement location
    (geographical position and details of the observation site).

    The required field is ``name``.

    ``id``
      Unique identifier of the geographical position

    ``name``
      The name of the observation location (str)

    ``latitude``
      Latitude (degrees north)

    ``longitude``
      Longitude (degrees East)

    ``comment``
      Free comment on the location (str)

    ``elevation``
      Point elevation (meters above sea level)

    ``aspect``
      Slope aspect (degrees, int. between 0 and 360)

    ``slope``
      Slope inclination (degrees, int. between 0 and 90)

    ``point_type``
      A point type description (str)

    ``country``
      Country code according to ISO3166

    ``region``
      Region (detail in the country, optional, str)

    ``additonal_data``
      Field to store additional data for CAAML compatibility (customData), do not use.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    id: typing.Optional[str] = None
    name: str
    point_type: typing.Optional[str] = None
    aspect: typing.Optional[int] = pydantic.Field(None, ge=0, le=360)
    elevation: typing.Optional[int] = None
    slope: typing.Optional[int] = pydantic.Field(None, ge=0, lt=90)
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None
    country: typing.Optional[typing.Literal[
        "AD", "AE", "AF", "AG", "AL", "AM", "AO", "AR", "AT", "AU",
        "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ",
        "BN", "BO", "BQ", "BR", "BS", "BT", "BW", "BY", "BZ", "CA",
        "CD", "CF", "CG", "CH", "CI", "CL", "CM", "CN", "CO", "CR",
        "CU", "CV", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ",
        "EC", "EE", "EG", "ER", "ES", "ET", "FI", "FJ", "FM", "FR",
        "GA", "GB", "GD", "GE", "GH", "GL", "GM", "GN", "GQ", "GR",
        "GT", "GW", "GY", "HN", "HR", "HT", "HU", "ID", "IE", "IL",
        "IN", "IQ", "IR", "IS", "IT", "JM", "JO", "JP", "KE", "KG",
        "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KZ", "LA", "LB",
        "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA",
        "MC", "MD", "ME", "MG", "MH", "MK", "ML", "MM", "MN", "MR",
        "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA", "NE", "NG",
        "NI", "NL", "NO", "NP", "NR", "NZ", "OM", "PA", "PE", "PG",
        "PH", "PK", "PL", "PS", "PT", "PW", "PY", "QA", "RO", "RS",
        "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI",
        "SK", "SL", "SM", "SN", "SO", "SR", "SS", "ST", "SV", "SY",
        "SZ", "TD", "TG", "TH", "TJ", "TL", "TM", "TN", "TO", "TR",
        "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ",
        "VC", "VE", "VN", "VU", "WF", "WS", "YE", "ZA", "ZM", "ZW"]] = None  # ISO 3166
    region: typing.Optional[str] = None
    comment: typing.Optional[str] = None
    additional_data: typing.Optional[AdditionalData] = None

    @pydantic.field_validator('country', mode='before')
    def _preprocess_country(country: typing.Optional[str]) -> typing.Optional[str]:
        """
        Ensure country code is upper case
        """
        if country is not None:
            return country.upper()
        return None


class Weather(pydantic.BaseModel, BaseMergeable):
    """
    Class to store the weather at time of observation.

    ``cloudiness``
     The cloudiness in octas (from 0 to 8) or in the form of METAR code:
      - CLR: clear
      - FEW: few clouds
      - SCT: scattered
      - BKN: broken
      - OVC: overcast
      - X: precipitation

    ``precipitation``
     Precipitation type, in the form of METAR code:
      - **Nil: No precipitation**
      - DZ: Drizzle
      - **RA: Rain**
      - **SN: Snow** (snow flakes)
      - **SG: Snow grains** (very small opaque grains, generally less than 1 mm)
      - IC: Ice crystals
      - PE: Ice pellets
      - GR: Hail (Grèle)
      - GS: Small hail and/or graupel (Grésil, grains below 5mm)
      - UP: Unknown precipitation type
      - **RASN: Rain and snow**
      - FZRA: Freezing rain

      The precipitation type can be preceded by '-' for light intensity or '+' for heavy intensity.
      The qualifier without +/- is moderate intensity.
      For a definition and pictures of the precipitation types, see e.g.
      `the International Cloud Atlas <https://cloudatlas.wmo.int/en/hydrometeors-other-than-clouds-falling.html>`_


    ``air_temperature``
      Temperature of air (°C)

    ``air_humidity``
      Relative humidity (%)

    ``wind_speed``
      Wind speed (m/s)

    ``wind_direction``
      Wind direction (in degree, from 0 to 360)

    ``air_temperature_measurement_height``
      Height of the air temperature measurement and humidity measurement (m)

    ``wind_measurement_height``
      Height of the wind speed and direction measurement (m)

    ``comment``
      Free comment on the weather

    ``additonal_data``
      Field to store additional data for CAAML compatibility (customData), do not use.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    cloudiness: typing.Optional[typing.Literal[
        'CLR', 'FEW', 'SCT', 'BKN', 'OVC', 'X']] = None
    precipitation: typing.Optional[typing.Literal[
        "-DZ", "DZ", "+DZ", "-RA", "RA", "+RA", "-SN", "SN", "+SN",
        "-SG", "SG", "+SG", "-IC", "IC", "+IC", "-PE", "PE", "+PE",
        "-GR", "GR", "+GR", "-GS", "GS", "+GS"
        "UP", "Nil", "RASN", "FZRA"]] = None
    air_temperature: typing.Optional[float] = None
    air_humidity: typing.Optional[float] = pydantic.Field(None, ge=0, le=100)
    wind_speed: typing.Optional[float] = pydantic.Field(None, ge=0)
    wind_direction: typing.Optional[int] = pydantic.Field(None, ge=0, le=360)
    air_temperature_measurement_height: typing.Optional[float] = pydantic.Field(None, gt=0)
    wind_measurement_height: typing.Optional[float] = pydantic.Field(None, gt=0)
    comment: typing.Optional[str] = None
    additional_data: typing.Optional[AdditionalData] = None

    @pydantic.field_validator('cloudiness', mode='before')
    def _preprocess_cloudiness(cloudiness: typing.Optional[str | int]) -> typing.Optional[str]:
        """
        Ensure cloudiness is upper case and convert octas to METAR code
        """
        if cloudiness is not None:
            if isinstance(cloudiness, str):
                return cloudiness.upper()
            elif isinstance(cloudiness, int):
                if cloudiness in cloudiness_attribution:
                    return cloudiness_attribution[cloudiness]
            return cloudiness
        return None


class SpectralAlbedo(pydantic.BaseModel, BaseData, BaseMergeable):
    """
    Class to store spectral albedo data

    The data contains:
      - ``min_wavelength`` (nm)
      - ``max_wavelength`` (nm)
      - ``albedo`` (between 0 and 1)

    and optionnally ``uncertainty`` (same unit as data) and/or ``quality`` (see :ref:`uncertainty`).
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid',
        arbitrary_types_allowed=True)

    comment: typing.Optional[str] = None
    _data_config = dict(
        _mode='Spectral',
        albedo=dict(min=0, max=1),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
    )

    def __init__(self, data=None, data_dict=None, **kwargs):
        super().__init__(**kwargs)
        checker = get_dataframe_checker(**self._data_config)
        if data is not None:
            self._data = checker(data)
        elif data_dict is not None:
            self._data = checker(data_dict)
        else:
            raise ValueError('data key is required')


class SolarMask(pydantic.BaseModel, BaseData):
    """
    Class to store solar mask

    The data contains:

    - ``azimuth`` (degrees from north)
    - ``elevation`` (in degrees from horizontal)

    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid',
        arbitrary_types_allowed=True)

    _data_config = dict(
        _mode='None',
        azimuth=dict(min=0, max=360),
        elevation=dict(min=-90, max=90),
    )

    def __init__(self, data=None, data_dict=None, **kwargs):
        super().__init__(**kwargs)
        checker = get_dataframe_checker(**self._data_config)
        if data is not None:
            self._data = checker(data)
        elif data_dict is not None:
            self._data = checker(data_dict)
        else:
            raise ValueError('data key is required')


class SurfaceConditions(pydantic.BaseModel, BaseMergeable):
    """
    Class to describe the snow surface conditions.

    ``surface_roughness``
     Surface roughness according to Fierz et al., 2009:
      - rsm: smooth
      - rwa: wavy (ripples)
      - rcv: concave furrows (ablation hollows, sun cups, penitents, due to melt or sublimation)
      - rcx: conex furrows (rain or melt groves)
      - rrd: random furrows (due to wind erosion)

    ``surface_wind_features``
     Wind features observable at the surface:
      - No observable wind bedforms
      - Snowdrift around obstacles
      - Snow ripples
      - Snow waves
      - Barchan dunes
      - Dunes
      - Loose patches
      - Pits
      - Snow steps
      - Sastrugi
      - mixed
      - other

    ``surface_melt_rain_features``
     Other surface features:
      - Sun cups
      - Penitents
      - Melt or rain furrows
      - other

    ``surface_features_amplitude``
     Amplitude of the surface features (m)

    ``surface_features_amplitude_max``
     Maximum amplitude of the surface features (m)

    ``surface_features_amplitude_min``
     Minimum amplitude of the surface features (m)

    ``surface_features_wavelength``
     Wavelength of the surface features (m)

    ``surface_features_wavelength_max``
     Maximum wavelength of the surface features (m)

    ``surface_features_wavelength_min``
     Minimum wavelength of the surface features (m)

    ``surface_features_aspect``
     Orientation of surface features (degree, from 0 to 360)

    ``comment``
     Free comment on surface conditions

    ``lap_presence``
     Indication of the presence of light absorbing particule at the snow surface. Values among:
      - No LAP
      - Black Carbon
      - Dust
      - Mixed
      - other

    ``surface_temperature``
     Snow surface temperature (°C)

    ``surface_temperature_measurement_method``
     Measurement method for the surface temperature:
      - Thermometer
      - Hemispheric IR
      - IR thermometer
      - other

    ``surface_albedo``
     Snow surface albedo (0 -1)

    ``surface_albedo_comment``
     Free comment on the snow albedo

    ``spectral_albedo``
     Spectral albedo data, see :py:class:`snowprofile.classes.SpectralAlbedo`

    ``spectral_albedo_comment``
     Free comment on the spectral snow albedo

    ``penetration_foot``
     Depth of snowpack penetration by foot (float, m)

    ``penetration_ram``
     Depth of snowpack penetration with the ramsonde (probe alone) (float, m)

    ``penetration_ski``
     Depth of snowpack penetration by ski (float, m)

    ``additonal_data``
     Field to store additional data for CAAML compatibility (customData), do not use.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    surface_roughness: typing.Optional[typing.Literal[
        'rsm', 'rwa', 'rcv', 'rcx', 'rrd']] = None
    surface_wind_features: typing.Optional[typing.Literal[
        "No observable wind bedforms",
        "Snowdrift around obstacles",
        "Snow ripples",
        "Snow waves",
        "Barchan dunes",
        "Dunes",
        "Loose patches",
        "Pits",
        "Snow steps",
        "Sastrugi",
        "mixed",
        "other"]] = None
    surface_melt_rain_features: typing.Optional[typing.Literal[
        "Sun cups",
        "Penitents",
        "Melt or rain furrows",
        "other"]] = None
    surface_features_amplitude: typing.Optional[float] = pydantic.Field(None, gt=0)
    surface_features_amplitude_min: typing.Optional[float] = pydantic.Field(None, gt=0)
    surface_features_amplitude_max: typing.Optional[float] = pydantic.Field(None, gt=0)
    surface_features_wavelength: typing.Optional[float] = pydantic.Field(None, gt=0)
    surface_features_wavelength_min: typing.Optional[float] = pydantic.Field(None, gt=0)
    surface_features_wavelength_max: typing.Optional[float] = pydantic.Field(None, gt=0)
    surface_features_aspect: typing.Optional[int] = pydantic.Field(None, ge=0, le=360)
    lap_presence: typing.Optional[typing.Literal[
        "No LAP", "Black Carbon", "Dust",
        "Mixed", "other"]] = None
    surface_temperature: typing.Optional[float] = None
    surface_temperature_measurement_method: typing.Optional[typing.Literal[
        'Thermometer', 'Hemispheric IR', 'IR thermometer', 'other']] = None
    surface_albedo: typing.Optional[float] = None
    surface_albedo_comment: typing.Optional[str] = None
    spectral_albedo: typing.Optional[SpectralAlbedo] = None
    penetration_ram: typing.Optional[float] = pydantic.Field(None, ge=0)
    penetration_foot: typing.Optional[float] = pydantic.Field(None, ge=0)
    penetration_ski: typing.Optional[float] = pydantic.Field(None, ge=0)
    comment: typing.Optional[str] = None
    additional_data: typing.Optional[AdditionalData] = None


class Environment(pydantic.BaseModel, BaseMergeable):
    """
    Description of the site environment, which is independant of the date and time of observation.

    ``solar_mask``
      The solar mask at the observation site. :py:class:`snowprofile.classes.SolarMask` object.

    ``solar_mask_method_of_measurement``
     Measurement method for the solar mask
      - Theodolite
      - Manual measurement
      - From DTM
      - From DSM
      - other

    ``solar_mask_uncertainty``
     Quantitative uncertainty of the solar mask measurement.

    ``solar_mask_quality``
     Qualitative quality of the solar mask measurement

    ``solar_mask_comment``
     Free comment on the solar mask measurement

    ``bed_surface``
     Characterization of the surface below the snowpack:
      - Sea ice
      - Glacier
      - Ice cap
      - Fresh water ice
      - Wetlands
      - Grassland
      - Shrubs
      - Rocks
      - Bare ground
      - Needle litter
      - Broadleaf litter
      - Artificial surface
      - Mixed
      - Other

    ``bed_surface_comment``
      Free comment on the bed surface

    ``litter_thickness``
      Thickness of the litter, if applicable (m)

    ``ice_thickness``
      Thickness of the ice, if applicable (m)

    ``low_vegetation_height``
      Height of the low vegetation, if applicable (m)

    ``LAI``
      Leaf area index, measured at the vegetation peak (summer, m2/m2).

    ``forest_presence``
      Type of forest, if applicable:
        - Open Area
        - Broadleaf forest
        - Needle forest
        - Mixed forest
        - Shrubs
        - Other

    ``forest_presence_comment``
      Free comment to describe the forest

    ``sky_view_factor``
      In case of forest site, the sky view factor (0 - 1)

    ``tree_height``
      In case of forest site, the mean height of trees (m).

    ``solar_mask_additional_data``
      Field to store additional data for CAAML compatibility (customData), do not use.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid',
        arbitrary_types_allowed=True)

    solar_mask: typing.Optional[SolarMask] = pydantic.Field(
        None,
        description="The spectral albedo data.")
    solar_mask_method_of_measurement: typing.Optional[typing.Literal[
        "Theodolite", "Manual measurement", "From DTM", "From DSM", "other"]] = None
    solar_mask_uncertainty: typing.Optional[float] = pydantic.Field(None, ge=0)
    solar_mask_quality: typing.Optional[typing.Literal[tuple(QUALITY_FLAGS)]] = None
    solar_mask_comment: typing.Optional[str] = None
    bed_surface: typing.Optional[typing.Literal[
        "Sea ice", "Glacier", "Ice cap", "Fresh water ice",
        "Wetlands", "Grassland", "Shrubs",
        "Rocks", "Bare ground",
        "Needle litter", "Broadleaf litter",
        "Artificial surface", "Mixed", "Other"]] = None
    bed_surface_comment: typing.Optional[str] = None
    litter_thickness: typing.Optional[float] = pydantic.Field(None, ge=0)
    ice_thickness: typing.Optional[float] = pydantic.Field(None, ge=0)
    low_vegetation_height: typing.Optional[float] = pydantic.Field(None, ge=0)
    LAI: typing.Optional[float] = pydantic.Field(None, ge=0)
    forest_presence: typing.Optional[typing.Literal[
        "Open Area", "Broadleaf forest", "Needle forest",
        "Mixed forest", "Shrubs", "Other"]] = pydantic.Field(
            None,)
    forest_presence_comment: typing.Optional[str] = None
    sky_view_factor: typing.Optional[float] = pydantic.Field(None, ge=0, le=1)
    tree_height: typing.Optional[float] = pydantic.Field(None, ge=0)
    solar_mask_additional_data: typing.Optional[AdditionalData] = None
