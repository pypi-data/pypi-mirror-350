# -*- coding: utf-8 -*-

import logging
import json

import numpy as np

from snowprofile import _constants

table_versions_uri = {
    '6.0.0': 'http://caaml.org/Schemas/SnowProfileIACS/v6.0/json/CAAML_SnowProfileSchema.json'}

_density_mom = {'6.0.0': ['Snow Tube', 'Snow Cylinder', 'Snow Cutter', 'Denoth Probe', 'other']}
_lwc_mom = {'6.0.0': ['Denoth Probe', 'Snow Fork', 'other']}
_ssa_mom = {'6.0.0': ['Ice Cube', 'other']}
_hardness_mom = {'6.0.0': ['SnowMicroPen', 'Ram Sonde', 'Push-Pull Gauge', 'other']}
_impurity_mom = {'6.0.0': ['other']}
_impurity_type = {'6.0.0': ['Black Carbon', 'Dust', 'Isotopes']}
_strength_mom = {'6.0.0': ['Shear Frame', 'other']}
_strength_type = {'6.0.0': ['compressive', 'tensile', 'shear']}


def write_caaml6_json(snowprofile, filename, version='6.0.0', indent=False):
    """
    Write a SnowProfile object into a CAAML 6 JSON-based IACS Snow Profile document.

    Currently supported versions:

    - 6.0.0 (default)

    :param snowprofile: A SnowProfile object to dump to a CAAML file
    :type snowprofile: SnowProfile
    :param filename: The filename to write into. If already exists, will be overwritten.
    :type filename: str
    :param indent: Visually indent the output (default: False, provide the more compact outut available)
    :type indent: bool or string (spaces for indentation)
    """
    # Id management
    id_list = []

    def _gen_id(id, default=None):
        if id is None and default is not None:
            return _gen_id(default)
        elif id is None and default is None:
            return _gen_id('id')
        else:
            i = 1
            id_test = id
            while id_test in id_list:
                id_test = f'{id}{i}'
                i += 1
            id = id_test
            id_list.append(id)
            return id

    def _get_snowdepth(s_p):
        if s_p.profile_depth is not None:
            return s_p.profile_depth
        elif snowprofile.profile_depth is not None:
            return snowprofile.profile_depth
        else:
            return 0

    # JSON output construction
    jo = {}

    jo['id'] = _gen_id(snowprofile.id, default='snowprofile')

    if snowprofile.application is not None or snowprofile.application_version is not None:
        jo['application'] = {}
        if snowprofile.application is not None:
            jo['application']['name'] = snowprofile.application
        if snowprofile.application_version is not None:
            jo['application']['version'] = snowprofile.application_version

    # Time
    jo['time'] = {}
    jo['time']['recordTime'] = snowprofile.time.record_time.isoformat()
    if snowprofile.time.report_time is not None:
        jo['time']['reportTime'] = snowprofile.time.report_time.isoformat()
    if snowprofile.time.last_edition_time is not None:
        jo['time']['lastEditTime'] = snowprofile.time.last_edition_time.isoformat()
    if snowprofile.time.comment is not None:
        jo['time']['metaData'] = {'comment': snowprofile.time.comment}
    _append_additional_data(jo['time'], snowprofile.time.additional_data)

    jo['source'] = {}
    if snowprofile.observer.source_name is None:
        # We suppose we have only one person
        e_s = jo['source']['person']  = {}
        e_s['name'] = snowprofile.observer.contact_persons[0].name
        if snowprofile.observer.contact_persons[0].comment is not None:
            e_s['metaData'] = {
                'comment': snowprofile.observer.contact_persons[0].comment}
        if snowprofile.observer.contact_persons[0].website is not None:
            e_s['website'] = snowprofile.observer.contact_persons[0].website
    else:
        e_s = jo['source']['provider'] = {}
        e_s['name'] = snowprofile.observer.source_name
        if snowprofile.observer.source_website is not None:
            e_s['website'] = snowprofile.observer.source_website
        e_s['contactPerson'] = []
        for p in snowprofile.observer.contact_persons:
            cp = {}
            if p.name is not None:
                cp['name'] = p.name
            if p.website is not None:
                cp['website'] = p.website
            if p.comment is not None:
                cp['metaData'] = {'comment': p.name}
            e_s['contactPerson'].append(cp)
        if snowprofile.observer.source_comment is not None:
            e_s['metaData'] = {'comment': snowprofile.observer.comment}
        _append_additional_data(e_s, snowprofile.observer)

    # Location
    e_l = jo['location'] = {}
    e_l['name'] = snowprofile.location.name
    if snowprofile.location.elevation is not None:
        e_l['elevation'] = snowprofile.location.elevation
    if snowprofile.location.aspect is not None:
        e_l['aspect'] = snowprofile.location.aspect
    if snowprofile.location.slope is not None:
        e_l['slopeAngle'] = snowprofile.location.slope
    if snowprofile.location.latitude is not None and snowprofile.location.longitude is not None:
        e_l['coordinates'] = {
            'lat': snowprofile.location.latitude,
            'long': snowprofile.location.longitude}
    if snowprofile.location.country is not None:
        e_l['country'] = snowprofile.location.country
    if snowprofile.location.region is not None:
        e_l['region'] = snowprofile.location.region
    if snowprofile.location.comment is not None:
        e_l['metaData'] = {'comment': snowprofile.location.comment}
    _append_additional_data(e_l, snowprofile.location.additional_data)

    # Measurements
    e_spm = jo['snowProfileMeasurements'] = {}

    # - Weather
    e_w = e_spm['weatherCondition'] = {}
    if snowprofile.weather.cloudiness is not None:
        e_w['skyCondition'] = snowprofile.weather.cloudiness
    # TODO: Precitipation type  <28-03-25, Léo Viallon-Galinier> #
    # if snowprofile.weather.precipitation is not None:
    #     e_w['precipitationType'] = snowprofile.weather.precipitation
    if snowprofile.weather.air_temperature is not None:
        e_w['airTemperature'] = snowprofile.weather.air_temperature
    if snowprofile.weather.wind_speed is not None:
        e_w['windSpeed'] = snowprofile.weather.wind_speed
    if snowprofile.weather.wind_direction is not None:
        e_w['windDirection'] = snowprofile.weather.wind_direction
    if snowprofile.weather.comment is not None:
        e_w['metaData'] = {'comment': snowprofile.weather.comment}
    _append_additional_data(e_w, snowprofile.weather.additional_data)

    # - Snowpack
    e_s = e_spm['snowPackCondition'] = {}
    if snowprofile.profile_depth is not None or snowprofile.profile_swe is not None:
        _ = e_s['heightSnow'] = {}
        if snowprofile.profile_depth is not None:
            _['height'] = snowprofile.profile_depth * 100
        if snowprofile.profile_swe is not None:
            _['height'] = snowprofile.profile_swe
    if snowprofile.new_snow_24_depth is not None or snowprofile.new_snow_24_swe is not None:
        _ = e_s['height24h'] = {}
        if snowprofile.new_snow_24_depth is not None:
            _['height'] = snowprofile.new_snow_24_depth * 100
        if snowprofile.new_snow_24_swe is not None:
            _['height'] = snowprofile.new_snow_24_swe
    if snowprofile.profile_depth_std is not None or snowprofile.profile_swe is not None:
        _ = e_s['heightIrregular'] = {}
        if snowprofile.profile_depth_std is not None:
            _['height'] = snowprofile.profile_depth_std * 100
        if snowprofile.profile_swe_std is not None:
            _['height'] = snowprofile.profile_swe_std
    if snowprofile.profile_comment is not None:
        e_s['metaData'] = {'comment': snowprofile.profile_comment}
    _append_additional_data(e_s, snowprofile.surface_conditions.additional_data)

    # - Surface
    e_s = e_spm['surfaceCondition'] = {}
    if snowprofile.surface_conditions.surface_roughness is not None:
        _ = e_s['surfaceFeatures'] = {}
        _['surfaceRoughness'] = snowprofile.surface_conditions.surface_roughness
        if snowprofile.surface_conditions.surface_features_amplitude is not None:
            _['amplitude'] = {'position': snowprofile.surface_conditions.surface_features_amplitude * 100}
        elif (snowprofile.surface_conditions.surface_features_amplitude_min is not None
              and snowprofile.surface_conditions.surface_features_amplitude_min is not None):
            _['amplitude'] = {
                'beginposition': snowprofile.surface_conditions.surface_features_amplitude_min * 100,
                'endposition': snowprofile.surface_conditions.surface_features_amplitude_min * 100}
        if snowprofile.surface_conditions.surface_features_wavelength is not None:
            _['wavelength'] = {'position': snowprofile.surface_conditions.surface_features_wavelength * 100}
        elif (snowprofile.surface_conditions.surface_features_wavelength_min is not None
              and snowprofile.surface_conditions.surface_features_wavelength_min is not None):
            _['wavelength'] = {
                'beginposition': snowprofile.surface_conditions.surface_features_wavelength_min,
                'endposition': snowprofile.surface_conditions.surface_features_wavelength_min}
    if snowprofile.surface_conditions.penetration_ram is not None:
        e_s['penetrationRam'] = snowprofile.surface_conditions.penetration_ram * 100  # cm
    if snowprofile.surface_conditions.penetration_foot is not None:
        e_s['penetrationFoot'] = snowprofile.surface_conditions.penetration_foot * 100
    if snowprofile.surface_conditions.penetration_ski is not None:
        e_s['penetrationSki'] = snowprofile.surface_conditions.penetration_ski * 100
    if snowprofile.surface_conditions.comment is not None:
        e_s['metaData'] = {'comment': snowprofile.surface_conditions.comment}

    # - stratigraphicProfile
    if snowprofile.stratigraphy_profile is not None and len(snowprofile.stratigraphy_profile.data) > 0:
        s_p = snowprofile.stratigraphy_profile
        profile_depth = _get_snowdepth(s_p)
        e_sp = e_spm['stratigraphicProfile'] = {}
        e_sp['layers'] = []
        for _, layer in s_p.data.iterrows():
            l = {}
            l['depthTop'] = (profile_depth - layer.top_height) * 100  # cm
            if not np.isnan(layer.thickness):
                l['thickness'] = layer.thickness * 100  # cm
            if 'grain_1' in layer and layer.grain_1 is not None:
                l['grainFormPrimary'] = layer.grain_1
            if 'grain_2' in layer and layer.grain_2 is not None:
                l['grainFormSecondary'] = layer.grain_2
            if 'grain_size' in layer and layer.grain_size is not None:
                l['grainSize'] = {'avg': layer.grain_size * 1e3}
                if 'grain_size_max' in layer and layer.grain_size_max is not None:
                    l['grainSize']['max'] = layer.grain_size_max * 1e3
            if 'formation_time' in layer and layer.formation_time is not None:
                l['validformationTime'] = layer.formation_time.isoformat()
            if 'comment' in layer and layer.comment is not None:
                l['metaData'] = {'comment': layer.comment}
            if 'additional_data' in layer:
                _append_additional_data(l, layer.additional_data)
            if layer.hardness is not None:
                l['hardness'] = layer.hardness
            if layer.wetness is not None:
                l['wetness'] = layer.wetness
            e_sp['layers'].append(l)
        if s_p.comment is not None:
            e_sp['metaData'] = {'comment': s_p.comment}
        _append_additional_data(e_sp, s_p.additional_data)

    # - temperatureProfile
    if len(snowprofile.temperature_profiles) > 0:
        if len(snowprofile.temperature_profiles) > 1:
            logging.warning('CAAML JSON v{version} does not allow for several temperature profiles, '
                            'only the ifrst one will be kept.')
        s_p = snowprofile.temperature_profiles[0]
        profile_depth = _get_snowdepth(s_p)
        if len(s_p.data) > 0:
            e_sp = e_spm['temperatureProfile'] = {}
            if s_p.uncertainty_of_measurement is not None:
                e_sp['uncertaintyOfMeasurement'] = s_p.uncertainty_of_measurement

            e_sp['measurements'] = []
            for _, layer in s_p.data.iterrows():
                e_sp['measurements'].append(
                    {
                        'temperature': layer.temperature,
                        'depth': (profile_depth - layer.height) * 100})  # cm

            if s_p.comment is not None:
                e_sp['metaData'] = {'comment': s_p.comment}
            _append_additional_data(e_sp, s_p.additional_data)

    # - densityProfiles
    if len(snowprofile.density_profiles) > 0:
        e_spm['densityProfiles'] = []
        for s_p in snowprofile.density_profiles:
            profile_depth = _get_snowdepth(s_p)
            if len(s_p.data) > 0:
                e_p = {}
                e_p['methodOfMeasurement'] = _get_value(s_p.method_of_measurement, _density_mom[version], 'other')
                if s_p.uncertainty_of_measurement is not None:
                    e_p['uncertaintyOfMeasurement'] = s_p.uncertainty_of_measurement
                if s_p.probed_volume is not None:
                    e_p['probeVolume'] = s_p.probed_volume * 1e6  # cm3
                if s_p.probed_diameter is not None:
                    e_p['probeDiameter'] = s_p.probed_diameter * 100  # cm
                if s_p.probed_length is not None:
                    e_p['probeLength'] = s_p.probed_length * 100  # cm
                if s_p.probed_thickness is not None:
                    e_p['probedThickness'] = s_p.probed_thickness * 100  # cm
                if s_p.profile_nr is not None:
                    e_p['profile_nr'] = s_p.profile_nr

                e_p['layers'] = []
                for _, layer in s_p.data.iterrows():
                    l = {
                        'depthTop': (profile_depth - layer.top_height) * 100,
                        'density': layer.density}
                    if not np.isnan(layer.thickness):
                        l['thickness'] = layer.thickness * 100
                    e_p['layers'].append(l)

                if s_p.comment is not None:
                    e_p['metaData'] = {'comment': s_p.comment}
                _append_additional_data(e_p, s_p.additional_data)
                e_spm['densityProfiles'].append(e_p)

    # - liquidWaterContentProfile
    if len(snowprofile.lwc_profiles) > 0:
        e_spm['liquidWaterContentProfiles'] = []
        for s_p in snowprofile.lwc_profiles:
            profile_depth = _get_snowdepth(s_p)
            if len(s_p.data) > 0:
                e_p = {}
                e_p['methodOfMeasurement'] = _get_value(s_p.method_of_measurement, _lwc_mom[version], 'other')
                if s_p.uncertainty_of_measurement is not None:
                    e_p['uncertaintyOfMeasurement'] = s_p.uncertainty_of_measurement
                if s_p.probed_thickness is not None:
                    e_p['probedThickness'] = s_p.probed_thickness * 100  # cm
                if s_p.profile_nr is not None:
                    e_p['profile_nr'] = s_p.profile_nr

                e_p['layers'] = []
                for _, layer in s_p.data.iterrows():
                    l = {
                        'depthTop': (profile_depth - layer.top_height) * 100,
                        'liquidWaterContent': layer.lwc}
                    if not np.isnan(layer.thickness):
                        l['thickness'] = layer.thickness * 100
                    e_p['layers'].append(l)

                if s_p.comment is not None:
                    e_p['metaData'] = {'comment': s_p.comment}
                _append_additional_data(e_p, s_p.additional_data)
                e_spm['liquidWatercontentProfiles'].append(e_p)

    # - specificSurfaceAreaProfiles
    from snowprofile.profiles import SSAProfile, SSAPointProfile
    if len(snowprofile.ssa_profiles) > 0:
        e_spm['specificSurfaceAreaProfiles'] = []
        for s_p in snowprofile.ssa_profiles:
            profile_depth = _get_snowdepth(s_p)
            if len(s_p.data) > 0:
                e_p = {}
                e_p['methodOfMeasurement'] = _get_value(s_p.method_of_measurement, _ssa_mom[version], 'other')
                if s_p.uncertainty_of_measurement is not None:
                    e_p['uncertaintyOfMeasurement'] = s_p.uncertainty_of_measurement
                if s_p.probed_thickness is not None:
                    e_p['probedThickness'] = s_p.probed_thickness * 100  # cm
                if s_p.profile_nr is not None:
                    e_p['profile_nr'] = s_p.profile_nr

                if isinstance(s_p, SSAProfile):
                    e_p['layers'] = []
                    for _, layer in s_p.data.iterrows():
                        l = {
                            'depthTop': (profile_depth - layer.top_height) * 100,
                            'density': layer.density}
                        if not np.isnan(layer.thickness):
                            l['thickness'] = layer.thickness * 100
                        e_p['layers'].append(l)
                elif isinstance(s_p, SSAPointProfile):
                    e_p['measurements'] = [
                        {'depth': (profile_depth - layer.height) * 100,
                         'value': layer.ssa} for layer in s_p.data.iterrows()]

                if s_p.comment is not None:
                    e_p['metaData'] = {'comment': s_p.comment}
                _append_additional_data(e_p, s_p.additional_data)
                e_spm['specificurfaceAreaProfiles'].append(e_p)

    # - hardnessProfiles
    from snowprofile.profiles import HardnessProfile, HardnessPointProfile
    if len(snowprofile.ssa_profiles) > 0:
        e_spm['hardnessProfiles'] = []
        for s_p in snowprofile.hardness_profiles:
            profile_depth = _get_snowdepth(s_p)
            if len(s_p.data) > 0:
                e_p = {}
                e_p['methodOfMeasurement'] = _get_value(s_p.method_of_measurement, _ssa_mom[version], 'other')
                if s_p.uncertainty_of_measurement is not None:
                    e_p['uncertaintyOfMeasurement'] = s_p.uncertainty_of_measurement
                if s_p.probed_thickness is not None:
                    e_p['probedThickness'] = s_p.probed_thickness * 100  # cm
                if s_p.profile_nr is not None:
                    e_p['profile_nr'] = s_p.profile_nr

                if isinstance(s_p, HardnessProfile):
                    e_p['layers'] = []
                    for _, layer in s_p.data.iterrows():
                        l = {
                            'depthTop': (profile_depth - layer.top_height) * 100,
                            'hardness': layer.hardness}
                        if not np.isnan(layer.thickness):
                            l['thickness'] = layer.thickness * 100
                        if 'weight_hammer' in layer and not np.isnan(layer.weight_hammer):
                            l['weightHammer'] = layer.weight_hammer
                        if 'weight_tube' in layer and not np.isnan(layer.weight_tube):
                            l['weightTube'] = layer.weight_tube
                        if 'n_drops' in layer and not np.isnan(layer.n_drops):
                            l['nDrops'] = layer.n_drops
                        if 'drop_height' in layer and not np.isnan(layer.drop_height):
                            l['dropHeight'] = layer.drop_height * 100
                        e_p['layers'].append(l)
                elif isinstance(s_p, HardnessPointProfile):
                    e_p['measurements'] = [
                        {'depth': (profile_depth - layer.height) * 100,
                         'value': layer.hardness} for layer in s_p.data.iterrows()]

                if s_p.comment is not None:
                    e_p['metaData'] = {'comment': s_p.comment}
                _append_additional_data(e_p, s_p.additional_data)
                e_spm['hardnessProfiles'].append(e_p)

    # - strengthProfiles
    if len(snowprofile.strength_profiles) > 0:
        e_spm['strengthProfiles'] = []
        for s_p in snowprofile.strength_profiles:
            profile_depth = _get_snowdepth(s_p)
            if len(s_p.data) > 0:
                e_p = {}
                e_p['strengthType'] = _get_value(s_p.strength_type, _strength_type[version], 'compressive')
                e_p['methodOfMeasurement'] = _get_value(s_p.method_of_measurement, _strength_mom[version], 'other')
                if s_p.uncertainty_of_measurement is not None:
                    e_p['uncertaintyOfMeasurement'] = s_p.uncertainty_of_measurement
                if s_p.probed_area is not None:
                    e_p['probedArea'] = s_p.probed_area * 1e4  # cm2
                if s_p.profile_nr is not None:
                    e_p['profile_nr'] = s_p.profile_nr

                e_p['layers'] = []
                for _, layer in s_p.data.iterrows():
                    l = {
                        'depthTop': (profile_depth - layer.top_height) * 100,
                        'strengthValue': layer.strength}
                    if not np.isnan(layer.thickness):
                        l['thickness'] = layer.thickness * 100
                    if 'fracture_character' in layer and layer.fracture_character is not None:
                        l['fractureCharacter'] = layer.fracture_character
                    e_p['layers'].append(l)

                if s_p.comment is not None:
                    e_p['metaData'] = {'comment': s_p.comment}
                _append_additional_data(e_p, s_p.additional_data)
                e_spm['strengthProfiles'].append(e_p)

    # - impurityProfiles
    if len(snowprofile.impurity_profiles) > 0:
        e_spm['impurityProfiles'] = []
        for s_p in snowprofile.impurity_profiles:
            profile_depth = _get_snowdepth(s_p)
            if len(s_p.data) > 0:
                e_p = {}
                e_p['impurity'] = _get_value(s_p.impurity_type, _impurity_type[version], 'Black carbon')
                e_p['methodOfMeasurement'] = _get_value(s_p.method_of_measurement, _impurity_mom[version], 'other')
                if s_p.uncertainty_of_measurement is not None:
                    e_p['uncertaintyOfMeasurement'] = s_p.uncertainty_of_measurement
                if s_p.probed_thickness is not None:
                    e_p['probedThickness'] = s_p.probed_thickness * 100  # cm
                if s_p.profile_nr is not None:
                    e_p['profile_nr'] = s_p.profile_nr

                e_p['layers'] = []
                for _, layer in s_p.data.iterrows():
                    l = {'depthTop': (profile_depth - layer.top_height) * 100}  # cm
                    if not np.isnan(layer.thickness):
                        l['thickness'] = layer.thickness * 100
                    if 'mass_fraction' in layer and not np.isnan(layer.mass_fraction):
                        l['massFraction'] = layer.mass_fraction
                    if 'volume_fraction' in layer and not np.isnan(layer.volume_fraction):
                        l['volumeFraction'] = layer.volume_fraction
                    e_p['layers'].append(l)

                if s_p.comment is not None:
                    e_p['metaData'] = {'comment': s_p.comment}
                _append_additional_data(e_p, s_p.additional_data)
                e_spm['impurityProfiles'].append(e_p)

    # - stabilityTests
    # TODO: To be done

    if snowprofile.profile_comment is not None:
        e_spm['metaData'] = {'comment': snowprofile.profile_comment}
    _append_additional_data(e_spm, snowprofile.profile_additional_data)

    if snowprofile.comment is not None:
        jo['metaData'] = {'comment': snowprofile.comment}

    _append_additional_data(jo, snowprofile.additional_data)

    # Write the output file
    if isinstance(indent, bool):
        indent = 2 if indent else None
    with open(filename, 'w') as f:
        json.dump(jo, f, indent=indent)


