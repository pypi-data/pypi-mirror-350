# -*- coding: utf-8 -*-

import logging
import datetime
import xml.etree.ElementTree as ET
import sys

import numpy as np

# Note to developpers:
# XML elements are prefixed by e_
# Snowprofile data is prefixes by s_

table_versions_uri = {
    '6.0.6': 'http://caaml.org/Schemas/SnowProfileIACS/v6.0.6',
    '6.0.5': 'http://caaml.org/Schemas/SnowProfileIACS/v6.0.4'}

uri_gml = 'http://www.opengis.net/gml'


def write_caaml6_xml(snowprofile, filename, version='6.0.5', indent=False):
    """
    Write a SnowProfile object into a CAAML 6 XML-based IACS Snow Profile document.

    Currently supported versions:

    - 6.0.6
    - 6.0.5 (default)

    :param snowprofile: A SnowProfile object to dump to a CAAML file
    :type snowprofile: SnowProfile
    :param filename: The filename to write into. If already exists, will be overwritten.
    :type filename: str
    :param indent: Visually indent the output (default: False, provide the more compact outut available)
    :type indent: bool or string (spaces for indentation)
    """
    if version not in table_versions_uri:
        raise ValueError(f'Unsupported CAAML version {version}.')
    uri = table_versions_uri[version]
    ns = '{' + uri + '}'
    ns_gml = '{' + uri_gml + '}'

    # Namespaces
    ET.register_namespace('caaml', uri)
    ET.register_namespace('gml', uri_gml)

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

    config = {'_gen_id': _gen_id,
              'ns': ns,
              'ns_gml': ns_gml,
              'profile_depth': snowprofile.profile_depth if snowprofile.profile_depth is not None else 0,
              'profile_swe': snowprofile.profile_swe,
              'version': version}

    if snowprofile.profile_depth is None:
        logging.warning('Profile depth not set. Ensure this is expected !')


    # Main XML element
    root = ET.Element(f'{ns}SnowProfile', attrib={f'{ns_gml}id': _gen_id(snowprofile.id, 'snowprofile')})

    # - Metadata (optional)
    if snowprofile.comment is not None:
        _ = ET.SubElement(root, f'{ns}metaData')
        _ = ET.SubElement(_, f'{ns}comment')
        _.text = snowprofile.comment

    # - timeRef
    time = ET.SubElement(root, f'{ns}timeRef')

    if snowprofile.time.comment is not None:
        _ = ET.SubElement(time, f'{ns}metaData')
        _ = ET.SubElement(_, f'{ns}comment')
        _.text = snowprofile.time.comment

    record_time = ET.SubElement(time, f'{ns}recordTime')

    if snowprofile.time.record_period[0] is not None and snowprofile.time.record_period[1] is not None:
        _ = ET.SubElement(record_time, f'{ns}TimePeriod')
        begin = ET.SubElement(_, f'{ns}beginPosition')
        begin.text = snowprofile.time.record_period[0].isoformat()
        end = ET.SubElement(_, f'{ns}endPosition')
        end.text = snowprofile.time.record_period[1].isoformat()
    elif snowprofile.time.record_time is not None:
        _ = ET.SubElement(record_time, f'{ns}TimeInstant')
        begin = ET.SubElement(_, f'{ns}timePosition')
        begin.text = snowprofile.time.record_time.isoformat()
    else:
        logging.error('Could not find a valid record time or time period. Use current time')
        _ = ET.SubElement(record_time, f'{ns}TimeInstant')
        begin = ET.SubElement(_, f'{ns}timePosition')
        begin.text = datetime.datetime.now().isoformat()

    if snowprofile.time.report_time is not None:
        _ = ET.SubElement(time, f'{ns}dateTimeReport')
        _.text = snowprofile.time.report_time.isoformat()

    if snowprofile.time.last_edition_time is not None:
        _ = ET.SubElement(time, f'{ns}dateTimeLastEdit')
        _.text = snowprofile.time.last_edition_time.isoformat()

    _append_additional_data(time, snowprofile.time.additional_data, ns=ns)

    # - srcRef
    src = ET.SubElement(root, f'{ns}srcRef')
    if snowprofile.observer.source_name is None:
        src = ET.SubElement(src, f'{ns}Person',
                            attrib={f'{ns_gml}id': _gen_id(snowprofile.observer.contact_persons[0].id, 'person')})
        if len(snowprofile.observer.contact_persons) > 1:
            logging.error('Observer: if you provide more than one contact person you need to provide a source name. '
                          'Only the first contact person will be used.')
        if snowprofile.observer.contact_persons[0].comment is not None:
            _ = ET.SubElement(src, f'{ns}metaData')
            _ = ET.SubElement(_, f'{ns}comment')
            _.text = snowprofile.observer.contact_persons[0].comment
        _ = ET.SubElement(src, f'{ns}name')
        if snowprofile.observer.contact_persons[0].name is not None:
            _.text = snowprofile.observer.contact_persons[0].name
        _append_additional_data(src, snowprofile.observer.contact_persons[0].additional_data, ns=ns)
    else:
        op = ET.SubElement(src, f'{ns}Operation', attrib={f'{ns_gml}id': _gen_id(snowprofile.observer.source_id,
                                                                                 'operation')})
        if snowprofile.observer.source_comment is not None:
            _ = ET.SubElement(op, f'{ns}metaData')
            _ = ET.SubElement(_, f'{ns}comment')
            _.text = snowprofile.observer.source_comment
        _ = ET.SubElement(op, f'{ns}name')
        _.text = snowprofile.observer.source_name
        for person in snowprofile.observer.contact_persons:
            p = ET.SubElement(op, f'{ns}contactPerson', attrib={f'{ns_gml}id': _gen_id(person.id, 'person')})
            if person.comment is not None:
                _ = ET.SubElement(p, f'{ns}metaData')
                _ = ET.SubElement(_, f'{ns}comment')
                _.text = person.comment
            name = ET.SubElement(p, f'{ns}name')  # Compulosry element (but no content is fine)
            if person.name is not None:
                name.text = person.name
            _append_additional_data(p, person.additional_data, ns=ns)
        _append_additional_data(op, snowprofile.observer.source_additional_data, ns=ns)

    # locRef
    src = ET.SubElement(root, f'{ns}locRef', attrib={f'{ns_gml}id': _gen_id(snowprofile.location.id, 'location')})
    loc = snowprofile.location
    if loc.comment is not None:
        _ = ET.SubElement(src, f'{ns}metaData')
        _ = ET.SubElement(_, f'{ns}comment')
        _.text = loc.comment
    name = ET.SubElement(src, f'{ns}name')
    name.text = loc.name
    _ = ET.SubElement(src, f'{ns}obsPointSubType')
    if loc.point_type is not None:
        _.text = loc.point_type
    if loc.elevation is not None:
        _ = ET.SubElement(src, f'{ns}validElevation')
        _ = ET.SubElement(_, f'{ns}ElevationPosition', attrib={'uom': 'm'})
        _ = ET.SubElement(_, f'{ns}position')
        _.text = str(int(loc.elevation))
    if loc.aspect is not None:
        _ = ET.SubElement(src, f'{ns}validAspect')
        _ = ET.SubElement(_, f'{ns}AspectPosition')
        _ = ET.SubElement(_, f'{ns}position')
        _.text = str(int(loc.aspect))
    if loc.slope is not None:
        _ = ET.SubElement(src, f'{ns}validSlopeAngle')
        _ = ET.SubElement(_, f'{ns}SlopeAnglePosition', attrib={'uom': 'deg'})
        _ = ET.SubElement(_, f'{ns}position')
        _.text = str(int(loc.slope))
    if loc.latitude is not None and loc.longitude is not None:
        _ = ET.SubElement(src, f'{ns}pointLocation')
        _ = ET.SubElement(_, f'{ns_gml}Point', attrib={f'{ns_gml}id': _gen_id('pointID'),
                                                       'srsName': "urn:ogc:def:crs:OGC:1.3:CRS84",
                                                       'srsDimension': "2"})
        _ = ET.SubElement(_, f'{ns_gml}pos')
        _.text = f'{loc.latitude} {loc.longitude}'
    if loc.country is not None:
        _ = ET.SubElement(src, f'{ns}country')
        _.text = loc.country
    if loc.region is not None:
        _ = ET.SubElement(src, f'{ns}region')
        _.text = loc.region

    if version >= "6.0.6":
        env = snowprofile.environment
        # Solar Mask
        sm = snowprofile.environment.solar_mask
        if sm is not None:
            e_sm = ET.SubElement(src, f'{ns}solarMask')
            e_smm = ET.SubElement(e_sm, f'{ns}solarMaskMetaData')
            if env.solar_mask_comment is not None:
                _ = ET.SubElement(e_smm, f'{ns}comment')
                _.text = env.solar_mask_comment
            _ = ET.SubElement(e_smm, f'{ns}methodOfMeas')
            if env.solar_mask_method_of_measurement is None:
                _.text = 'other'
            else:
                _.text = env.solar_mask_method_of_measurement
            if env.solar_mask_uncertainty:
                _ = ET.SubElement(e_smm, f'{ns}uncertaintyOfMeas')
                _.text = "{:.12g}".format(env.solar_mask_uncertainty)
            if env.solar_mask_quality:
                _ = ET.SubElement(e_smm, f'{ns}qualityOfMeas')
                _.text = env.solar_mask_quality

            for _, dataline in sm.data.iterrows():
                e_ = ET.SubElement(e_sm, f'{ns}Data', attrib={'uom': 'deg'})
                _ = ET.SubElement(e_, f'{ns}azimuth')
                _.text = str(int(dataline.azimuth))
                _ = ET.SubElement(e_, f'{ns}elevation')
                _.text = "{:.12g}".format(dataline.elevation)

            _append_additional_data(e_sm, snowprofile.environment.solar_mask_additional_data)

        # obsPointEnvironment
        e_ope = ET.SubElement(src, f'{ns}obsPointEnvironment')
        if env.bed_surface is not None:
            _ = ET.SubElement(e_ope, f'{ns}bedSurface')
            _.text = env.bed_surface
        if env.bed_surface_comment is not None:
            _ = ET.SubElement(e_ope, f'{ns}bedSurfaceComment')
            _.text = env.bed_surface_comment
        if env.litter_thickness is not None:
            _ = ET.SubElement(e_ope, f'{ns}litterThickness', attrib={'uom': 'm'})
            _.text = "{:.12g}".format(env.litter_thickness)
        if env.ice_thickness is not None:
            _ = ET.SubElement(e_ope, f'{ns}iceThickness', attrib={'uom': 'm'})
            _.text = "{:.12g}".format(env.ice_thickness)
        if env.low_vegetation_height is not None:
            _ = ET.SubElement(e_ope, f'{ns}lowVegetationHeight', attrib={'uom': 'm'})
            _.text = "{:.12g}".format(env.low_vegetation_height)
        if env.LAI is not None:
            _ = ET.SubElement(e_ope, f'{ns}lai', attrib={'uom': '1'})
            _.text = "{:.12g}".format(env.LAI)
        if env.forest_presence is not None:
            _ = ET.SubElement(e_ope, f'{ns}forestPresence')
            _.text = env.forest_presence
        if env.forest_presence_comment is not None:
            _ = ET.SubElement(e_ope, f'{ns}forestComment')
            _.text = env.forest_presence_comment
        if env.sky_view_factor is not None:
            _ = ET.SubElement(e_ope, f'{ns}skyViewFactor', attrib={'uom': '1'})
            _.text = "{:.12g}".format(env.sky_view_factor)
        if env.tree_height is not None:
            _ = ET.SubElement(e_ope, f'{ns}treeHeight', attrib={'uom': 'm'})
            _.text = "{:.12g}".format(env.tree_height)

    _append_additional_data(src, loc.additional_data, ns=ns)

    # snowProfileResultsOf
    e_r = ET.SubElement(root, f'{ns}snowProfileResultsOf')
    e_r = ET.SubElement(e_r, f'{ns}SnowProfileMeasurements', attrib={'dir': 'top down'})

    if snowprofile.profile_comment is not None:
        _ = ET.SubElement(e_r, f'{ns}metaData')
        _ = ET.SubElement(_, f'{ns}comment')
        _.text = snowprofile.profile_comment

    # profileDepth seem to be designed to be the observed depth rather than the total depth
    # if snowprofile.profile_depth is not None:
    #     _ = ET.SubElement(r, f'{ns}profileDepth', attrib={'uom': 'cm'})
    #     _.text = str(float(snowprofile.profile_depth) * 100)

    # - Weather
    e_weather = ET.SubElement(e_r, f'{ns}weatherCond')
    s_weather = snowprofile.weather

    e_weather_metadata = ET.SubElement(e_weather, f'{ns}metaData')
    e_weather_comment = ET.SubElement(e_weather_metadata, f'{ns}comment')
    comment = ''
    if s_weather.air_temperature_measurement_height is not None and version >= "6.0.6":
        _ = ET.SubElement(e_weather_metadata, f'{ns}airTempMeasurementHeight', attrib={'uom': 'm'})
        _.text = "{:.10g}".format(s_weather.air_temperature_measurement_height)
    elif s_weather.air_temperature_measurement_height is not None:
        comment += f'Height of the temperature measurement: {s_weather.air_temperature_measurement_height}m\n'
    if s_weather.wind_measurement_height is not None and version >= "6.0.6":
        _ = ET.SubElement(e_weather_metadata, f'{ns}windMeasurementHeight', attrib={'uom': 'm'})
        _.text = "{:.10g}".format(s_weather.wind_measurement_height)
    elif s_weather.wind_measurement_height is not None:
        comment += f'Height of the wind measurement: {s_weather.wind_measurement_height}m\n'
    if s_weather.comment is not None or len(comment) > 1:
        if s_weather.comment is not None and len(comment) == 0:
            comment = s_weather.comment
        else:
            comment = s_weather.comment + "\n\n" + comment
        e_weather_comment.text = comment

    if s_weather.cloudiness is not None:
        _ = ET.SubElement(e_weather, f'{ns}skyCond')
        _.text = s_weather.cloudiness
    if s_weather.precipitation is not None:
        _ = ET.SubElement(e_weather, f'{ns}precipTI')
        _.text = s_weather.precipitation
    if s_weather.air_temperature is not None:
        _ = ET.SubElement(e_weather, f'{ns}airTempPres', attrib={'uom': 'degC'})
        _.text = "{:.10g}".format(s_weather.air_temperature)
    if s_weather.air_humidity is not None and version >= "6.0.6":
        _ = ET.SubElement(e_weather, f'{ns}airHumPres')
        _.text = "{:.10g}".format(s_weather.air_humidity)
    if s_weather.wind_speed is not None:
        _ = ET.SubElement(e_weather, f'{ns}windSpd', attrib={'uom': 'ms-1'})
        _.text = "{:.10g}".format(s_weather.wind_speed)
    if s_weather.wind_direction is not None:
        _ = ET.SubElement(e_weather, f'{ns}windDir')
        _ = ET.SubElement(_, f'{ns}AspectPosition')
        _ = ET.SubElement(_, f'{ns}position')
        _.text = str(int(s_weather.wind_direction))
    _append_additional_data(e_weather, s_weather.additional_data, ns=ns)

    # - Snowpack
    e_snowpack = ET.SubElement(e_r, f'{ns}snowPackCond')
    if snowprofile.profile_depth is not None or snowprofile.profile_swe is not None:
        hs = ET.SubElement(e_snowpack, f'{ns}hS')
        hsc = ET.SubElement(hs, f'{ns}Components')
        if snowprofile.profile_depth is not None:
            _ = ET.SubElement(hsc, f'{ns}height', attrib={'uom': 'cm'})
            _.text = "{:.12g}".format(snowprofile.profile_depth * 100)
        if snowprofile.profile_swe is not None:
            _ = ET.SubElement(hsc, f'{ns}waterEquivalent', attrib={'uom': 'kgm-2'})
            _.text = "{:.12g}".format(snowprofile.profile_swe)
    if (snowprofile.profile_depth_std is not None or snowprofile.profile_swe_std is not None):
        if version >= "6.0.6":
            hs = ET.SubElement(e_snowpack, f'{ns}hSVariability')
            hsc = ET.SubElement(hs, f'{ns}Components')
            if snowprofile.profile_depth_std is not None:
                _ = ET.SubElement(hsc, f'{ns}height', attrib={'uom': 'cm'})
                _.text = "{:.12g}".format(snowprofile.profile_depth_std * 100)
            if snowprofile.profile_swe_std is not None:
                _ = ET.SubElement(hsc, f'{ns}waterEquivalent', attrib={'uom': 'kgm-2'})
                _.text = "{:.12g}".format(snowprofile.profile_swe_std)
        else:
            logging.warning('Caaml 6 < 6.0.6 does not support profile_depth_std and profile_swe_std.')
    if snowprofile.new_snow_24_depth is not None or snowprofile.new_snow_24_swe is not None:
        hs = ET.SubElement(e_snowpack, f'{ns}hN24')
        hsc = ET.SubElement(hs, f'{ns}Components')
        if snowprofile.new_snow_24_depth is not None:
            _ = ET.SubElement(hsc, f'{ns}height', attrib={'uom': 'cm'})
            _.text = "{:.12g}".format(snowprofile.new_snow_24_depth * 100)
        if snowprofile.new_snow_24_swe is not None:
            _ = ET.SubElement(hsc, f'{ns}waterEquivalent', attrib={'uom': 'kgm-2'})
            _.text = "{:.12g}".format(snowprofile.new_snow_24_swe)
    if (snowprofile.new_snow_24_depth_std is not None or snowprofile.new_snow_24_swe_std is not None):
        hs = ET.SubElement(e_snowpack, f'{ns}hIN',
                           attrib={'dateTimeCleared': snowprofile.time.record_time.isoformat(timespec='seconds')})
        hsc = ET.SubElement(hs, f'{ns}Components')
        if snowprofile.new_snow_24_depth_std is not None:
            _ = ET.SubElement(hsc, f'{ns}height', attrib={'uom': 'cm'})
            _.text = "{:.12g}".format(snowprofile.new_snow_24_depth_std * 100)
        if snowprofile.new_snow_24_swe_std is not None:
            _ = ET.SubElement(hsc, f'{ns}waterEquivalent', attrib={'uom': 'kgm-2'})
            _.text = "{:.12g}".format(snowprofile.new_snow_24_swe_std)
    if snowprofile.snow_transport is not None:
        if version >= "6.0.6":
            _ = ET.SubElement(e_snowpack, f'{ns}snowTransport')
            _.text = snowprofile.snow_transport
        else:
            logging.warning('Caaml 6 < 6.0.6 does not support snow transport data.')
    if snowprofile.snow_transport_occurence_24 is not None:
        if version >= "6.0.6":
            _ = ET.SubElement(e_snowpack, f'{ns}snowTransportOccurrence24')
            _.text = "{:.12g}".format(snowprofile.snow_transport_occurence_24)
        else:
            logging.warning('Caaml 6 < 6.0.6 does not support snow transport data.')

    #  - Surface characterization
    e_surf = ET.SubElement(e_r, f'{ns}surfCond')
    s_surf = snowprofile.surface_conditions
    comment = ''
    _ = ET.SubElement(e_surf, f'{ns}metaData')
    e_surf_comment = ET.SubElement(_, f'{ns}comment')

    _ = ET.SubElement(e_surf, f'{ns}surfFeatures')
    e_surff = ET.SubElement(_, f'{ns}Components')
    _ = ET.SubElement(e_surff, f'{ns}surfRoughness')
    if s_surf.surface_roughness is not None:
        _.text = s_surf.surface_roughness
    else:
        _.text = 'unknown'
    if s_surf.surface_wind_features is not None:
        if version >= "6.0.6":
            _ = ET.SubElement(e_surff, f'{ns}surfWindFeatures')
            _.text = s_surf.surface_wind_features
        else:
            comment += f'Wind surface features: {s_surf.surface_wind_features}\n'
    if s_surf.surface_melt_rain_features is not None:
        if version >= "6.0.6":
            _ = ET.SubElement(e_surff, f'{ns}surfMeltRainFeatures')
            _.text = s_surf.surface_melt_rain_features
        else:
            comment += f'Melt and rain surface features: {s_surf.surface_melt_rain_features}\n'

    if s_surf.surface_features_amplitude is not None:
        if s_surf.surface_features_amplitude_min is not None or s_surf.surface_features_amplitude_max is not None:
            logging.warning('CAAML6 could not store both surface_feature amplitude and min/max of amplitude.')
        _ = ET.SubElement(e_surff, f'{ns}validAmplitude')
        _ = ET.SubElement(_, f'{ns}AmplitudePosition', attrib={'uom': 'cm'})
        _ = ET.SubElement(_, f'{ns}position')
        _.text = "{:.12g}".format(s_surf.surface_features_amplitude * 100)
    elif s_surf.surface_features_amplitude_min is not None and s_surf.surface_features_amplitude_max is not None:
        _ = ET.SubElement(e_surff, f'{ns}validAmplitude')
        _r = ET.SubElement(_, f'{ns}AmplitudeRange', attrib={'uom': 'cm'})
        _ = ET.SubElement(_r, f'{ns}beginPosition')
        _.text = "{:.12g}".format(s_surf.surface_features_amplitude_min * 100)
        _ = ET.SubElement(_r, f'{ns}endPosition')
        _.text = "{:.12g}".format(s_surf.surface_features_amplitude_max * 100)

    if s_surf.surface_features_wavelength is not None:
        if s_surf.surface_features_wavelength_min is not None or s_surf.surface_features_wavelength_max is not None:
            logging.warning('CAAML6 could not store both surface_feature wavelength and min/max of wavelength.')
        _ = ET.SubElement(e_surff, f'{ns}validWavelength')
        _ = ET.SubElement(_, f'{ns}WavelengthPosition', attrib={'uom': 'm'})
        _ = ET.SubElement(_, f'{ns}position')
        _.text = "{:.12g}".format(s_surf.surface_features_wavelength)
    elif s_surf.surface_features_wavelength_min is not None and s_surf.surface_features_wavelength_max is not None:
        _ = ET.SubElement(e_surff, f'{ns}validWavelength')
        _r = ET.SubElement(_, f'{ns}WavelengthRange', attrib={'uom': 'm'})
        _ = ET.SubElement(_r, f'{ns}beginPosition')
        _.text = "{:.12g}".format(s_surf.surface_features_wavelength_min)
        _ = ET.SubElement(_r, f'{ns}endPosition')
        _.text = "{:.12g}".format(s_surf.surface_features_wavelength_max)

    if s_surf.surface_features_aspect is not None:
        _ = ET.SubElement(e_surff, f'{ns}validAspect')
        _ = ET.SubElement(_, f'{ns}AspectPosition')
        _ = ET.SubElement(_, f'{ns}position')
        _.text = str(int(s_surf.surface_features_aspect))

    if version >= "6.0.6":
        _ = ET.SubElement(e_surff, f'{ns}lapPresence')
        if s_surf.lap_presence is None:
            _.text = 'unknown'
        else:
            _.text = s_surf.lap_presence

        if s_surf.surface_temperature is not None:
            _surftemp = ET.SubElement(e_surff, f'{ns}surfTemp')
            if s_surf.surface_temperature_measurement_method is not None:
                _ = ET.SubElement(_surftemp, f'{ns}methodOfMeas')
                _.text = s_surf.surface_temperature_measurement_method
            _ = ET.SubElement(_surftemp, f'{ns}data', attrib={'uom': 'degC'})
            _.text = str(s_surf.surface_temperature)
    else:
        if s_surf.lap_presence is not None:
            comment += f'LAP presence: {s_surf.lap_presence}\n'
        if s_surf.surface_temperature is not None:
            comment += f'Surface temperature: {s_surf.surface_temperature}\n'
        if s_surf.surface_temperature_measurement_method is not None:
            comment += f'Surface temperature measurement method: {s_surf.surface_temperature_measurement_method}\n'

    if (s_surf.surface_albedo is not None or s_surf.spectral_albedo is not None) and version >= '6.0.6':
        e_albedo = ET.SubElement(e_surff, f'{ns}surfAlbedo')
        if s_surf.surface_albedo is not None:
            e_albedo_broadband = ET.SubElement(e_albedo, f'{ns}albedo')
            _ = ET.SubElement(e_albedo_broadband, f'{ns}albedoMeasurement')
            _.text = "{:.12g}".format(s_surf.surface_albedo)
            if s_surf.surface_albedo_comment is not None:
                _ = ET.SubElement(e_albedo_broadband, f'{ns}metaData')
                _ = ET.SubElement(_, f'{ns}comment')
                _.text = s_surf.surface_albedo_comment
        if s_surf.spectral_albedo is not None:
            e_albedo_spectral = ET.SubElement(e_albedo, f'{ns}spectralAlbedo')
            logging.warning('Spectral albedo not yet implemented for CAAML6 output')
            for _, dataline in s_surf.spectral_albedo.data.iterrows():
                e_sam = ET.SubElement(e_albedo_spectral, f'{ns}spectralAlbedoMeasurement')

                _ = ET.SubElement(e_sam, f'{ns}minWaveLength', attrib={'uom': 'nm'})
                _.text = "{:.12g}".format(dataline.min_wavelength)

                _ = ET.SubElement(e_sam, f'{ns}maxWaveLength', attrib={'uom': 'nm'})
                _.text = "{:.12g}".format(dataline.max_wavelength)

                attrib = {}
                if 'uncertainty' in dataline and not np.isnan(dataline.uncertainty) and version >= '6.0.6':
                    attrib['uncertainty'] = "{:.12g}".format(dataline.uncertainty)
                if 'quality' in dataline and dataline.quality is not None and version >= '6.0.6':
                    attrib['quality'] = dataline.quality
                _ = ET.SubElement(e_sam, f'{ns}albedo', attrib=attrib)
                _.text = "{:.12g}".format(dataline.albedo)

            if s_surf.spectral_albedo.comment is not None:
                _ = ET.SubElement(e_albedo_spectral, f'{ns}metaData')
                _ = ET.SubElement(_, f'{ns}comment')
                _.text = s_surf.spectral_albedo.comment


    if s_surf.comment is not None or len(comment) > 0:
        if s_surf.comment is not None and len(comment) == 0:
            comment = s_surf.comment
        elif s_surf.comment is not None:
            comment = s_surf.comment + "\n\n" + comment
        e_surf_comment.text = comment

    if s_surf.penetration_ram is not None:
        _ = ET.SubElement(e_surf, f'{ns}penetrationRam', attrib={'uom': 'cm'})
        _.text = "{:.12g}".format(s_surf.penetration_ram * 100)
    if s_surf.penetration_foot is not None:
        _ = ET.SubElement(e_surf, f'{ns}penetrationFoot', attrib={'uom': 'cm'})
        _.text = "{:.12g}".format(s_surf.penetration_foot * 100)
    if s_surf.penetration_ski is not None:
        _ = ET.SubElement(e_surf, f'{ns}penetrationSki', attrib={'uom': 'cm'})
        _.text = "{:.12g}".format(s_surf.penetration_ski * 100)

    _append_additional_data(e_surf, s_surf.additional_data)

    # - Profiles
    _insert_stratigrpahy_profile(e_r, snowprofile.stratigraphy_profile, config=config)

    if version >= "6.0.6":
        for profile in snowprofile.temperature_profiles:
            _insert_temperature_profile(e_r, profile, config=config)
    else:
        if len(snowprofile.temperature_profiles) > 1:
            logging.error(f'Only one temperature profile acepted in CAAML v{version}.')
        if len(snowprofile.temperature_profiles) > 0:
            _insert_temperature_profile(e_r, snowprofile.temperature_profiles[0], config=config)

    for profile in snowprofile.density_profiles:
        _insert_density_profile(e_r, profile, config=config)

    for profile in snowprofile.lwc_profiles:
        _insert_lwc_profile(e_r, profile, config=config)

    for profile in snowprofile.ssa_profiles:
        _insert_ssa_profile(e_r, profile, config=config)

    for profile in snowprofile.hardness_profiles:
        _insert_hardness_profile(e_r, profile, config=config)

    for profile in snowprofile.strength_profiles:
        _insert_strength_profile(e_r, profile, config=config)

    for profile in snowprofile.impurity_profiles:
        _insert_impurity_profile(e_r, profile, config=config)

    if len(snowprofile.stability_tests) > 0:
        e_stb = ET.SubElement(e_r, f'{ns}stbTests')
        for stbt in snowprofile.stability_tests:
            _insert_stb_test(e_stb, stbt, config=config)

    for profile in snowprofile.other_scalar_profiles:
        _insert_otherscalar_profile(e_r, profile, config=config)

    for profile in snowprofile.other_vectorial_profiles:
        _insert_othervectorial_profile(e_r, profile, config=config)

    # - Additional data
    _append_additional_data(e_r, snowprofile.profile_additional_data)

    # application  and application_version (optional)
    if snowprofile.application is not None:
        _ = ET.SubElement(root, f'{ns}application')
        _.text = snowprofile.application
    if snowprofile.application_version is not None:
        _ = ET.SubElement(root, f'{ns}applicationVersion')
        _.text = snowprofile.application_version

    _append_additional_data(root, snowprofile.additional_data, ns=ns)

    #
    # Generate Tree from mail element and write
    #
    tree = ET.ElementTree(root)
    if indent:
        if sys.version_info.major == 3 and sys.version_info.minor >= 9:
            if isinstance(indent, bool) and indent is True:
                indent = '  '
            ET.indent(tree, space=indent)
        else:
            logging.error('CAAML6_XML write: Indentation is not available with python < 8.9. Will use indent=False.')
    tree.write(filename, encoding='utf-8',
               xml_declaration=True)


