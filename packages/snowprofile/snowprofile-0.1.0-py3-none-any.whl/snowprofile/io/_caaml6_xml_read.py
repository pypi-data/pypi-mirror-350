# -*- coding: utf-8 -*-

import logging
import xml.etree.ElementTree as ET
import re

from snowprofile.io._caaml_parse_utils import _parse_str, _parse_numeric, _parse_additional_data, \
    _parse_list, _parse_numeric_list, _search_gml_id, _parse_lat_lon
from snowprofile import _constants


def read_caaml6_xml(filename):
    """
    Parse a CAAML 6 XML-based IACS Snow Profile document and return the associated SnowProfile object.

    Versions up to 6.0.5 are currently supported.

    This parser correctly deal with XML namespaces. One unique namespace URI have to be used for CAAML tags across
    the entire XML file for the parser to work correctly.

    Most of the data stored in the CAAML format is parsed. However, some specific corner cases are not
    covered by this parser. Specifically, when dealing with profiles with unkown snow depth (not compulsoy in CAAML),
    the total depth may be set to 0 and the layer top/bottom height may be negative values.

    Some data is partially parsed. For instance, missing numeric data could be specified as
    inapplicable (there is no value), missing (the value is not available when the data is written and may not exist),
    template (the value will be available later), unknown(the value is not available to the data writer but exists),
    or withheld (the value cannot be disclosed). All these cases are treated in the same way, using a 
    python value ``None``. Some parameters can be represented by text rather than numeric measurements (e.g. grain size could
    be reported in mm or by categories). To facilitate data processing, when categories are used, the package translates the category value into a numerical value
    refering to the center of the category.

    Finally, CAAML may contain some additional data defined by the user. This cannot be parsed, as the structure is
    unknown. Most of this data could be stored and rewritten in a new file but not all, especially not those
    associated with layers in the different profiles.

    Hence, reading a CAAML file and rewritten it with this package may cause some data loss. Most users, however, will experience no problems in this respect.

    :param filename: File path of the CAAML/XML document to parse
    :type filename: str
    :returns: The associated SnowProfile python object (or None in case of errors)
    :rtype: SnowProfile
    """
    # XML parsing
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
    except ET.ParseError as e:
        logging.error(f"Fail to parse CAAML XML-based document {filename}. Error while parsing XML file: {str(e)}")
        return None
    # Identification of CAAML namespace
    if root.tag == "SnowProfile":  # Case no namespace
        ns = None
        nss = ''
    else:
        r = re.match('{(.*)}SnowProfile$', root.tag)
        if r is None:
            logging.error(f"The root element of {filename} is not a SnowProfile element. "
                          "This is not a valid CAAML file.")
            return None
        else:
            ns = r.group(1)
            nss = '{' + ns + '}'
    logging.debug(f"Parsing {filename}. Found CAAML namespace as {nss}")

    # Parsing part by part
    from snowprofile import SnowProfile
    from snowprofile.classes import Time, Observer, Location, Environment, Weather, SurfaceConditions

    # - Time
    time = Time(
        record_time=_parse_str(root, [f'{nss}timeRef/{nss}recordTime/{nss}TimeInstant/{nss}timePosition',
                                      f'{nss}timeRef/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition']),
        record_period=(
            _parse_str(root, f'{nss}timeRef/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition'),
            _parse_str(root, f'{nss}timeRef/{nss}recordTime/{nss}TimePeriod/{nss}endPosition')),
        report_time=_parse_str(root, f'{nss}timeRef/{nss}dateTimeReport'),
        last_edition_time=_parse_str(root, f'{nss}timeRef/{nss}dateTimeLastEdit'),
        comment=_parse_str(root, f'{nss}timeRef/{nss}metaData/{nss}comment'),
        additional_data=_parse_additional_data(root.find(f'{nss}timeRef/{nss}customData')))

    # - Observer
    observer = Observer(
        source_id=_search_gml_id(root.find(f'{nss}srcRef/{nss}Operation')),
        source_name=_parse_str(root, f'{nss}srcRef/{nss}Operation/{nss}name'),
        source_comment=_parse_str(root, f'{nss}srcRef/{nss}Operation/{nss}metaData/{nss}comment'),
        source_additional_data = _parse_additional_data(root.find(f'{nss}srcRef/{nss}Operation/{nss}customData')))
    contact_persons_1 = root.findall(f'{nss}srcRef/{nss}Operation/{nss}contactPerson')
    contact_persons_2 = root.findall(f'{nss}srcRef/{nss}Person')
    contact_persons = []
    if contact_persons_1 is not None:
        for p in contact_persons_1:
            contact_persons.append(_parse_contact_person(p, nss=nss, ns=ns))
    if contact_persons_2 is not None:
        for p in contact_persons_2:
            contact_persons.append(_parse_contact_person(p, nss=nss, ns=ns))
    if len(contact_persons) > 0:
        observer.contact_persons = contact_persons

    # - Location
    loc = root.find(f'{nss}locRef')
    lat, lon = _parse_lat_lon(loc.find(f'{nss}pointLocation'))
    location = Location(
        id=_search_gml_id(loc),
        name=_parse_str(root, f'{nss}locRef/{nss}name'),
        point_type=_parse_str(root, f'{nss}locRef/{nss}obsPointSubType'),
        aspect=_parse_numeric(root, f'{nss}locRef/{nss}validAspect/{nss}AspectPosition/{nss}position',
                              attribution_table=_constants.aspects),
        elevation=_parse_numeric(root, f'{nss}locRef/{nss}validElevation/{nss}ElevationPosition/{nss}position'),
        slope=_parse_numeric(root, f'{nss}locRef/{nss}validSlopeAngle/{nss}SlopeAnglePosition/{nss}position'),
        latitude=lat,
        longitude = lon,
        country=_parse_str(root, f'{nss}locRef/{nss}country'),
        region=_parse_str(root, f'{nss}locRef/{nss}region'),
        comment=_parse_str(root, f'{nss}locRef/{nss}metaData/{nss}comment'),
        additional_data=_parse_additional_data(root.find(f'{nss}locRef/{nss}customData')))

    # - Environment
    base = f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}weatherCond'
    environment = Environment(
        solar_mask=_parse_solar_mask(root.find(f'{nss}locRef/{nss}solarMask'), nss=nss),
        solar_mask_method_of_measurement=_parse_str(root, f'{nss}locRef/{nss}solarMask/{nss}solarMaskMetaData/{nss}methodOfMeas'),
        solar_mask_uncertainty=_parse_numeric(root, f'{nss}locRef/{nss}solarMask/{nss}solarMaskMetaData/{nss}uncertaintyOfMeas'),
        solar_mask_quality=_parse_str(root, f'{nss}locRef/{nss}solarMask/{nss}solarMaskMetaData/{nss}qualityOfMeas'),
        solar_mask_comment=_parse_str(root, f'{nss}locRef/{nss}solarMask/{nss}solarMaskMetaData/{nss}comment'),
        solar_mask_additional_data=_parse_additional_data(root.find(f'{nss}locRef/{nss}solarMask/{nss}customData')),
        bed_surface=_parse_str(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}bedSurface'),
        bed_surface_comment=_parse_str(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}bedSurfaceComment'),
        litter_thickness=_parse_numeric(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}litterThickness'),
        ice_thickness=_parse_numeric(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}iceThickness'),
        low_vegetation_height=_parse_numeric(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}lowVegetationHeight'),
        LAI=_parse_numeric(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}lai'),
        forest_presence=_parse_str(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}forestPresence'),
        forest_presence_comment=_parse_str(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}forestComment'),
        sky_view_factor=_parse_numeric(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}skyViewFactor'),
        tree_height=_parse_numeric(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}treeHeight'))

    # - Weather
    base = f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}weatherCond'
    weather = Weather(
        cloudiness=_parse_str(root, f'{base}/{nss}skyCond'),
        precipitation=_parse_str(root, f'{base}/{nss}precipTI'),
        air_temperature=_parse_numeric(root, f'{base}/{nss}airTempPres'),
        wind_speed=_parse_numeric(
            root, f'{base}/{nss}windSpd',
            attribution_table=_constants.wind_speed),
        wind_direction=_parse_numeric(
            root, f'{base}/{nss}windDir/{nss}AspectPosition/{nss}position',
            attribution_table=_constants.aspects),
        air_temperature_measurement_height=_parse_numeric(
            root,
            f'{base}/{nss}metaData/{nss}airTempMeasurementHeight'),
        wind_measurement_height=_parse_numeric(
            root,
            f'{base}/{nss}metaData/{nss}windMeasurementHeight'),
        comment = _parse_str(
            root,
            f'{base}/{nss}metaData/{nss}comment'),
        additional_data=_parse_additional_data(root.find(
            f'{base}/{nss}customData')))

    # - Surface Conditions
    base = f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}surfCond'
    surface_conditions = SurfaceConditions(
        surface_roughness=_parse_str(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}surfRoughness'),
        surface_wind_features=_parse_str(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}surfWindFeatures'),
        surface_melt_rain_features=_parse_str(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}surfMeltRainFeatures'),
        surface_features_amplitude=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validAmplitude/{nss}AmplitudePosition/{nss}position',
            factor=0.01),  # cm -> m
        surface_features_amplitude_min=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validAmplitude/{nss}AmplitudeRange/{nss}beginPosition',
            factor=0.01),  # cm -> m
        surface_features_amplitude_max=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validAmplitude/{nss}AmplitudeRange/{nss}endPosition',
            factor=0.01),  # cm -> m
        surface_features_wavelength=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validWavelength/{nss}WavelengthPosition/{nss}position',
            factor=1),  # m
        surface_features_wavelength_min=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validWavelength/{nss}WavelengthRange/{nss}beginPosition',
            factor=1),  # m
        surface_features_wavelength_max=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validWavelength/{nss}WavelengthRange/{nss}endPosition',
            factor=1),  # m
        surface_features_aspect=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validAspect/{nss}AspectPosition/{nss}position'),
        penetration_ram=_parse_numeric(
            root,
            f'{base}/{nss}penetrationRam',
            factor=0.01),  # cm -> m
        penetration_foot=_parse_numeric(
            root,
            f'{base}/{nss}penetrationFoot',
            factor=0.01),  # cm -> m
        penetration_ski=_parse_numeric(
            root,
            f'{base}/{nss}penetrationSki',
            factor=0.01),  # cm -> m
        lap_presence=_parse_str(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}lapPresence'),
        surface_temperature=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}surfTemp/{nss}data'),
        surface_temperature_measurement_method=_parse_str(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}surfTemp/{nss}methodOfMeas'),
        surface_albedo=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}surfAlbedo/{nss}albedo/{nss}albedoMeasurement'),
        surface_albedo_comment=_parse_str(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}surfAlbedo/{nss}albedo/{nss}metaData/{nss}comment'),
        spectral_albedo=_parse_spectral_albedo(
            root.find(
                f'{base}/{nss}surfFeatures/{nss}Components/{nss}surfAlbedo/{nss}spectralAlbedo'),
            nss=nss),
        comment=_parse_str(
            root,
            f'{base}/{nss}metaData/{nss}comment'),
        additional_data=_parse_additional_data(root.find(
            f'{base}/{nss}customData')))

    # Creating SnowProfile object
    base = f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}snowPackCond'

    # Profile depth is not taken by default from the profileDepth element, to be coherent
    # with NiViz.
    profile_depth = _parse_numeric(
        root,
        f'{base}/{nss}hS/{nss}Components/{nss}height',
        factor=0.01)  # cm -> m
    if profile_depth is None:
        profile_depth = _parse_numeric(
            root,
            f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}profileDepth',
            factor=0.01)

    sp = SnowProfile(
        id=_search_gml_id(root),
        comment=_parse_str(root, f'{nss}metaData/{nss}comment'),
        profile_comment=_parse_str(
            root,
            f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}metaData/{nss}comment'),
        time=time,
        observer=observer,
        location=location,
        environment=environment,
        weather=weather,
        surface_conditions=surface_conditions,
        application=_parse_str(root, f'{nss}application'),
        application_version=_parse_str(root, f'{nss}applicationVersion'),
        profile_depth=profile_depth,
        profile_depth_std=_parse_numeric(
            root,
            f'{base}/{nss}hSVariability/{nss}Components/{nss}height',
            factor=0.01),
        profile_swe=_parse_numeric(
            root,
            f'{base}/{nss}hS/{nss}Components/{nss}waterEquivalent',
            factor=1),  # kg/m2 is the only one accepted
        profile_swe_std=_parse_numeric(
            root,
            f'{base}/{nss}hSVariability/{nss}Components/{nss}waterEquivalent',
            factor=1),
        new_snow_24_depth=_parse_numeric(
            root,
            f'{base}/{nss}hN24/{nss}Components/{nss}height',
            factor=0.01),  # cm -> m
        new_snow_24_depth_std=_parse_numeric(
            root,
            f'{base}/{nss}hIN/{nss}Components/{nss}height',
            factor=0.01),
        new_snow_24_swe=_parse_numeric(
            root,
            f'{base}/{nss}hN24/{nss}Components/{nss}waterEquivalent',
            factor=1),
        new_snow_24_swe_std=_parse_numeric(
            root,
            f'{base}/{nss}hIN/{nss}Components/{nss}waterEquivalent',
            factor=1),
        snow_transport=_parse_str(
            root,
            f'{base}/{nss}snowTransport'),
        snow_transport_occurence_24=_parse_numeric(
            root,
            f'{base}/{nss}snowTransportOccurrence24'),
        stratigraphy_profile = _parse_stratigraphy(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}stratProfile'),
            nss=nss, profile_depth=profile_depth),
        temperature_profiles = _parse_temperature_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}tempProfile'),
            nss=nss, profile_depth=profile_depth),
        density_profiles = _parse_density_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}densityProfile'),
            nss=nss, profile_depth=profile_depth),
        lwc_profiles = _parse_lwc_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}lwcProfile'),
            nss=nss, profile_depth=profile_depth),
        ssa_profiles = _parse_ssa_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}specSurfAreaProfile'),
            nss=nss, profile_depth=profile_depth),
        hardness_profiles = _parse_hardness_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}hardnessProfile'),
            nss=nss, profile_depth=profile_depth),
        strength_profiles = _parse_strength_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}strengthProfile'),
            nss=nss, profile_depth=profile_depth),
        impurity_profiles = _parse_impurity_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}impurityProfile'),
            nss=nss, profile_depth=profile_depth),
        other_scalar_profiles = _parse_other_scalar_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}otherScalarProfile'),
            nss=nss, profile_depth=profile_depth),
        other_vectorial_profiles = _parse_other_vectorial_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}otherVectorialProfile'),
            nss=nss, profile_depth=profile_depth),
        stability_tests = _parse_stability_tests(
            root.find(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}stbTests'),
            nss=nss, profile_depth=profile_depth),
        additional_data=_parse_additional_data(root.find(
            f'{nss}customData')),
        profile_additional_data = _parse_additional_data(root.find(
            f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}customData')))

    return sp


def _parse_contact_person(p, nss='', ns=None):
    if p is None:
        return None
    from snowprofile.classes import Person
    return Person(
        id=_search_gml_id(p),
        name=_parse_str(p, f'{nss}name'),
        comment=_parse_str(p, f'{nss}metaData/{nss}comment'),
        additional_data=_parse_additional_data(p.find(f'{nss}customData')))


def _parse_solar_mask(sm_element, nss=''):
    if sm_element is None:
        return None

    from snowprofile.classes import SolarMask

    data = _parse_generic_profile(
        sm_element.findall(f'{nss}Data'),
        {'azimuth': {'path': f'{nss}azimuth', 'type': 'numeric'},
         'elevation': {'path': f'{nss}elevation', 'type': 'numeric'}},
        nss=nss)
    sm = SolarMask(data=data)
    return sm


def _parse_spectral_albedo(sa_element, nss=''):
    if sa_element is None:
        return None

    from snowprofile.classes import SpectralAlbedo

    e = sa_element
    data = _parse_generic_profile(
        e.findall(f'{nss}spectralAlbedoMeasurement'),
        {'min_wavelength': {'path': f'{nss}minWaveLength', 'type': 'numeric'},
         'max_wavelength': {'path': f'{nss}maxWaveLength', 'type': 'numeric'},
         'albedo': {'path': f'{nss}albedo', 'type': 'numeric'},
         'uncertainty': {'path': f'{nss}albedo', 'type': 'numeric', 'attribute': '{nss}uncertainty'},
         'quality': {'path': f'{nss}albedo', 'type': 'str', 'attribute': '{nss}quality'},
         },
        nss=nss)
    sm = SpectralAlbedo(
        data=data,
        comment=_parse_str(e, f'{nss}metaData/{nss}comment'))
    return sm


def _parse_generic_profile(elements, definitions, nss='', min_columns=[]):
    # Eventully get the height to invert depth and height !!
    if elements is None or len(elements) == 0:
        return None
    results = {}
    for key in definitions:
        results[key] = []

    for e in elements:
        for key, value in definitions.items():
            factor = value['numeric_factor'] if 'numeric_factor' in value else 1
            attribute = value['attribute'] if 'attribute' in value else None
            attribution_table = value['attribution_table'] if 'attribution_table' in value else None

            if 'type' in value and value['type'] == 'numeric':
                r = _parse_numeric(e, value['path'], factor=factor, attribute=attribute,
                                   attribution_table=attribution_table)
                if 'adapt_total_depth' in value:
                    r = value['adapt_total_depth'] - r
            elif 'type' in value and value['type'] == 'numeric_list':
                r = _parse_numeric_list(e, value['path'], factor=factor, attribute=attribute)
            else:
                r = _parse_str(e, value['path'], attribute=attribute,
                               attribution_table=attribution_table)
            results[key].append(r)

    # Get rid of columns full of None
    results = {key: value for key, value in results.items() if key in min_columns or set(value) != set([None])}

    return results


def _parse_stratigraphy(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return None

    # Metadata key
    mdk = f'{nss}stratMetaData'

    r = []

    for elem in elements:
        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            _profile_depth = profile_depth_local
        else:
            _profile_depth = profile_depth if profile_depth is not None else 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': _profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'grain_1': {'path': f'{nss}grainFormPrimary', 'type': 'str'},
             'grain_2': {'path': f'{nss}grainFormSecondary', 'type': 'str'},
             'grain_size': {'path': f'{nss}grainSize/{nss}Components/{nss}avg', 'type': 'numeric',
                            'numeric_factor': 0.001,  # mm -> m
                            'attribution_table': _constants.grain_sizes},
             'grain_size_max': {'path': f'{nss}grainSize/{nss}Components/{nss}avgMax', 'type': 'numeric',
                                'numeric_factor': 0.001,
                                'attribution_table': _constants.grain_sizes},
             'hardness': {'path': f'{nss}hardness', 'type': 'str'},
             'wetness': {'path': f'{nss}wetness', 'type': 'str'},
             'loc': {'path': f'{nss}layerOfConcern', 'type': 'str'},
             'comment': {'path': f'{nss}metaData/{nss}comment', 'type': 'str'},
             'formation_time': {'path': f'{nss}validFormationTime/{nss}TimeInstant/{nss}timePosition', 'type': 'str'},
             'formation_period_begin': {'path': f'{nss}validFormationTime/{nss}TimePeriod/{nss}beginPosition',
                                        'type': 'str'},
             'formation_period_end': {'path': f'{nss}validFormationTime/{nss}TimePeriod/{nss}endPosition',
                                      'type': 'str'}},
            min_columns=['grain_1', 'grain_size', 'hardness', 'grain_2', 'wetness'],
            nss=nss)

        from snowprofile.profiles import Stratigraphy
        s = Stratigraphy(
            id=_search_gml_id(elem),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData')),
            data = data)
        r.append(s)

    return r[0] if len(r) > 0 else None