def _append_additional_data(e, additional_data):
    pass


def _get_value(value, table, default):
    if value in table:
        return value
    else:
        return default


def _read_json(j, path: str | list, factor=None, attribution_table=None, default=None):
    """
    Helper to search for an element in a JSON document.
    """
    if not isinstance(path, list):
        path = [path]

    elem = j
    for p in path:
        if elem is None or not isinstance(elem, dict):
            return None
        if p not in elem:
            elem = None
        else:
            elem = elem[p]

    if not (isinstance(elem, list) or isinstance(elem, dict)):
        if attribution_table is not None and elem in attribution_table:
            elem = attribution_table[elem]

        if elem is not None and factor is not None:
            try:
                elem = elem * factor
            except Exception:
                elem = None

    if elem is None:
        return default
    else:
        return elem


def read_caaml6_json(filename):
    """
    Read a CAAML 6 JSON-based IACS Snow Profile document and genberate a SnowProfile object.

    :param filename: The filename to write into. If already exists, will be overwritten.
    :type filename: str
    :returns: SnowProfile object
    """
    from snowprofile import SnowProfile
    from snowprofile.classes import Time, Location, Weather, SurfaceConditions, Observer, Person
    with open(filename, 'r') as f:
        try:
            j = json.load(f)
        except Exception as e:
            logging.critical(f'The provided JSON file {filename} could not be read. '
                             'Generally, this means that the JSOn is inproperly formatted')
            raise e

    contact_persons = []
    e_contact_persons = _read_json(j, ['source', 'provider', 'contactPerson'])
    if e_contact_persons is None or len(e_contact_persons) == 0:
        contact_persons.append(Person())
    else:
        for p in e_contact_persons:
            contact_persons.append(
                Person(
                    name = _read_json(p, 'name'),
                    website = _read_json(p, 'website'),
                    comment = _read_json(p, ['metaData', 'comment'])))
    observer = Observer(
        source_name=_read_json(j, ['source', 'provider', 'name']),
        source_website=_read_json(j, ['source', 'provider', 'website']),
        source_comment=_read_json(j, ['source', 'provider', 'metaData', 'comment']),
        contact_persons=contact_persons)

    profile_depth = _read_json(
        j,
        ['snowProfileMeasurements', 'snowPackCondition', 'heightSnow', 'height'],
        factor=0.01)


    sp = SnowProfile(
        id=_read_json(j, 'id'),
        comment=_read_json(j, ['metaData', 'comment']),
        time=Time(
            record_time=_read_json(j, ['time', 'recordTime']),
            report_time=_read_json(j, ['time', 'reportTime']),
            last_edition_time=_read_json(j, ['time', 'lastEditTime']),
            comment=_read_json(j, ['time', 'metaData', 'comment']),
            additional_data = _parse_adddata(j, ['time', 'customData'])),
        observer=observer,
        location=Location(
            id=_read_json(j, ['location', 'id']),
            name=_read_json(j, ['location', 'name']),
            aspect=_read_json(j, ['location', 'aspect'], attribution_table=_constants.aspects),
            slope=_read_json(j, ['location', 'slopeAngle']),
            elevation=_read_json(j, ['location', 'elevation']),
            latitude=_read_json(j, ['location', 'coordinates', 'lat']),
            longitude=_read_json(j, ['location', 'coordinates', 'long']),
            country=_read_json(j, ['location', 'country']),
            region=_read_json(j, ['location', 'region']),
            comment=_read_json(j, ['location', 'metaData', 'comment']),
            additional_data = _parse_adddata(j, ['location', 'customData'])),
        application=_read_json(j, ['application', 'name']),
        application_version=_read_json(j, ['application', 'version']),
        profile_depth=profile_depth,
        profile_swe=_read_json(
            j,
            ['snowProfileMeasurements', 'snowPackCondition', 'heightSnow', 'waterEquivalent']),
        new_snow_24_depth=_read_json(
            j,
            ['snowProfileMeasurements', 'snowPackCondition', 'height24h', 'height']),
        new_snow_24_swe=_read_json(
            j,
            ['snowProfileMeasurements', 'snowPackCondition', 'height24h', 'waterEquivalent']),
        new_snow_24_depth_std=_read_json(
            j,
            ['snowProfileMeasurements', 'snowPackCondition', 'heightIrregular', 'height']),
        new_snow_24_swe_std=_read_json(
            j,
            ['snowProfileMeasurements', 'snowPackCondition', 'heightIrregular', 'waterEquivalent']),
        weather=Weather(
            cloudiness=_read_json(j, ['snowProfileMeasurements', 'weatherCondition', 'skyCondition']),
            precipitation=_read_json(
                j,
                ['snowProfileMeasurements', 'weatherCondition', 'precipitationType'],
                attribution_table={'None': 'Nil', 'Snow': 'SN', 'Hail': 'GR',
                                   'Rain': 'RA', 'Sleet': 'RASN', 'Graupel': 'GS'}),
            air_temperature=_read_json(j, ['snowProfileMeasurements', 'weatherCondition', 'airTemperature']),
            wind_speed=_read_json(
                j,
                ['snowProfileMeasurements', 'weatherCondition', 'windSpeed'],
                attribution_table=_constants.wind_speed),
            wind_direction=_read_json(
                j,
                ['snowProfileMeasurements', 'weatherCondition', 'windDirection'],
                attribution_table=_constants.aspects),
            comment=_read_json(j, ['snowProfileMeasurements', 'weatherCondition', 'metaData', 'comment']),
            additional_data = _parse_adddata(j, ['snowProfileMeasurements', 'weatherCondition', 'customData'])),
        surface_conditions=SurfaceConditions(
            surface_roughness=_read_json(
                j,
                ['snowProfileMeasurements', 'surfaceCondition', 'surfaceFeature', 'surfaceRoughness']),
            surface_features_amplitude=_read_json(
                j,
                ['snowProfileMeasurements', 'surfaceCondition', 'surfaceFeature', 'amplitude', 'position'],
                factor=0.01),
            surface_features_amplitude_min=_read_json(
                j,
                ['snowProfileMeasurements', 'surfaceCondition', 'surfaceFeature', 'amplitude', 'beginposition'],
                factor=0.01),
            surface_features_amplitude_max=_read_json(
                j,
                ['snowProfileMeasurements', 'surfaceCondition', 'surfaceFeature', 'amplitude', 'endposition'],
                factor=0.01),
            surface_features_wavelength=_read_json(
                j,
                ['snowProfileMeasurements', 'surfaceCondition', 'surfaceFeature', 'wavelength', 'position']),
            surface_features_wavelength_min=_read_json(
                j,
                ['snowProfileMeasurements', 'surfaceCondition', 'surfaceFeature', 'wavelength', 'beginposition']),
            surface_features_wavelength_max=_read_json(
                j,
                ['snowProfileMeasurements', 'surfaceCondition', 'surfaceFeature', 'wavelength', 'endposition']),
            penetration_ram=_read_json(j, ['snowProfileMeasurements', 'surfaceCondition', 'penetrationRam'],
                                       factor = 0.01),
            penetration_foot=_read_json(j, ['snowProfileMeasurements', 'surfaceCondition', 'penetrationFoot'],
                                        factor = 0.01),
            penetration_ski=_read_json(j, ['snowProfileMeasurements', 'surfaceCondition', 'penetrationSki'],
                                       factor = 0.01),
            comment=_read_json(j, ['snowProfileMeasurements', 'surfaceCondition', 'metaData', 'comment']),
            additional_data=_parse_adddata(j, ['snowProfileMeasurements', 'surfaceCondition', 'customData'])),
        stratigraphy_profile=_parse_stratigraphy_profile(_read_json(
            j,
            ['snowProfileMeasurements', 'stratigraphicProfile']),
            profile_depth=profile_depth),
        temperature_profiles=_parse_temperature_profile(_read_json(
            j,
            ['snowProfileMeasurements', 'temperatureProfile']),
            profile_depth=profile_depth),
        density_profiles=_parse_density_profile(_read_json(j, ['snowProfileMeasurements', 'densityProfiles']),
                                                profile_depth=profile_depth),
        lwc_profiles=_parse_lwc_profile(_read_json(j, ['snowProfileMeasurements', 'liquidWaterContentProfiles']),
                                        profile_depth=profile_depth),
        ssa_profiles=_parse_ssa_profile(_read_json(j, ['snowProfileMeasurements', 'specificSurfaceAreaProfiles']),
                                        profile_depth=profile_depth),
        hardness_profiles=_parse_hardness_profile(_read_json(j, ['snowProfileMeasurements', 'hardnessProfiles']),
                                                  profile_depth=profile_depth),
        strength_profiles=_parse_strength_profile(_read_json(j, ['snowProfileMeasurements', 'strengthProfiles']),
                                                  profile_depth=profile_depth),
        impurity_profiles=_parse_impurity_profile(_read_json(j, ['snowProfileMeasurements', 'impurityProfiles']),
                                                  profile_depth=profile_depth),
        stability_tests=_parse_stb_tests(_read_json(j, ['snowProfileMeasurements', 'stabilityTests']),
                                         profile_depth=profile_depth),
        profile_comment=_read_json(j, ['snowProfileMeasurements', 'metaData', 'comment']),
        profile_additional_data=_parse_adddata(j, ['snowProfileMeasurements', 'customData']),
        additional_data=_parse_adddata(j, ['customData']))

    return sp