def _append_additional_data(element, data, ns=''):
    if data is None or data.data is None:
        return None
    # TODO: tbd  <24-02-25, Léo Viallon-Galinier> #


def _gen_common_attrib(s, config={}):
    attrib = {}
    if s.id is not None and config['version'] >= '6.0.6':
        attrib['id'] = config['_gen_id'](s.id)
    if len(s.related_profiles) > 0 and config['version'] >= '6.0.6':
        attrib['relatedProfiles'] = ' '.join(s.related_profiles)
    if s.name is not None and config['version'] >= '6.0.6':
        attrib['name'] = s.name
    return attrib


def _gen_common_metadata(e, s, config={}, additional_metadata = [], name='metaData'):
    """
    Metadata handler common to all profiles.
    """
    ns = config['ns']
    comment = ''

    e_md = ET.SubElement(e, f'{ns}{name}')
    e_comment = ET.SubElement(e_md, f'{ns}comment')

    if config['version'] >= "6.0.6":
        if s.record_period is not None and s.record_period[0] is not None and s.record_period[1] is not None:
            e_record_time = ET.SubElement(e_md, f'{ns}recordTime')
            _ = ET.SubElement(e_record_time, f'{ns}TimePeriod')
            begin = ET.SubElement(_, f'{ns}beginPosition')
            begin.text = s.record_period[0].isoformat()
            end = ET.SubElement(_, f'{ns}endPosition')
            end.text = s.record_period[1].isoformat()
        elif s.record_time is not None:
            e_record_time = ET.SubElement(e_md, f'{ns}recordTime')
            _ = ET.SubElement(e_record_time, f'{ns}TimeInstant')
            _ = ET.SubElement(_, f'{ns}timePosition')
            _.text = s.record_time.isoformat()
    else:
        if s.record_time is not None:
            comment += f"Record time: {s.record_time.isoformat()}\n"
        if s.record_period is not None and s.record_period[0] is not None and s.record_period[1] is not None:
            comment += f"Record period: {s.record_period[0].isoformat()}-{s.record_period[1].isoformat()}\n"

    e_hs = None
    if s.profile_depth is not None and s.profile_depth != config['profile_depth']:
        if config['version'] >= "6.0.6":
            e_hs = ET.SubElement(e_md, f"{ns}hS")
            e_hs = ET.SubElement(e_hs, f"{ns}Components")
            _ = ET.SubElement(e_hs, f"{ns}height", attrib={'uom': 'cm'})
            _.text = str(s.profile_depth * 100)
        else:
            comment += f"Profile depth: {s.profile_depth}m\n"
    if s.profile_swe is not None and s.profile_swe != config['profile_swe']:
        if config['version'] >= "6.0.6":
            if e_hs is None:
                e_hs = ET.SubElement(e_md, f"{ns}hS")
                e_hs = ET.SubElement(e_hs, f"{ns}Components")
            _ = ET.SubElement(e_hs, f"{ns}waterEquivalent", attrib={'uom': 'kgm-2'})
            _.text = str(s.profile_swe)
        else:
            comment += f"Profile SWE: {s.profile_swe}m\n"

    for elem in additional_metadata:
        value = elem['value']
        key = elem['key']

        # None values
        if value is None:
            continue

        # Check version
        if 'min_version' in elem and elem['min_version'] > config['version']:
            if 'comment_title' in elem:
                comment += f'{elem["comment_title"]}: {value}\n'
            continue

        # Get the value and pre-process to get a string
        if 'values' in elem and elem['values'] is not None and value not in elem['values']:
            if 'default_value' in elem:
                value = elem['default_value']
            else:  # Invalid value and no default value
                logging.error(f'Value {value} not accepted in CAAML format for key {key}. '
                              'May generate an invalid CAAML file.')
                continue
        if 'factor' in elem:
            value = value * elem['factor']
        if isinstance(value, float):
            value = "{:.12g}".format(value)
        elif not isinstance(value, str):
            value = str(value)

        # Write the metadata
        _ = ET.SubElement(e_md, f'{ns}{key}',
                          attrib=elem['attrib'] if 'attrib' in elem and elem['attrib'] is not None else {})
        _.text = value

    if s.comment is not None or len(comment) > 0:
        if s.comment is not None and len(comment) == 0:
            comment = s.comment
        elif s.comment is not None:
            comment = s.comment + "\n\n" + comment
        e_comment.text = comment

    return e_md