def _parse_temperature_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    # Metadata key
    mdk = f'{nss}tempMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            _profile_depth = profile_depth_local
        else:
            _profile_depth = profile_depth if profile_depth is not None else 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Obs'),
            {'height': {'path': f'{nss}depth', 'type': 'numeric',
                        'numeric_factor': 0.01, 'adapt_total_depth': _profile_depth},
             'temperature': {'path': f'{nss}snowTemp', 'type': 'numeric'},
             'uncertainty': {'path': f'{nss}uncertaintyOfMeas', 'type': 'str'},
             'quality': {'path': f'{nss}qualityOfMeas', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import TemperatureProfile
        s = TemperatureProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{nss}tempMetaData/{nss}uncertaintyOfMeas'),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData')),
            data = data)
        r.append(s)

    return r


def _parse_density_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    # Metadata key
    mdk = f'{nss}densityMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            _profile_depth = profile_depth_local
        else:
            _profile_depth = profile_depth if profile_depth is not None else 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': _profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'density': {'path': f'{nss}density', 'type': 'numeric'},
             'uncertainty': {'path': f'{nss}density', 'attribute': 'uncertainty', 'type': 'str'},
             'quality': {'path': f'{nss}density', 'attribute': 'quality', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import DensityProfile
        s = DensityProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            probed_volume = _parse_numeric(elem, f'{mdk}/{nss}probeVolume', factor=1e-6),
            probed_diameter = _parse_numeric(elem, f'{mdk}/{nss}probeDiameter', factor=0.01),
            probed_length = _parse_numeric(elem, f'{mdk}/{nss}probeLength', factor=0.01),
            probed_thickness = _parse_numeric(elem, f'{mdk}/{nss}probedThickness', factor=0.01),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData')),
            data = data)
        r.append(s)

    return r