def _parse_adddata(j, path):
    # TODO: To be done
    return None


def _parse_generic_profile(j, definitions, min_columns=[]):
    if j is None:
        return None
    if not isinstance(j, list):
        return None

    results = {}
    for key in definitions:
        results[key] = []

    for e in j:
        for key, value in definitions.items():
            factor = value['factor'] if 'factor' in value else None
            attribution_table = value['attribution_table'] if 'attribution_table' in value else None

            r = _read_json(e, value['path'], factor=factor, attribution_table=attribution_table)

            if 'total_depth' in value and r is not None:
                r = value['total_depth'] - r

            results[key].append(r)

    # Get rid of columns full of None
    results = {key: value for key, value in results.items() if key in min_columns or set(value) != set([None])}

    return results


def _parse_stratigraphy_profile(j, profile_depth=0):
    if j is None:
        return None
    _profile_depth = profile_depth if profile_depth is not None else 0
    from snowprofile.profiles import Stratigraphy
    data = _parse_generic_profile(
        _read_json(j, 'layers'),
        {'top_height': {'path': 'depthTop', 'factor': 0.01, 'total_depth': _profile_depth},
         'thickness': {'path': 'thickness', 'factor': 0.01},  # cm -> m
         'grain_1': {'path': 'grainFormPrimary'},
         'grain_2': {'path': 'grainFormSecondary'},
         'grain_size': {'path': ['grainSize', 'avg'], 'factor': 0.001,  # mm -> m
                        'attribution_table': _constants.grain_sizes},
         'grain_size_max': {'path': ['grainSize', 'max'], 'factor': 0.001,
                            'attribution_table': _constants.grain_sizes},
         'hardness': {'path': 'hardness'},
         'wetness': {'path': 'wetness'},
         'loc': {'path': 'uniqueLayerOfConcern'},
         'comment': {'path': ['metaData', 'comment']},
         'formation_time': {'path': ['validFormationTime']}},
        min_columns=['grain_1', 'grain_size', 'hardness', 'grain_2', 'wetness'])
    s = Stratigraphy(
        data=data,
        comment=_read_json(j, ['metaData', 'comment']),
        additional_data=_parse_adddata(j, ['customData']))
    return s