def _insert_stratigrpahy_profile(e_r, s_strat, config):
    if s_strat is None:
        return

    ns = config['ns']
    profile_depth = s_strat.profile_depth if s_strat.profile_depth is not None else config['profile_depth']

    e_s = ET.SubElement(e_r, f'{ns}stratProfile',
                        attrib=_gen_common_attrib(s_strat, config=config))
    e_md = _gen_common_metadata(e_s, s_strat, config=config, name='stratMetaData')

    # Layer loop
    for _, layer in s_strat.data.iterrows():
        e_layer = ET.SubElement(e_s, f'{ns}Layer')
        _ = ET.SubElement(e_layer, f'{ns}depthTop', attrib={'uom': 'cm'})
        if profile_depth - layer.top_height < 0:
            raise ValueError(f'Top height ({layer.top_height}m) > profile depth ({profile_depth}m) '
                             'in statigraphy profile)')
        _.text = "{:.12g}".format((profile_depth - layer.top_height) * 100)
        if not np.isnan(layer.thickness):
            _ = ET.SubElement(e_layer, f'{ns}thickness', attrib={'uom': 'cm'})
            _.text = "{:.12g}".format(layer.thickness * 100)
        if layer.grain_1 is not None:
            _ = ET.SubElement(e_layer, f'{ns}grainFormPrimary')
            _.text = layer.grain_1
        if layer.grain_1 is not None and layer.grain_2 is not None:
            _ = ET.SubElement(e_layer, f'{ns}grainFormSecondary')
            _.text = layer.grain_2
        if layer.grain_size is not None:
            _ = ET.SubElement(e_layer, f'{ns}grainSize', attrib={'uom': 'mm'})
            _c = ET.SubElement(_, f'{ns}Components')
            _ = ET.SubElement(_c, f'{ns}avg')
            _.text = "{:.12g}".format(layer.grain_size * 1e3)
            if 'grain_size_max' in layer and not np.isnan(layer.grain_size_max):
                _ = ET.SubElement(_c, f'{ns}avgMax')
                _.text = "{:.12g}".format(layer.grain_size_max * 1e3)
        if layer.hardness is not None:
            _ = ET.SubElement(e_layer, f'{ns}hardness', attrib={'uom': ''})
            _.text = layer.hardness
        if layer.wetness is not None:
            _ = ET.SubElement(e_layer, f'{ns}wetness', attrib={'uom': ''})
            _.text = layer.wetness
        if 'loc' in layer and layer.loc is not None:
            _ = ET.SubElement(e_layer, f'{ns}layerOfConcern')
            _.text = layer.loc
        _md = None
        if ('comment' in layer and layer.comment is not None and len(layer.comment) > 0):
            _md = ET.SubElement(e_layer, f'{ns}metaData')
            _ = ET.SubElement(_md, f'{ns}comment')
            _.text = str(layer.comment)
        if 'additional_data' in layer and layer.additional_data is not None:
            if _md is None:
                _md = ET.SubElement(e_layer, f'{ns}metaData')
                _append_additional_data(_md, layer.additional_data, ns=ns)
        if 'formation_time' in layer and layer.formation_time is not None:
            _ = ET.SubElement(e_layer, f'{ns}validFormationTime')
            _t = ET.SubElement(_, f'{ns}TimeInstant')
            _ = ET.SubElement(_t, f'{ns}timePosition')
            _.text = layer.formation_time.isoformat()
        elif ('formation_period_begin' in layer and 'formation_period_end' in layer
              and layer.formation_period_begin is not None and layer.formation_period_end is not None):
            _ = ET.SubElement(e_layer, f'{ns}validFormationTime')
            _t = ET.SubElement(_, f'{ns}TimePeriod')
            _ = ET.SubElement(_t, f'{ns}beginPosition')
            _.text = layer.formation_period_begin.isoformat()
            _ = ET.SubElement(_t, f'{ns}endPosition')
            _.text = layer.formation_period_end.isoformat()

    _append_additional_data(e_s, s_strat.additional_data, ns=ns)