def _parse_lwc_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    # Metadata key
    mdk = f'{nss}lwcMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            _profile_depth = profile_depth_local
        else:
            _profile_depth = profile_depth if profile_depth is not None else 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': _profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'lwc': {'path': f'{nss}lwc', 'type': 'numeric'},
             'uncertainty': {'path': f'{nss}lwc', 'attribute': 'uncertainty', 'type': 'str'},
             'quality': {'path': f'{nss}lwc', 'attribute': 'quality', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import LWCProfile
        s = LWCProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            probed_thickness = _parse_numeric(elem, f'{mdk}/{nss}probedThickness', factor=0.01),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData')),
            data = data)
        r.append(s)

    return r


def _parse_ssa_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    # Metadata key
    mdk = f'{nss}specSurfAreaMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            _profile_depth = profile_depth_local
        else:
            _profile_depth = profile_depth if profile_depth is not None else 0

        metadata = dict(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            probed_thickness = _parse_numeric(elem, f'{mdk}/{nss}probedThickness', factor=0.01),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData')))

        from snowprofile.profiles import SSAProfile, SSAPointProfile

        # Layer profile of SSA
        data1 = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': _profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'ssa': {'path': f'{nss}specSurfArea', 'type': 'numeric'},
             'uncertainty': {'path': f'{nss}specSurfArea', 'attribute': 'uncertainty', 'type': 'str'},
             'quality': {'path': f'{nss}specSurfArea', 'attribute': 'quality', 'type': 'str'}},
            nss=nss)

        if data1 is not None and 'top_height' in data1 and len(data1['top_height']) > 0:
            s = SSAProfile(
                **metadata,
                data = data1)
            r.append(s)

        # Point profile of SSA
        height = []
        ssa = []
        e = elem.find(f'{nss}Measurements/{nss}tupleList')
        if e is not None:
            t = e.text
            try:
                for x in t.split(' '):
                    if len(x.strip()) == 0:
                        continue
                    _tuple = x.split(',')
                    _height = _profile_depth - float(_tuple[0]) / 100
                    _ssa = float(_tuple[1])
                    height.append(_height)
                    ssa.append(_ssa)
            except IndexError:
                logging.error('Could not parse the SSA Profile. tupleList is not well formatted '
                              '(not two element at least in the tuple List (depth adn SSA).'
                              f' Value: {_tuple}')
            except ValueError:
                logging.error('Could not parse the SSA Profile. tupleList is not well formatted '
                              '(element of the tuple list that is not recognized as a float value).'
                              f' Value: {_tuple}')
        if len(height) > 0:
            s = SSAPointProfile(
                **metadata,
                data = {'height': height, 'ssa': ssa})
            r.append(s)

    return r