def _parse_temperature_profile(j, profile_depth=0):
    if j is None:
        return []
    _profile_depth = profile_depth if profile_depth is not None else 0
    from snowprofile.profiles import TemperatureProfile
    data = _parse_generic_profile(
        _read_json(j, 'measurements'),
        {'height': {'path': 'depth', 'factor': 0.01, 'total_depth': _profile_depth},
         'temperature': {'path': 'temperature'}},)
    p = TemperatureProfile(
        data=data,
        comment=_read_json(j, ['metaData', 'comment']),
        additional_data=_parse_adddata(j, ['customData']))
    return [p]


def _parse_density_profile(j, profile_depth=0):
    if j is None or not isinstance(j, list):
        return []
    lr = []
    for e in j:
        _profile_depth = profile_depth if profile_depth is not None else 0
        from snowprofile.profiles import DensityProfile
        data = _parse_generic_profile(
            _read_json(e, 'layers'),
            {'top_height': {'path': 'depthTop', 'factor': 0.01, 'total_depth': _profile_depth},
             'thickness': {'path': 'thickness', 'factor': 0.01},
             'density': {'path': 'density'}})
        p = DensityProfile(
            data=data,
            profile_nr=_read_json(e, ['profileNumber']),
            method_of_measurement=_read_json(e, ['methodOfMeasurement']),
            uncertainty_of_measurement=_read_json(e, ['uncertaintyOfMeasurement']),
            probed_volume=_read_json(e, ['probeVolume'], factor=1e-6),
            probed_diameter=_read_json(e, ['probeDiameter'], factor=0.01),
            probed_length=_read_json(e, ['probeLength'], factor=0.01),
            probed_thickness=_read_json(e, ['probedThickness'], factor=0.01),
            comment=_read_json(e, ['metaData', 'comment']),
            additional_data=_parse_adddata(e, ['customData']))
        lr.append(p)
    return lr