_density_mom = {'6.0.5': ['Snow Tube', 'Snow Cylinder', 'Snow Cutter', 'Denoth Probe', 'other']}


def _insert_density_profile(e_r, s_p, config):
    if s_p is None:
        return

    ns = config['ns']
    profile_depth = s_p.profile_depth if s_p.profile_depth is not None else config['profile_depth']
    version = config['version']

    e_p = ET.SubElement(e_r, f'{ns}densityProfile',
                        attrib=_gen_common_attrib(s_p, config=config))

    e_md = _gen_common_metadata(
        e_p, s_p, config=config,
        name = 'densityMetaData',
        additional_metadata = [
            {'value': s_p.method_of_measurement, 'default_value': 'other',
             'values': _density_mom[version] if version in _density_mom else None,
             'key': 'methodOfMeas'},
            {'value': s_p.uncertainty_of_measurement, 'key': 'uncertaintyOfMeas', 'attrib': {'uom': 'kgm-3'}},
            {'value': s_p.quality_of_measurement, 'min_version': '6.0.6', 'comment_title': 'Quality of measurement',
             'key': 'qualityOfMeas'},
            {'value': s_p.probed_volume, 'key': 'probeVolume', 'factor': 1e6, 'attrib': {'uom': 'cm3'}},
            {'value': s_p.probed_diameter, 'key': 'probeDiameter', 'factor': 100, 'attrib': {'uom': 'cm'}},
            {'value': s_p.probed_length, 'key': 'probeLength', 'factor': 100, 'attrib': {'uom': 'cm'}},
            {'value': s_p.probed_thickness, 'key': 'probedThickness', 'factor': 100, 'attrib': {'uom': 'cm'}}, ])

    if s_p.profile_nr is not None:
        _ = ET.SubElement(e_p, f'{ns}profileNr')
        _.text = str(s_p.profile_nr)

    # Loop layers
    for _, layer in s_p.data.iterrows():
        e_layer = ET.SubElement(e_p, f'{ns}Layer')
        _ = ET.SubElement(e_layer, f'{ns}depthTop', attrib={'uom': 'cm'})
        if profile_depth - layer.top_height < 0:
            raise ValueError(f'Top height ({layer.top_height}m) > profile depth ({profile_depth}m) '
                             'in density profile)')
        _.text = "{:.12g}".format((profile_depth - layer.top_height) * 100)
        if not np.isnan(layer.thickness):
            _ = ET.SubElement(e_layer, f'{ns}thickness', attrib={'uom': 'cm'})
            _.text = "{:.12g}".format(layer.thickness * 100)
        attrib = {'uom': 'kgm-3'}
        if 'uncertainty' in layer and not np.isnan(layer.uncertainty) and version >= '6.0.6':
            attrib['uncertainty'] = "{:.12g}".format(layer.uncertainty)
        if 'quality' in layer and layer.quality is not None and version >= '6.0.6':
            attrib['quality'] = layer.quality
        _ = ET.SubElement(e_layer, f'{ns}density', attrib=attrib)
        _.text = "{:.12g}".format(layer.density)

    _append_additional_data(e_p, s_p.additional_data, ns=ns)