def _parse_hardness_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    # Metadata key
    mdk = f'{nss}hardnessMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            _profile_depth = profile_depth_local
        else:
            _profile_depth = profile_depth if profile_depth is not None else 0

        metadata = dict(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            surface_of_indentation = _parse_numeric(elem, f'{mdk}/{nss}surfOfIndentation', factor=0.0001),
            penetration_speed = _parse_numeric(elem, f'{mdk}/{nss}penetrationSpeed', factor=1),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData')))

        from snowprofile.profiles import HardnessProfile, HardnessPointProfile

        # Ramsonde Profile of Hardness
        data1 = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': _profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'hardness': {'path': f'{nss}hardness', 'type': 'numeric'},
             'weight_hammer': {'path': f'{nss}weightHammer', 'type': 'numeric'},
             'weight_tube': {'path': f'{nss}weightTube', 'type': 'numeric'},
             'n_drops': {'path': f'{nss}nDrops', 'type': 'numeric'},
             'drop_height': {'path': f'{nss}dropHeight', 'type': 'numeric',
                             'numeric_factor': 0.01}},  # cm -> m
            nss=nss)

        if data1 is not None and 'top_height' in data1 and len(data1['top_height']) > 0:
            s = HardnessProfile(
                **metadata,
                data = data1)
            r.append(s)

        # Point profile of Hardness
        height = []
        res = []
        e = elem.find(f'{nss}Measurements/{nss}tupleList')
        if e is not None:
            t = e.text
            try:
                for x in t.split(' '):
                    if len(x.strip()) == 0:
                        continue
                    _tuple = x.split(',')
                    _height = _profile_depth - float(_tuple[0]) / 100
                    _res = float(_tuple[1])
                    height.append(_height)
                    res.append(_res)
            except IndexError:
                logging.error('Could not parse the Hardness Profile. tupleList is not well formatted '
                              '(not two element at least in the tuple List (depth adn SSA).'
                              f' Value: {_tuple}')
            except ValueError:
                logging.error('Could not parse the Hardness Profile. tupleList is not well formatted '
                              '(element of the tuple list that is not recognized as a float value).'
                              f' Value: {_tuple}')
        if len(height) > 0:
            s = HardnessPointProfile(
                **metadata,
                data = {'height': height, 'hardness': res})
            r.append(s)

    return r