def _parse_lwc_profile(j, profile_depth=0):
    if j is None or not isinstance(j, list):
        return []
    lr = []
    for e in j:
        _profile_depth = profile_depth if profile_depth is not None else 0
        from snowprofile.profiles import DensityProfile
        data = _parse_generic_profile(
            _read_json(e, 'layers'),
            {'top_height': {'path': 'depthTop', 'factor': 0.01, 'total_depth': _profile_depth},
             'thickness': {'path': 'thickness', 'factor': 0.01},
             'lwc': {'path': 'liquidWaterContent'}},)
        p = DensityProfile(
            data=data,
            profile_nr=_read_json(e, ['profileNumber']),
            method_of_measurement=_read_json(e, ['methodOfMeasurement']),
            uncertainty_of_measurement=_read_json(e, ['uncertaintyOfMeasurement']),
            probed_thickness=_read_json(e, ['probeThickness'], factor=0.01),
            comment=_read_json(e, ['metaData', 'comment']),
            additional_data=_parse_adddata(e, ['customData']))
        lr.append(p)
    return lr


def _parse_strength_profile(j, profile_depth=0):
    if j is None or not isinstance(j, list):
        return []
    lr = []
    for e in j:
        _profile_depth = profile_depth if profile_depth is not None else 0
        from snowprofile.profiles import StrengthProfile
        data = _parse_generic_profile(
            _read_json(e, 'layers'),
            {'top_height': {'path': 'depthTop', 'factor': 0.01, 'total_depth': _profile_depth},
             'thickness': {'path': 'thickness', 'factor': 0.01},
             'strength': {'path': 'strengthValue'}},)
        p = StrengthProfile(
            data=data,
            profile_nr=_read_json(e, ['profileNumber']),
            strength_type=_read_json(e, ['strengthType']),
            method_of_measurement=_read_json(e, ['methodOfMeasurement']),
            uncertainty_of_measurement=_read_json(e, ['uncertaintyOfMeasurement']),
            probed_area=_read_json(e, ['probedArea'], factor=1e-4),
            comment=_read_json(e, ['metaData', 'comment']),
            additional_data=_parse_adddata(e, ['customData']))
        lr.append(p)
    return lr