def _insert_temperature_profile(e_r, s_p, config):
    if s_p is None:
        return

    ns = config['ns']
    profile_depth = s_p.profile_depth if s_p.profile_depth is not None else config['profile_depth']
    version = config['version']

    e_p = ET.SubElement(e_r, f'{ns}tempProfile',
                        attrib=_gen_common_attrib(s_p, config=config))

    e_md = _gen_common_metadata(
        e_p, s_p, config=config,
        name = 'tempMetaData',
        additional_metadata = [
            {'value': s_p.method_of_measurement, 'min_version': '6.0.6', 'comment_title': 'Measurement method',
             'key': 'methodOfMeas'},
            {'value': s_p.uncertainty_of_measurement, 'key': 'uncertaintyOfMeas', 'attrib': {'uom': 'degC'},
             'min_version': '6.0.6', 'comment_title': 'Uncertainty of measurement (degC)'},
            {'value': s_p.quality_of_measurement, 'min_version': '6.0.6', 'comment_title': 'Quality of measurement',
             'key': 'qualityOfMeas'}, ])

    # Loop layers
    for _, layer in s_p.data.iterrows():
        e_layer = ET.SubElement(e_p, f'{ns}Obs')
        _ = ET.SubElement(e_layer, f'{ns}depth', attrib={'uom': 'cm'})
        if profile_depth - layer.height < 0:
            raise ValueError(f'Height ({layer.height}m) > profile depth ({profile_depth}m) '
                             'in temperature profile)')
        _.text = "{:.12g}".format((profile_depth - layer.height) * 100)
        _ = ET.SubElement(e_layer, f'{ns}snowTemp', attrib={'uom': 'degC'})
        _.text = "{:.12g}".format(layer.temperature)
        if 'uncertainty' in layer and not np.isnan(layer.uncertainty) and version >= '6.0.6':
            _ = "{:.12g}".format(layer.uncertainty)
        if 'quality' in layer and layer.quality is not None and version >= '6.0.6':
            _ = ET.SubElement(e_layer, f'{ns}qualityOfMeas')
            _.text = layer.quality

    if version >= "6.0.6" and s_p.profile_nr is not None:
        _ = ET.SubElement(e_p, f'{ns}profileNr')
        _.text = str(s_p.profile_nr)

    _append_additional_data(e_p, s_p.additional_data, ns=ns)


_lwc_mom = {'6.0.5': ['Denoth Probe', 'Snow Fork', 'other']}


def _insert_lwc_profile(e_r, s_p, config):
    if s_p is None:
        return

    ns = config['ns']
    profile_depth = s_p.profile_depth if s_p.profile_depth is not None else config['profile_depth']
    version = config['version']

    e_p = ET.SubElement(e_r, f'{ns}lwcProfile',
                        attrib=_gen_common_attrib(s_p, config=config))

    e_md = _gen_common_metadata(
        e_p, s_p, config=config,
        name = 'lwcMetaData',
        additional_metadata = [
            {'value': s_p.method_of_measurement, 'default_value': 'other',
             'values': _lwc_mom[version] if version in _lwc_mom else None,
             'key': 'methodOfMeas'},
            {'value': s_p.uncertainty_of_measurement, 'key': 'uncertaintyOfMeas', 'attrib': {'uom': '% by Vol'}},
            {'value': s_p.quality_of_measurement, 'min_version': '6.0.6', 'comment_title': 'Quality of measurement',
             'key': 'qualityOfMeas'},
            {'value': s_p.probed_thickness, 'key': 'probedThickness', 'factor': 100, 'attrib': {'uom': 'cm'}}, ])

    if s_p.profile_nr is not None:
        _ = ET.SubElement(e_p, f'{ns}profileNr')
        _.text = str(s_p.profile_nr)

    # Loop layers
    for _, layer in s_p.data.iterrows():
        e_layer = ET.SubElement(e_p, f'{ns}Layer')
        _ = ET.SubElement(e_layer, f'{ns}depthTop', attrib={'uom': 'cm'})
        if profile_depth - layer.top_height < 0:
            raise ValueError(f'Top height ({layer.top_height}m) > profile depth ({profile_depth}m) '
                             'in LWC profile)')
        _.text = "{:.12g}".format((profile_depth - layer.top_height) * 100)
        if not np.isnan(layer.thickness):
            _ = ET.SubElement(e_layer, f'{ns}thickness', attrib={'uom': 'cm'})
            _.text = "{:.12g}".format(layer.thickness * 100)
        attrib = {'uom': '% by Vol'}
        if 'uncertainty' in layer and not np.isnan(layer.uncertainty) and version >= '6.0.6':
            attrib['uncertainty'] = "{:.12g}".format(layer.uncertainty)
        if 'quality' in layer and layer.quality is not None and version >= '6.0.6':
            attrib['quality'] = layer.quality
        _ = ET.SubElement(e_layer, f'{ns}lwc', attrib=attrib)
        _.text = "{:.12g}".format(layer.lwc)

    _append_additional_data(e_p, s_p.additional_data, ns=ns)


_strength_mom = {'6.0.5': ['Shear Frame', 'other']}