def _parse_strength_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    # Metadata key
    mdk = f'{nss}strengthMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            _profile_depth = profile_depth_local
        else:
            _profile_depth = profile_depth if profile_depth is not None else 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': _profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'strength': {'path': f'{nss}strengthValue', 'type': 'numeric'},
             'fracture_character': {'path': f'{nss}fractureCharacter', 'type': 'str'},
             'uncertainty': {'path': f'{nss}strengthValue', 'attribute': 'uncertainty', 'type': 'str'},
             'quality': {'path': f'{nss}strengthValue', 'attribute': 'quality', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import StrengthProfile
        s = StrengthProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            probed_area = _parse_numeric(elem, f'{mdk}/{nss}probedArea', factor=1e-4),
            strength_type = _parse_str(elem, f'{mdk}/{nss}strengthType'),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData')),
            data = data)
        r.append(s)

    return r


def _parse_impurity_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    # Metadata key
    mdk = f'{nss}impurityMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            _profile_depth = profile_depth_local
        else:
            _profile_depth = profile_depth if profile_depth is not None else 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': _profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'mass_fraction': {'path': f'{nss}massFraction', 'type': 'numeric'},
             'volume_fraction': {'path': f'{nss}volumeFraction', 'type': 'numeric'},
             'uncertainty': {'path': [f'{nss}volumeFraction', f'{nss}massFraction'],
                             'attribute': 'uncertainty', 'type': 'str'},
             'quality': {'path': [f'{nss}volumeFraction', f'{nss}massFraction'],
                         'attribute': 'quality', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import ImpurityProfile
        s = ImpurityProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            impurity_type = _parse_str(elem, f'{mdk}/{nss}impurity'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            probed_volume = _parse_numeric(elem, f'{mdk}/{nss}probedVolume', factor=1e-6),
            probed_diameter = _parse_numeric(elem, f'{mdk}/{nss}probedDiameter', factor=0.01),
            probed_length = _parse_numeric(elem, f'{mdk}/{nss}probedLength', factor=0.01),
            probed_thickness = _parse_numeric(elem, f'{mdk}/{nss}probedThickness', factor=0.01),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData')),
            data = data)
        r.append(s)

    return r


def _parse_other_scalar_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    # Metadata key
    mdk = f'{nss}otherScalarMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            _profile_depth = profile_depth_local
        else:
            _profile_depth = profile_depth if profile_depth is not None else 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': _profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'data': {'path': f'{nss}value', 'type': 'numeric'},
             'uncertainty': {'path': f'{nss}value', 'attribute': 'uncertainty',
                             'type': 'str'},
             'quality': {'path': f'{nss}value', 'attribute': 'quality', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import ScalarProfile
        s = ScalarProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            parameter = _parse_str(elem, f'{mdk}/{nss}parameter'),
            unit = _parse_str(elem, f'{mdk}/{nss}uom'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData')),
            data = data)
        r.append(s)

    return r


def _parse_other_vectorial_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    # Metadata key
    mdk = f'{nss}otherVectorialMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            _profile_depth = profile_depth_local
        else:
            _profile_depth = profile_depth if profile_depth is not None else 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': _profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'data': {'path': f'{nss}value', 'type': 'numeric_list'},
             'uncertainty': {'path': f'{nss}value', 'attribute': 'uncertainty',
                             'type': 'str'},
             'quality': {'path': f'{nss}value', 'attribute': 'quality', 'type': 'str'}},
            nss=nss, min_columns=['top_height', 'data'])

        from snowprofile.profiles import VectorialProfile
        s = VectorialProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            parameter = _parse_str(elem, f'{mdk}/{nss}parameter'),
            unit = _parse_str(elem, f'{mdk}/{nss}uom'),
            rank = _parse_numeric(elem, f'{mdk}/{nss}rank'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePeriod/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData')),
            data = data)
        r.append(s)

    return r