def _parse_impurity_profile(j, profile_depth=0):
    if j is None or not isinstance(j, list):
        return []
    lr = []
    for e in j:
        _profile_depth = profile_depth if profile_depth is not None else 0
        from snowprofile.profiles import ImpurityProfile
        data = _parse_generic_profile(
            _read_json(e, 'layers'),
            {'top_height': {'path': 'depthTop', 'factor': 0.01, 'total_depth': _profile_depth},
             'thickness': {'path': 'thickness', 'factor': 0.01},
             'mass_fraction': {'path': 'massFraction'},
             'volume_fraction': {'path': 'volumeFraction'}},)
        p = ImpurityProfile(
            data=data,
            profile_nr=_read_json(e, ['profileNumber']),
            impurity_type=_read_json(e, ['impurity']),
            method_of_measurement=_read_json(e, ['methodOfMeasurement']),
            uncertainty_of_measurement=_read_json(e, ['uncertaintyOfMeasurement']),
            probed_thickness=_read_json(e, ['probedThickness'], factor=0.01),
            comment=_read_json(e, ['metaData', 'comment']),
            additional_data=_parse_adddata(e, ['customData']))
        lr.append(p)
    return lr


def _parse_ssa_profile(j, profile_depth=0):
    if j is None or not isinstance(j, list):
        return []
    lr = []
    for e in j:
        _profile_depth = profile_depth if profile_depth is not None else 0
        if 'measurements' in e:
            data = _parse_generic_profile(
                _read_json(e, 'measurements'),
                {'height': {'path': 'depth', 'factor': 0.01, 'total_depth': _profile_depth},
                 'ssa': {'path': 'value'}},)
            from snowprofile.profiles import SSAPointProfile
            class_ = SSAPointProfile
        else:
            data = _parse_generic_profile(
                _read_json(e, 'layers'),
                {'top_height': {'path': 'depthTop', 'factor': 0.01, 'total_depth': _profile_depth},
                 'thickness': {'path': 'thickness', 'factor': 0.01},
                 'strength': {'path': 'value'}},)
            from snowprofile.profiles import SSAProfile
            class_ = SSAProfile
        p = class_(
            data=data,
            profile_nr=_read_json(e, ['profileNumber']),
            method_of_measurement=_read_json(e, ['methodOfMeasurement']),
            uncertainty_of_measurement=_read_json(e, ['uncertaintyOfMeasurement']),
            probed_thickness=_read_json(e, ['probedThickness'], factor=0.01),
            comment=_read_json(e, ['metaData', 'comment']),
            additional_data=_parse_adddata(e, ['customData']))
        lr.append(p)
    return lr