def _insert_strength_profile(e_r, s_p, config):
    if s_p is None:
        return

    ns = config['ns']
    profile_depth = s_p.profile_depth if s_p.profile_depth is not None else config['profile_depth']
    version = config['version']

    e_p = ET.SubElement(e_r, f'{ns}strengthProfile',
                        attrib=_gen_common_attrib(s_p, config=config))

    e_md = _gen_common_metadata(
        e_p, s_p, config=config,
        name = 'strengthMetaData',
        additional_metadata = [
            {'value': s_p.strength_type, 'key': 'strengthType', 'values': ['compressive', 'tensile', 'shear']},
            {'value': s_p.method_of_measurement, 'default_value': 'other',
             'values': _strength_mom[version] if version in _strength_mom else None,
             'key': 'methodOfMeas'},
            {'value': s_p.uncertainty_of_measurement, 'key': 'uncertaintyOfMeas', 'attrib': {'uom': 'Nm-2'}},
            {'value': s_p.quality_of_measurement, 'min_version': '6.0.6', 'comment_title': 'Quality of measurement',
             'key': 'qualityOfMeas'},
            {'value': s_p.probed_area, 'key': 'probedArea', 'factor': 1e4, 'attrib': {'uom': 'cm2'}}, ])

    if s_p.profile_nr is not None:
        _ = ET.SubElement(e_p, f'{ns}profileNr')
        _.text = str(s_p.profile_nr)

    # Loop layers
    for _, layer in s_p.data.iterrows():
        e_layer = ET.SubElement(e_p, f'{ns}Layer')
        _ = ET.SubElement(e_layer, f'{ns}depthTop', attrib={'uom': 'cm'})
        if profile_depth - layer.top_height < 0:
            raise ValueError(f'Top height ({layer.top_height}m) > profile depth ({profile_depth}m) '
                             'in strength profile)')
        _.text = "{:.12g}".format((profile_depth - layer.top_height) * 100)
        if not np.isnan(layer.thickness):
            _ = ET.SubElement(e_layer, f'{ns}thickness', attrib={'uom': 'cm'})
            _.text = "{:.12g}".format(layer.thickness * 100)
        attrib = {'uom': 'Nm-2'}
        if 'uncertainty' in layer and not np.isnan(layer.uncertainty) and version >= '6.0.6':
            attrib['uncertainty'] = "{:.12g}".format(layer.uncertainty)
        if 'quality' in layer and layer.quality is not None and version >= '6.0.6':
            attrib['quality'] = layer.quality
        _ = ET.SubElement(e_layer, f'{ns}strengthValue', attrib=attrib)
        _.text = "{:.12g}".format(layer.strength)
        if 'fracture_character' in layer and layer.fracture_character is not None:
            _ = ET.SubElement(e_layer, f'{ns}fractureCharacter')
            _.text = layer.fracture_character

    _append_additional_data(e_p, s_p.additional_data, ns=ns)


_impurity_mom = {'6.0.5': ['other']}
_impurity_type = {'6.0.5': ['Black Carbon', 'Dust', 'Isotopes']}


def _insert_impurity_profile(e_r, s_p, config):
    if s_p is None:
        return

    ns = config['ns']
    profile_depth = s_p.profile_depth if s_p.profile_depth is not None else config['profile_depth']
    version = config['version']

    e_p = ET.SubElement(e_r, f'{ns}impurityProfile',
                        attrib=_gen_common_attrib(s_p, config=config))

    e_md = _gen_common_metadata(
        e_p, s_p, config=config,
        name = 'impurityMetaData',
        additional_metadata = [
            {'value': s_p.impurity_type, 'default_value': 'other',
             'values': _impurity_type[version] if version in _impurity_type else None,
             'key': 'impurity'},
            {'value': s_p.method_of_measurement, 'default_value': 'other',
             'values': _impurity_mom[version] if version in _impurity_mom else None,
             'key': 'methodOfMeas'},
            {'value': s_p.uncertainty_of_measurement, 'key': 'uncertaintyOfMeas', 'attrib': {'uom': '%'}},
            {'value': s_p.quality_of_measurement, 'min_version': '6.0.6', 'comment_title': 'Quality of measurement',
             'key': 'qualityOfMeas'},
            {'value': s_p.probed_thickness, 'key': 'probedThickness', 'factor': 100, 'attrib': {'uom': 'cm'}},
            {'value': s_p.probed_volume, 'key': 'probedVolume', 'factor': 1e6, 'attrib': {'uom': 'cm3'},
             'min_version': '6.0.6', 'comment_title': 'Probe thickness (cm3)'},
            {'value': s_p.probed_diameter, 'key': 'probedDiameter', 'factor': 100, 'attrib': {'uom': 'cm'},
             'min_version': '6.0.6', 'comment_title': 'Probe thickness (cm3)'},
            {'value': s_p.probed_length, 'key': 'probedLength', 'factor': 100, 'attrib': {'uom': 'cm'},
             'min_version': '6.0.6', 'comment_title': 'Probe thickness (cm3)'}, ])

    if s_p.profile_nr is not None:
        _ = ET.SubElement(e_p, f'{ns}profileNr')
        _.text = str(s_p.profile_nr)

    # Loop layers
    for _, layer in s_p.data.iterrows():
        if (('mass_fraction' in layer and not np.isnan(layer.mass_fraction)) or
            ('volume_fraction' in layer and not np.isnan(layer.volume_fraction))):
            e_layer = ET.SubElement(e_p, f'{ns}Layer')
            _ = ET.SubElement(e_layer, f'{ns}depthTop', attrib={'uom': 'cm'})
            if profile_depth - layer.top_height < 0:
                raise ValueError(f'Top height ({layer.top_height}m) > profile depth ({profile_depth}m) '
                                 'in impurity profile)')
            _.text = "{:.12g}".format((profile_depth - layer.top_height) * 100)
            if not np.isnan(layer.thickness):
                _ = ET.SubElement(e_layer, f'{ns}thickness', attrib={'uom': 'cm'})
                _.text = "{:.12g}".format(layer.thickness * 100)
            attrib = {'uom': '%'}
            if 'uncertainty' in layer and not np.isnan(layer.uncertainty) and version >= '6.0.6':
                attrib['uncertainty'] = "{:.12g}".format(layer.uncertainty)
            if 'quality' in layer and layer.quality is not None and version >= '6.0.6':
                attrib['quality'] = layer.quality
            if 'mass_fraction' in layer and not np.isnan(layer.mass_fraction):
                _ = ET.SubElement(e_layer, f'{ns}massFraction', attrib=attrib)
                _.text = "{:.12g}".format(layer.mass_fraction)
            else:
                _ = ET.SubElement(e_layer, f'{ns}volumeFraction', attrib=attrib)
                _.text = "{:.12g}".format(layer.volume_fraction)

    _append_additional_data(e_p, s_p.additional_data, ns=ns)


def _insert_otherscalar_profile(e_r, s_p, config):
    if s_p is None:
        return

    ns = config['ns']
    profile_depth = s_p.profile_depth if s_p.profile_depth is not None else config['profile_depth']
    print('Profile depth in ScalarProfile', profile_depth)
    version = config['version']

    if version < '6.0.6':
        logging.warning(f'Other scalar profile not stored in CAAML XML v{version}.')
        return

    e_p = ET.SubElement(e_r, f'{ns}otherScalarProfile',
                        attrib=_gen_common_attrib(s_p, config=config))

    e_md = _gen_common_metadata(
        e_p, s_p, config=config,
        name = 'otherScalarMetaData',
        additional_metadata = [
            {'value': s_p.parameter, 'key': 'parameter'},
            {'value': s_p.method_of_measurement, 'key': 'methodOfMeas'},
            {'value': s_p.unit, 'key': 'uom'},
            {'value': s_p.uncertainty_of_measurement, 'key': 'uncertaintyOfMeas'},
            {'value': s_p.quality_of_measurement, 'key': 'qualityOfMeas'}, ])

    if s_p.profile_nr is not None:
        _ = ET.SubElement(e_p, f'{ns}profileNr')
        _.text = str(s_p.profile_nr)

    # Loop layers
    for _, layer in s_p.data.iterrows():
        e_layer = ET.SubElement(e_p, f'{ns}Layer')
        _ = ET.SubElement(e_layer, f'{ns}depthTop', attrib={'uom': 'cm'})
        if profile_depth - layer.top_height < 0:
            raise ValueError(f'Top height ({layer.top_height}m) > profile depth ({profile_depth}m) '
                             'in other scalar profile)')
        _.text = "{:.12g}".format((profile_depth - layer.top_height) * 100)
        if not np.isnan(layer.thickness):
            _ = ET.SubElement(e_layer, f'{ns}thickness', attrib={'uom': 'cm'})
            _.text = "{:.12g}".format(layer.thickness * 100)
        attrib = {}
        if 'uncertainty' in layer and not np.isnan(layer.uncertainty):
            attrib['uncertainty'] = "{:.12g}".format(layer.uncertainty)
        if 'quality' in layer and layer.quality is not None:
            attrib['quality'] = layer.quality
        _ = ET.SubElement(e_layer, f'{ns}value', attrib=attrib)
        _.text = "{:.12g}".format(layer.data)

    _append_additional_data(e_p, s_p.additional_data, ns=ns)