def _parse_stability_tests(element, nss='', profile_depth=0):
    if element is None:
        return []

    r = []

    # RB tests
    for elementtest in element.findall(f'{nss}RBlockTest'):
        from snowprofile.stability_tests import RBStabilityTest, RBStabilityTestResult
        _results = []
        for e in elementtest.findall(f'{nss}failedOn'):
            test_score = _parse_str(e, f'{nss}Results/{nss}testScore')
            m = re.match('RB([0-7])', test_score)
            if m is None:
                logging.error(f'Could not parse Rutschblock score {test_score}.')
                continue
            test_score = int(m.group(1))
            _s = RBStabilityTestResult(
                **_parse_generic_stability_test_result_fields(e, nss=nss, profile_depth=profile_depth),
                test_score = test_score,
                release_type = _parse_str(e, f'{nss}Results/{nss}releaseType'),
                fracture_character = _parse_str(e, f'{nss}Results/{nss}fractureCharacter'))
            _results.append(_s)
        s = RBStabilityTest(
            **_parse_generic_stability_test_fields(elementtest, nss=nss, profile_depth=profile_depth),
            results = _results)
        r.append(s)

    # CT tests
    for elementtest in element.findall(f'{nss}ComprTest'):
        from snowprofile.stability_tests import CTStabilityTest, CTStabilityTestResult
        _results = []
        for e in elementtest.findall(f'{nss}failedOn'):
            test_score = _parse_str(e, f'{nss}Results/{nss}testScore', attribution_table=_constants.CT_scores)
            try:
                test_score = int(test_score)
            except ValueError:
                logging.error(f'Could not parse ECT score {test_score}.')
                continue
            _s = CTStabilityTestResult(
                **_parse_generic_stability_test_result_fields(e, nss=nss, profile_depth=profile_depth),
                test_score = test_score,
                fracture_character = _parse_str(e, f'{nss}Results/{nss}fractureCharacter'))
            _results.append(_s)
        s = CTStabilityTest(
            **_parse_generic_stability_test_fields(elementtest, nss=nss, profile_depth=profile_depth),
            results = _results)
        r.append(s)

    # ECT tests
    for elementtest in element.findall(f'{nss}ExtColumnTest'):
        from snowprofile.stability_tests import ECTStabilityTest, ECTStabilityTestResult
        _results = []
        for e in elementtest.findall(f'{nss}failedOn'):
            test_score = _parse_str(e, f'{nss}Results/{nss}testScore')
            if test_score == 'ECTPV':
                test_score = 0
                propagation = True
            else:
                m = re.match('ECT([NP])([0-9]*)', test_score)
                if m is None:
                    logging.error(f'Could not parse Rutschblock score {test_score}.')
                    continue
                test_score = int(m.group(2))
                propagation = m.group(1) == 'P'
            _s = ECTStabilityTestResult(
                **_parse_generic_stability_test_result_fields(e, nss=nss, profile_depth=profile_depth),
                test_score = test_score,
                propagation = propagation)
            _results.append(_s)
        s = ECTStabilityTest(
            **_parse_generic_stability_test_fields(elementtest, nss=nss, profile_depth=profile_depth),
            results = _results)
        r.append(s)

    # PST tests
    for elementtest in element.findall(f'{nss}PropSawTest'):
        from snowprofile.stability_tests import PSTStabilityTest
        e = elementtest.find(f'{nss}failedOn')
        if e is not None:
            s = PSTStabilityTest(
                **_parse_generic_stability_test_fields(elementtest, nss=nss, profile_depth=profile_depth),
                **_parse_generic_stability_test_result_fields(e, nss=nss, profile_depth=profile_depth),
                column_length = _parse_numeric(e, f'{nss}Results/{nss}columnLength', factor=0.01),
                cut_length = _parse_numeric(e, f'{nss}Results/{nss}cutLength', factor=0.01),
                propagation = _parse_str(e, f'{nss}Results/{nss}fracturePropagation'))
            r.append(s)

    # Shear frame tests
    for elementtest in element.findall(f'{nss}ShearFrameTest'):
        from snowprofile.stability_tests import ShearFrameStabilityTest, ShearFrameStabilityTestResult
        _results = []
        for e in elementtest.findall(f'{nss}failedOn'):
            _s = ShearFrameStabilityTestResult(
                **_parse_generic_stability_test_result_fields(e, nss=nss, profile_depth=profile_depth),
                force = _parse_numeric(e, f'{nss}Results/{nss}failureForce'),
                fracture_character = _parse_str(e, f'{nss}Results/{nss}fractureCharacter'))
            _results.append(_s)
        s = ShearFrameStabilityTest(
            **_parse_generic_stability_test_fields(elementtest, nss=nss, profile_depth=profile_depth),
            results = _results)
        r.append(s)

    return r