def _parse_hardness_profile(j, profile_depth=0):
    if j is None or not isinstance(j, list):
        return []
    lr = []
    for e in j:
        _profile_depth = profile_depth if profile_depth is not None else 0
        if 'measurements' in e:
            data = _parse_generic_profile(
                _read_json(e, 'measurements'),
                {'height': {'path': 'depth', 'factor': 0.01, 'total_depth': _profile_depth},
                 'hardness': {'path': 'value'}},)
            from snowprofile.profiles import HardnessPointProfile
            class_ = HardnessPointProfile
        else:
            data = _parse_generic_profile(
                _read_json(e, 'layers'),
                {'top_height': {'path': 'depthTop', 'factor': 0.01, 'total_depth': _profile_depth},
                 'thickness': {'path': 'thickness', 'factor': 0.01},
                 'hardness': {'path': 'hardness'},
                 'weight_hammer': {'path': 'weightHammer'},
                 'weight_tube': {'path': 'weightTube'},
                 'n_drops': {'path': 'nDrops'},
                 'drop_height': {'path': 'dropHeight', 'factor': 0.01}},)
            from snowprofile.profiles import HardnessProfile
            class_ = HardnessProfile
        p = class_(
            data=data,
            profile_nr=_read_json(e, ['profileNumber']),
            method_of_measurement=_read_json(e, ['methodOfMeasurement']),
            uncertainty_of_measurement=_read_json(e, ['uncertaintyOfMeasurement']),
            probed_thickness=_read_json(e, ['probedThickness'], factor=0.01),
            comment=_read_json(e, ['metaData', 'comment']),
            additional_data=_parse_adddata(e, ['customData']))
        lr.append(p)
    return lr


def _parse_stb_tests(j, profile_depth=0):
    return []