def _insert_othervectorial_profile(e_r, s_p, config):
    if s_p is None:
        return

    ns = config['ns']
    profile_depth = s_p.profile_depth if s_p.profile_depth is not None else config['profile_depth']
    version = config['version']

    if version < '6.0.6':
        logging.warning(f'Other vectorial profile not stored in CAAML XML v{version}.')
        return

    e_p = ET.SubElement(e_r, f'{ns}otherVectorialProfile',
                        attrib=_gen_common_attrib(s_p, config=config))

    e_md = _gen_common_metadata(
        e_p, s_p, config=config,
        name = 'otherVectorialMetaData',
        additional_metadata = [
            {'value': s_p.parameter, 'key': 'parameter'},
            {'value': s_p.rank, 'key': 'rank'},
            {'value': s_p.method_of_measurement, 'key': 'methodOfMeas'},
            {'value': s_p.unit, 'key': 'uom'},
            {'value': s_p.uncertainty_of_measurement, 'key': 'uncertaintyOfMeas'},
            {'value': s_p.quality_of_measurement, 'key': 'qualityOfMeas'}, ])

    if s_p.profile_nr is not None:
        _ = ET.SubElement(e_p, f'{ns}profileNr')
        _.text = str(s_p.profile_nr)

    # Loop layers
    for _, layer in s_p.data.iterrows():
        e_layer = ET.SubElement(e_p, f'{ns}Layer')
        _ = ET.SubElement(e_layer, f'{ns}depthTop', attrib={'uom': 'cm'})
        if profile_depth - layer.top_height < 0:
            raise ValueError(f'Top height ({layer.top_height}m) > profile depth ({profile_depth}m) '
                             'in vectorial profile)')
        _.text = "{:.12g}".format((profile_depth - layer.top_height) * 100)
        if not np.isnan(layer.thickness):
            _ = ET.SubElement(e_layer, f'{ns}thickness', attrib={'uom': 'cm'})
            _.text = "{:.12g}".format(layer.thickness * 100)
        attrib = {}
        if 'uncertainty' in layer and not np.isnan(layer.uncertainty):
            attrib['uncertainty'] = "{:.12g}".format(layer.uncertainty)
        if 'quality' in layer and layer.quality is not None:
            attrib['quality'] = layer.quality
        _ = ET.SubElement(e_layer, f'{ns}value', attrib=attrib)
        _.text = ' '.join(["{:.12g}".format(e) for e in layer.data])

    _append_additional_data(e_p, s_p.additional_data, ns=ns)


_ssa_mom = {'6.0.5': ['Ice Cube', 'other']}


def _insert_ssa_profile(e_r, s_p, config):
    if s_p is None:
        return

    ns = config['ns']
    profile_depth = s_p.profile_depth if s_p.profile_depth is not None else config['profile_depth']
    version = config['version']

    e_p = ET.SubElement(e_r, f'{ns}specSurfAreaProfile',
                        attrib=_gen_common_attrib(s_p, config=config))

    e_md = _gen_common_metadata(
        e_p, s_p, config=config,
        name = 'specSurfAreaMetaData',
        additional_metadata = [
            {'value': s_p.method_of_measurement, 'default_value': 'other',
             'values': _ssa_mom[version] if version in _ssa_mom else None,
             'key': 'methodOfMeas'},
            {'value': s_p.uncertainty_of_measurement, 'key': 'uncertaintyOfMeas', 'attrib': {'uom': 'm2kg-1'}},
            {'value': s_p.quality_of_measurement, 'min_version': '6.0.6', 'comment_title': 'Quality of measurement',
             'key': 'qualityOfMeas'},
            {'value': s_p.probed_thickness, 'key': 'probedThickness', 'factor': 100, 'attrib': {'uom': 'cm'}}, ])

    if s_p.profile_nr is not None:
        _ = ET.SubElement(e_p, f'{ns}profileNr')
        _.text = str(s_p.profile_nr)

    # Loop layers
    import snowprofile.profiles
    if isinstance(s_p, snowprofile.profiles.SSAProfile):
        for _, layer in s_p.data.iterrows():
            e_layer = ET.SubElement(e_p, f'{ns}Layer')
            _ = ET.SubElement(e_layer, f'{ns}depthTop', attrib={'uom': 'cm'})
            if profile_depth - layer.top_height < 0:
                raise ValueError(f'Top height ({layer.top_height}m) > profile depth ({profile_depth}m) '
                                 'in SSA profile)')
            _.text = "{:.12g}".format((profile_depth - layer.top_height) * 100)
            if not np.isnan(layer.thickness):
                _ = ET.SubElement(e_layer, f'{ns}thickness', attrib={'uom': 'cm'})
                _.text = "{:.12g}".format(layer.thickness * 100)
            attrib = {'uom': 'm2kg-1'}
            if 'uncertainty' in layer and not np.isnan(layer.uncertainty) and version >= '6.0.6':
                attrib['uncertainty'] = "{:.12g}".format(layer.uncertainty)
            if 'quality' in layer and layer.quality is not None and version >= '6.0.6':
                attrib['quality'] = layer.quality
            _ = ET.SubElement(e_layer, f'{ns}specSurfArea', attrib=attrib)
            _.text = "{:.12g}".format(layer.ssa)
    elif isinstance(s_p, snowprofile.profiles.SSAPointProfile):
        e_mc = ET.SubElement(e_p, f'{ns}MeasurementComponents', attrib={
            'uomDepth': 'cm',
            'uomSpecSurfArea': 'm2kg-1'})
        _ = ET.SubElement(e_mc, f'{ns}depth')
        _.text = 'template'
        _ = ET.SubElement(e_mc, f'{ns}specSurfArea')
        _.text = 'template'
        e_m = ET.SubElement(e_p, f'{ns}Measurements')
        e_m = ET.SubElement(e_m, f'{ns}tupleList')
        tl = []
        for _, layer in s_p.data.iterrows():
            if profile_depth - layer.height < 0:
                raise ValueError(f'Top height ({layer.height}m) > profile depth ({profile_depth}m) '
                                 'in SSA profile)')
            _depth = (profile_depth - layer.height) * 100
            tl.append(f'{_depth:.12g},{layer.ssa:.12g}')
        e_m.text = ' '.join(tl)

    _append_additional_data(e_p, s_p.additional_data, ns=ns)


_hardness_mom = {'6.0.5': ['SnowMicroPen', 'Ram Sonde', 'Push-Pull Gauge', 'other']}


def _insert_hardness_profile(e_r, s_p, config):
    if s_p is None:
        return

    ns = config['ns']
    profile_depth = s_p.profile_depth if s_p.profile_depth is not None else config['profile_depth']
    version = config['version']

    e_p = ET.SubElement(e_r, f'{ns}hardnessProfile',
                        attrib={
                            'uomWeightHammer': 'kg',
                            'uomWeightTube': 'kg',
                            'uomDropHeight': 'cm',
                            **_gen_common_attrib(s_p, config=config)})

    e_md = _gen_common_metadata(
        e_p, s_p, config=config,
        name = 'hardnessMetaData',
        additional_metadata = [
            {'value': s_p.method_of_measurement, 'default_value': 'other',
             'values': _hardness_mom[version] if version in _hardness_mom else None,
             'key': 'methodOfMeas'},
            {'value': s_p.uncertainty_of_measurement, 'key': 'uncertaintyOfMeas', 'attrib': {'uom': 'N'}},
            {'value': s_p.quality_of_measurement, 'min_version': '6.0.6', 'comment_title': 'Quality of measurement',
             'key': 'qualityOfMeas'},
            {'value': s_p.surface_of_indentation, 'key': 'surfOfIndentation', 'factor': 10000,
             'attrib': {'uom': 'cm2'}},
            {'value': s_p.penetration_speed, 'key': 'penetrationSpeed', 'attrib': {'uom': 'ms-1'},
             'min_version': '6.0.6', 'comment_title': 'Penetration speed'}, ])

    if s_p.profile_nr is not None:
        _ = ET.SubElement(e_p, f'{ns}profileNr')
        _.text = str(s_p.profile_nr)

    # Loop layers
    import snowprofile.profiles
    if isinstance(s_p, snowprofile.profiles.HardnessProfile):
        for _, layer in s_p.data.iterrows():
            e_layer = ET.SubElement(e_p, f'{ns}Layer')
            _ = ET.SubElement(e_layer, f'{ns}depthTop', attrib={'uom': 'cm'})
            if profile_depth - layer.top_height < 0:
                raise ValueError(f'Top height ({layer.top_height}m) > profile depth ({profile_depth}m) '
                                 'in hardness profile)')
            _.text = "{:.12g}".format((profile_depth - layer.top_height) * 100)
            if not np.isnan(layer.thickness):
                _ = ET.SubElement(e_layer, f'{ns}thickness', attrib={'uom': 'cm'})
                _.text = "{:.12g}".format(layer.thickness * 100)
            attrib = {'uom': 'N'}
            _ = ET.SubElement(e_layer, f'{ns}hardness', attrib=attrib)
            _.text = "{:.12g}".format(layer.hardness)
            if 'weight_hammer' in layer and not np.isnan(layer.weight_hammer):
                _ = ET.SubElement(e_layer, f'{ns}weightHammer')
                _.text = "{:.12g}".format(layer.weight_hammer)
            if 'weight_tube' in layer and not np.isnan(layer.weight_tube):
                _ = ET.SubElement(e_layer, f'{ns}weightTube')
                _.text = "{:.12g}".format(layer.weight_tube)
            if 'n_drops' in layer and not np.isnan(layer.n_drops):
                _ = ET.SubElement(e_layer, f'{ns}nDrops')
                _.text = "{:.12g}".format(layer.n_drops)
            if 'drop_height' in layer and not np.isnan(layer.drop_height):
                _ = ET.SubElement(e_layer, f'{ns}dropHeight')
                _.text = "{:.12g}".format(layer.drop_height * 100)
    elif isinstance(s_p, snowprofile.profiles.HardnessPointProfile):
        e_mc = ET.SubElement(e_p, f'{ns}MeasurementComponents', attrib={
            'uomDepth': 'cm',
            'uomHardness': 'N'})
        _ = ET.SubElement(e_mc, f'{ns}depth')
        _.text = 'template'
        _ = ET.SubElement(e_mc, f'{ns}penRes')
        _.text = 'template'
        e_m = ET.SubElement(e_p, f'{ns}Measurements')
        e_m = ET.SubElement(e_m, f'{ns}tupleList')
        tl = []
        for _, layer in s_p.data.iterrows():
            if profile_depth - layer.height < 0:
                raise ValueError(f'Top height ({layer.height}m) > profile depth ({profile_depth}m) '
                                 'in hardness profile)')
            _depth = (profile_depth - layer.height) * 100
            tl.append(f'{_depth:.12g},{layer.hardness:.12g}')
        e_m.text = ' '.join(tl)

    _append_additional_data(e_p, s_p.additional_data, ns=ns)