def _parse_generic_stability_test_fields(elem, nss='', profile_depth=0):
    return dict(
        id=_search_gml_id(elem),
        name = _parse_str(elem, path='.', attribute='name'),
        test_nr = _parse_numeric(elem, path=f'{nss}testNr'),
        comment = _parse_str(elem, f'{nss}metaData/{nss}comment'),
        additional_data = _parse_additional_data(elem.find(f'{nss}customData')))


def _parse_generic_stability_test_result_fields(elem, nss='', profile_depth=0):
    depth = _parse_numeric(elem, f'{nss}Layer/{nss}depthTop', factor = 0.01)
    return dict(
        height = profile_depth - depth if depth is not None else None,
        layer_thickness = _parse_numeric(elem, f'{nss}Layer/{nss}thickness', factor = 0.01),
        grain_1 = _parse_str(elem, f'{nss}Layer/{nss}grainFormPrimary'),
        grain_2 = _parse_str(elem, f'{nss}Layer/{nss}grainFormSecondary'),
        grain_size = _parse_numeric(elem, f'{nss}Layer/{nss}grainSize/{nss}Components/{nss}avg', factor=0.001,
                                    attribution_table=_constants.grain_sizes),
        grain_size_max = _parse_numeric(elem, f'{nss}Layer/{nss}grainSize/{nss}Components/{nss}avgMax', factor=0.001,
                                        attribution_table=_constants.grain_sizes),
        layer_formation_time = _parse_str(elem,
                                          f'{nss}Layer/{nss}validFormationTime/{nss}TimeInstant/{nss}timePosition'),
        layer_formation_period = (
            _parse_str(elem, f'{nss}Layer/{nss}validFormationTime/{nss}TimePeriod/{nss}beginPosition'),
            _parse_str(elem, f'{nss}Layer/{nss}validFormationTime/{nss}TimePeriod/{nss}endPosition')),
        layer_comment = _parse_str(elem, f'{nss}Layer/{nss}metaData/{nss}comment'),
        layer_additional_data = _parse_additional_data(elem.find(f'{nss}Layer/{nss}customData')))