def _insert_stb_test(e_r, s_t, config):
    if s_t is None:
        return

    ns = config['ns']
    profile_depth = config['profile_depth']

    import snowprofile.stability_tests

    if isinstance(s_t, snowprofile.stability_tests.CTStabilityTest):
        e_t = ET.SubElement(e_r, f'{ns}ComprTest',
                            attrib=_gen_common_attrib(s_t, config=config))
        _stb_test_common(e_t, s_t, config=config)

        if len(s_t.results) == 0:  # No failure
            _ = ET.SubElement(e_t, f'{ns}noFailure')
        else:  # Positive result(s)
            for result in s_t.results:
                e_fail = ET.SubElement(e_t, f'{ns}failedOn')
                # Failure layer details
                _stb_test_layer_details(e_fail, result, ns=ns, profile_depth=profile_depth)
                # CT result
                e_resu = ET.SubElement(e_fail, f'{ns}Results')
                if result.fracture_character is not None:
                    _ = ET.SubElement(e_resu, f'{ns}fractureCharacter')
                    _.text = result.fracture_character
                _ = ET.SubElement(e_resu, f'{ns}testScore')
                _.text = '{:d}'.format(result.test_score)
    elif isinstance(s_t, snowprofile.stability_tests.ECTStabilityTest):
        e_t = ET.SubElement(e_r, f'{ns}ExtColumnTest',
                            attrib=_gen_common_attrib(s_t, config=config))
        _stb_test_common(e_t, s_t, config=config)

        if len(s_t.results) == 0:  # No failure
            _ = ET.SubElement(e_t, f'{ns}noFailure')
        else:  # Positive result(s)
            for result in s_t.results:
                e_fail = ET.SubElement(e_t, f'{ns}failedOn')
                # Failure layer details
                _stb_test_layer_details(e_fail, result, ns=ns, profile_depth=profile_depth)
                # ECT result
                e_resu = ET.SubElement(e_fail, f'{ns}Results')
                _ = ET.SubElement(e_resu, f'{ns}testScore')
                if result.test_score == 0 and result.propagation:
                    _.text = 'ECTPV'
                elif result.test_score == 0:
                    _.text = 'ECTN1'
                else:
                    _.text = 'ECT{p}{n}'.format(p = 'P' if result.propagation else 'N', n = result.test_score)
    elif isinstance(s_t, snowprofile.stability_tests.RBStabilityTest):
        e_t = ET.SubElement(e_r, f'{ns}RBlockTest',
                            attrib=_gen_common_attrib(s_t, config=config))
        _stb_test_common(e_t, s_t, config=config)

        if len(s_t.results) == 0:  # No failure
            _ = ET.SubElement(e_t, f'{ns}noFailure')
        else:  # Positive result(s)
            for result in s_t.results:
                e_fail = ET.SubElement(e_t, f'{ns}failedOn')
                # Failure layer details
                _stb_test_layer_details(e_fail, result, ns=ns, profile_depth=profile_depth)
                # RB result
                e_resu = ET.SubElement(e_fail, f'{ns}Results')
                if result.fracture_character is not None:
                    _ = ET.SubElement(e_resu, f'{ns}fractureCharacter')
                    _.text = result.fracture_character
                if result.release_type is not None:
                    _ = ET.SubElement(e_resu, f'{ns}releaseType')
                    _.text = result.release_type
                _ = ET.SubElement(e_resu, f'{ns}testScore')
                _.text = f'RB{result.test_score}'
    elif isinstance(s_t, snowprofile.stability_tests.ShearFrameStabilityTest):
        e_t = ET.SubElement(e_r, f'{ns}ShearFrameTest',
                            attrib=_gen_common_attrib(s_t, config=config))
        _stb_test_common(e_t, s_t, config=config)

        if len(s_t.results) == 0:  # No failure
            _ = ET.SubElement(e_t, f'{ns}noFailure')
        else:  # Positive result(s)
            for result in s_t.results:
                e_fail = ET.SubElement(e_t, f'{ns}failedOn')
                # Failure layer details
                _stb_test_layer_details(e_fail, result, ns=ns, profile_depth=profile_depth)
                # SF result
                e_resu = ET.SubElement(e_fail, f'{ns}Results')
                if result.fracture_character is not None:
                    _ = ET.SubElement(e_resu, f'{ns}fractureCharacter')
                    _.text = result.fracture_character
                _ = ET.SubElement(e_resu, f'{ns}failureForce', attrib={'uom': 'N'})
                _.text = "{:.12g}".format(result.force)
    elif isinstance(s_t, snowprofile.stability_tests.PSTStabilityTest):
        e_t = ET.SubElement(e_r, f'{ns}PropSawTest',
                            attrib=_gen_common_attrib(s_t, config=config))
        _stb_test_common(e_t, s_t, config=config)
        e_t = ET.SubElement(e_t, f'{ns}failedOn')

        # Failure layer details
        _stb_test_layer_details(e_t, s_t, ns=ns, profile_depth=profile_depth)
        # ECT result
        e_resu = ET.SubElement(e_t, f'{ns}Results')
        _ = ET.SubElement(e_resu, f'{ns}fracturePropagation')
        _.text = s_t.propagation
        _ = ET.SubElement(e_resu, f'{ns}cutLength', attrib={'uom': 'cm'})
        _.text = "{:.12g}".format(s_t.cut_length * 100)
        _ = ET.SubElement(e_resu, f'{ns}columnLength', attrib={'uom': 'cm'})
        if s_t.column_length is None:
            _.text = "150"
        else:
            _.text = "{:.12g}".format(s_t.column_length * 100)
    else:
        raise ValueError(f'Unknown stability test type {type(s_t)}.')


def _stb_test_common(e_t, s_t, config={'ns': ''}):
    ns = config['ns']
    if s_t.comment is not None:
        _ = ET.SubElement(e_t, f'{ns}metaData')
        _ = ET.SubElement(_, f'{ns}comment')
        _.text = s_t.comment

    if s_t.test_nr is not None and config['version'] >= '6.0.6':
        _ = ET.SubElement(e_t, f'{ns}testNr')
        _.text = str(s_t.test_nr)

    _append_additional_data(e_t, s_t.additional_data, ns=ns)


def _stb_test_layer_details(e_fail, result, ns='', profile_depth=0):
    e_layer = ET.SubElement(e_fail, f'{ns}Layer')
    if result.layer_comment is not None and len(result.layer_comment) > 0:
        _md = ET.SubElement(e_layer, f'{ns}metaData')
        _ = ET.SubElement(_md, f'{ns}comment')
        _.text = str(result.layer_comment)

    _ = ET.SubElement(e_layer, f'{ns}depthTop', attrib={'uom': 'cm'})
    _.text = "{:.12g}".format((profile_depth - result.height) * 100)

    if result.layer_thickness is not None:
        _ = ET.SubElement(e_layer, f'{ns}thickness', attrib={'uom': 'cm'})
        _.text = "{:.12g}".format(result.layer_thickness * 100)

    if result.grain_1 is not None:
        _ = ET.SubElement(e_layer, f'{ns}grainFormPrimary')
        _.text = result.grain_1

    if result.grain_2 is not None:
        _ = ET.SubElement(e_layer, f'{ns}grainFormSecondary')
        _.text = result.grain_2

    if result.grain_size is not None:
        _ = ET.SubElement(e_layer, f'{ns}grainSize', attrib={'uom': 'mm'})
        _c = ET.SubElement(_, f'{ns}Components')
        _ = ET.SubElement(_c, f'{ns}avg')
        _.text = "{:.12g}".format(result.grain_size * 1e3)
        if result.grain_size_max is not None:
            _ = ET.SubElement(_c, f'{ns}avgMax')
            _.text = "{:.12g}".format(result.grain_size_max * 1e3)
    _md = None

    if result.layer_formation_time is not None:
        _ = ET.SubElement(e_layer, f'{ns}validFormationTime')
        _t = ET.SubElement(_, f'{ns}TimeInstant')
        _ = ET.SubElement(_t, f'{ns}timePosition')
        _.text = result.layer_formation_time.isoformat()
    elif (result.layer_formation_period is not None
          and result.layer_formation_period[0] is not None
          and result.layer_formation_period[1] is not None):
        _ = ET.SubElement(e_layer, f'{ns}validFormationTime')
        _t = ET.SubElement(_, f'{ns}TimePeriod')
        _ = ET.SubElement(_t, f'{ns}beginPosition')
        _.text = result.layer_formation_period[0].isoformat()
        _ = ET.SubElement(_t, f'{ns}endPosition')
        _.text = result.layer_formation_period[1].isoformat()

    if result.layer_additional_data is not None:
        if _md is None:
            _md = ET.SubElement(e_layer, f'{ns}metaData')
            _append_additional_data(_md, result.additional_data, ns=ns)
