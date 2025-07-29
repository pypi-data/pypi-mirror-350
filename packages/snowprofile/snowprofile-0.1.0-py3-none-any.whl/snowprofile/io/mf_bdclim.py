# -*- coding: utf-8 -*-

import logging
import datetime

from snowprofile import _utils


def read_mf_bdclim(numposte, date, db_config={}):
    """
    Read snow profile from a database as stored in the Meteo-France climatological database.
    This routine is designed for internal use at Meteo-France only.

    You have to provide database url and creedentials:

    - Via the ``bd_config`` key
    - Or in the ``[io_mf_bdclim]`` key of the snowprofile configuration file (see :ref:`configuration`)

    Keys to configure connexion are ``host``, ``port``, ``dbname``, ``user``, ``password``.

    :param numposte: numposte
    :type numposte: str
    :param date: date to read
    :type date: python datetime object or str
    :param db_config: The information to connect to the database
    :type db_config: dict
    :returns: The SnowProfile object containin the data
    :rtype: SnowProfile
    """
    date = _utils.check_date(date)
    conn = _mf_conn(**db_config)

    # Read database
    metadata_poste = _get_poste_info(conn, numposte)
    metadata = _get_metadata_obs(conn, numposte, date)

    if metadata is None:
        conn.close()
        raise ValueError(f"Could not find data at date {date.isoformat(sep=' ')}")

    profil, profil_ram, profil_t, maxdepth = _get_profil(conn, numposte, date)

    conn.close()

    # Check topdepth
    if metadata['totdepth'] is None:
        metadata['totdepth'] = maxdepth
    else:
        if not maxdepth == metadata['totdepth']:
            logging.error(f'Incompatbile maximum depth: {maxdepth}cm in the database and '
                          f"{metadata['totdepth']} in the data.")

    # Process data
    from snowprofile import SnowProfile
    from snowprofile.profiles import DensityProfile, Stratigraphy, HardnessProfile, TemperatureProfile
    from snowprofile.classes import Location, Weather, Time

    loc = Location(
        id=str(numposte),
        name=f"{metadata_poste['name']} ({metadata_poste['name_detail']})",
        latitude=metadata_poste['lat'],
        longitude=metadata_poste['lon'],
        elevation=metadata_poste['elevation'],
        slope=metadata_poste['slope'],
        aspect=metadata_poste['aspect'])

    # Stratigraphy
    s = Stratigraphy(data={
        'top_height': [p[0] for p in profil],
        'thickness': [p[1] for p in profil],
        'grain_1': [p[2] for p in profil],
        'grain_2': [p[3] for p in profil],
        'grain_size': [p[4] for p in profil],
        'hardness': [p[5] for p in profil],
        'wetness': [p[6] for p in profil]})

    # Density profile
    d_v = [p[7] for p in profil]
    if len(set(d_v)) > 0 and set(d_v) != set([None, ]):
        d = [DensityProfile(data={
            'top_height': [p[0] for i, p in enumerate(profil) if d_v[i] is not None],
            'thickness': [p[1] for i, p in enumerate(profil) if d_v[i] is not None],
            'density': [p[7] for i, p in enumerate(profil) if d_v[i] is not None]}), ]
    else:
        d = []

    # TODO: Faire qqch de mesure LWC et cisso ?  <27-01-25, Léo Viallon-Galinier> #

    # RAM Profile
    if len(profil_ram) > 0:
        r = [HardnessProfile(data={
            'top_height': [p[0] for p in profil_ram],
            'thickness': [p[1] for p in profil_ram],
            'hardness': [p[2] for p in profil_ram]}), ]
    else:
        r = []

    # Temp profile
    if len(profil_t) > 0:
        t = [TemperatureProfile(data={
            'height': [p[0] for p in profil_t],
            'temperature': [p[1] for p in profil_t]}), ]
    else:
        t = []

    # Observer
    observer = _utils.get_default_observer(key='io_mf_bdclim')

    # Time
    time = Time(record_time=date)

    sp = SnowProfile(
        id=f'{numposte}-{date.isoformat()}',
        profile_comment=metadata['comment'],
        profile_depth=metadata['totdepth'],
        profile_swe=metadata['lwc'],
        location=loc,
        time=time,
        weather=Weather(cloudiness=metadata['ww'], air_temperature=float(metadata['t'])),
        observer=observer,
        stratigraphy_profile=s,
        density_profiles=d,
        hardness_profiles=r,
        temperature_profiles=t)

    return sp


def search_mf_bdclim_dates(numposte, date_min, date_max=None, db_config={}):
    """
    Get the dates of observation for given num poste and between
    date_min and date_max.

    See

    :param numposte: numposte
    :type numposte: str
    :param date_min: begin date for search
    :type date_min: python datetime object or str
    :param date_max: end date for search
    :type date_max: python datetime object or str
    :param db_config: The information to connect to the database
    :type db_config: dict
    :returns: list of available dates
    :rtype: list of python datetime objects
    """

    date_min = _utils.check_date(date_min)
    if date_max is not None:
        date_max = _utils.check_date(date_max)
    else:
        date_max = datetime.datetime.now()
    sql = ("SELECT DISTINCT dat FROM donnees_profil_neige "
           "WHERE num_poste='{numposte}' AND dat >= '{beg}' AND dat <= '{end}';".format(numposte=numposte,
                                                                                        beg=date_min.isoformat(sep=' '),
                                                                                        end=date_max.isoformat(sep=' '),
                                                                                        )
           )
    conn = _mf_conn(**db_config)
    with conn.cursor() as cur:
        cur.execute(sql)
        dates = cur.fetchall()
    conn.close()

    dates = [d[0] for d in dates]
    return dates


def _get_poste_info(conn, numposte):
    """
    Get the info from poste

    :param conn: connection to the database
    :type conn: psycopg2 connexion
    :param numposte: numposte
    :type numposte: str
    :returns: Information related to poste
    :rtype: dict
    """
    sql = ("SELECT nom_usuel, lieu_dit, alti, lat_dg, lon_dg, exposition_nivo, pente_nivo"
           " FROM poste_nivo WHERE num_poste='{}';".format(numposte))
    with conn.cursor() as cur:
        cur.execute(sql)
        data = cur.fetchone()

    aspect_raw = str(data[5])
    if aspect_raw in _correspStrAspect:
        aspect = _correspStrAspect[aspect_raw]
    else:
        aspect = None

    r = {'name': data[0],
         'name_detail': data[1],
         'elevation': int(data[2]),
         'slope': int(data[6]),
         'aspect': aspect,
         'lat': float(data[3]),
         'lon': float(data[4]),
         }
    return r


def _get_profil(conn, numposte, date):
    """
    Get the standard profile (grain shape, depths, thicknesses) for
    a given numposte and date.

    :param conn: connection to the database
    :type conn: psycopg2 connexion
    :param numposte: numposte
    :type numposte: str
    :param date: Date of the observation
    :type date: python datetime object
    :returns: Profiles on the form of a list of lines. Standard profile, RAM profile and Temperature profile.
              Maximum depth is also returned.
              For std profile: topdepth, thickness, grain primary, grain secondary, grain size,
                             hardness_class, lwc_class, density (kg/m3), hardness (daN), lwc (%)
              For RAM profile: topdepth, thickness, value (daN)
              For T profile: depth, value (Celsius degree)
    :rtype: list, list, list, int
    """
    sql = """SELECT hauteur, resist, t_neige, cod_type_grain1, cod_type_grain2, \
             diam_grain, cod_dur_grain, cod_u_neige, masse_vol, teneur_eau, cisaillt_cal, \
             epaisseur_couche_strati, epaisseur_couche_resist \
             FROM donnees_profil_neige \
             WHERE num_poste=\'{numposte}\' AND dat=\'{date}\' \
             ORDER BY hauteur DESC;
             """.format(numposte=numposte, date=date.isoformat(sep=' '))

    with conn.cursor() as cur:
        cur.execute(sql)
        data = cur.fetchall()

    profil_std = []
    profil_ram = []
    profil_t = []
    maxdepth = 0

    for i, line in enumerate(data):
        # Standard profile
        if line[3] is not None:
            topdepth = int(line[0])
            maxdepth = max(topdepth, maxdepth)
            ep = line[11]
            g1 = _correspGrainForm[line[3]]
            g2 = _correspGrainForm[line[4]] if line[4] is not None else _correspGrainForm[line[3]]
            diam = float(line[5]) if line[5] is not None else None
            hardness = _correspHardness[line[6]] if line[6] in _correspHardness else None
            lwc = _correspLwc[line[7]] if line[7] in _correspLwc else None
            density = float(line[8]) if line[8] is not None else None
            cisaillt = float(line[10]) if line[10] is not None else None
            lwc_m = float(line[9]) if line[9] is not None else None

            # ep processing
            # sometimes epaisseur_couche_strati is not defined...
            if ep is None:
                ep = topdepth
                ii = i + 1
                for j in range(ii, len(data)):
                    if data[j][3] is not None:
                        ep = topdepth - int(data[j][0])
                        break
            ep = int(ep)

            profil_std.append([topdepth / 100, ep / 100, g1, g2,
                               diam, hardness, lwc,
                               density, cisaillt, lwc_m]
                              )

        # RAM profile
        if line[1] is not None:
            topdepth = int(line[0])
            maxdepth = max(topdepth, maxdepth)
            ep = line[12]
            ram = float(line[1]) * 9.81  # Convert kgf in N

            # ep processing
            # sometimes epaisseur_couche_resist is not defined...
            if ep is None:
                ep = topdepth
                ii = i + 1
                for j in range(ii, len(data)):
                    if data[j][1] is not None:
                        ep = topdepth - int(data[j][0])
                        break
            ep = int(ep)

            profil_ram.append([topdepth / 100, ep / 100, ram])

        # Temperature profile
        if line[2] is not None:
            depth = int(line[0])
            maxdepth = max(depth, maxdepth)
            t = float(line[2])

            profil_t.append([depth / 100, t])

    return profil_std, profil_ram, profil_t, maxdepth / 100


def _get_metadata_obs(conn, numposte, date):
    """
    Get the metadata associated to profile observation

    :param conn: connection to the database
    :type conn: psycopg2 connexion
    :param numposte: numposte
    :type numposte: str
    :param date: Date of the observation
    :type date: python datetime object
    :returns: Information related to obsrvation
    :rtype: dict
    """
    sql = """SELECT t, ww_profil_neige, hauteur_neige, equivalent_eau, comment_court, comment_long \
             from infos_profil_neige WHERE num_poste='{numposte}' and dat='{date}'
             """.format(numposte=numposte, date=date.isoformat(sep=' '))
    with conn.cursor() as cur:
        cur.execute(sql)
        data = cur.fetchone()

    if data is None:
        return None

    comment = "{}\n{}".format(data[4] if data[4] is not None else '',
                              data[5] if data[5] is not None else '')

    r = {'t': data[0],
         'ww': _correspWWSkyCond[data[1]] if data[1] is not None and data[1] in _correspWWSkyCond else None,
         'totdepth': int(data[2]) / 100 if data[2] is not None else None,
         'lwc': int(data[3]) if data[3] is not None else None,
         'comment': comment,
         }
    return r


def _mf_conn(**kwargs):
    import psycopg2

    # Read from config the database details if not provided in kwargs
    if 'host' not in kwargs:
        config = _utils.get_config()
        if 'io_mf_bdclim' in config:
            c = config['io_mf_bdclim']
            if 'host' in c:
                kwargs['host'] = c['host']
            if 'port' in c:
                kwargs['port'] = c['port']
            if 'user' in c:
                kwargs['user'] = c['user']
            if 'password' in c:
                kwargs['password'] = c['password']
            if 'dbname' in c:
                kwargs['dbname'] = c['dbname']

    # If config not found and nothing provided in kwargs: cannot connect.
    if 'host' not in kwargs:
        logging.critical('io_mf_bdclim: Could not connect to the database. '
                         'Please provide host and creedentials.')
        raise ValueError('Host not known to connect to database.')

    # Connect to the database
    return psycopg2.connect(**kwargs)


_correspStrAspect = {
    "0": 0.0,     # N
    "1": 0.0,     # N
    "2": 22.5,    # NNE
    "3": 22.5,    # NNE
    "4": 45.0,    # NE
    "5": 45.0,    # NE
    "6": 67.5,    # ENE
    "7": 67.5,    # ENE
    "8": 90.0,    # E
    "9": 90.0,    # E
    "10": 90.0,   # E
    "11": 112.5,  # ESE
    "12": 112.5,  # ESE
    "13": 135.0,  # SE
    "14": 135.0,  # SE
    "15": 157.5,  # SSE
    "16": 157.5,  # SSE
    "17": 180.0,  # S
    "18": 180.0,  # S
    "19": 180.0,  # S
    "20": 202.5,  # SSW
    "21": 202.5,  # SSW
    "22": 225.0,  # SW
    "23": 225.0,  # SW
    "24": 225.0,  # SW
    "25": 247.5,  # WSW
    "26": 270.0,  # W
    "27": 270.0,  # W
    "28": 270.0,  # W
    "29": 292.5,  # WNW
    "30": 157.5,  # WNW
    "31": 315.0,  # NW
    "32": 315.0,  # NW
    "33": 337.5,  # NNW
    "34": 337.5,  # NNW
    "35": 0.0,    # N
    "36": 0.0,    # N
    # 96 Crete
    # 97 Fond de vallee
    # 98 Plateau
}

_correspGrainForm = {
    1: 'PP',
    2: 'DF',
    3: 'RG',
    4: 'FC',
    5: 'DH',
    6: 'MF',
    7: 'IF',
    8: 'SH',
    9: 'PPgp',
}

_correspHardness = {
    1: 'F',
    2: '4F',
    3: '1F',
    4: 'P',
    5: 'K',
}

_correspLwc = {
    1: 'D',
    2: 'M',
    3: 'W',
    4: 'V',
    5: 'S',
}

_correspWWSkyCond = {
    0: 'CLR',
    1: 'BKN',
    4: 'X',
    9: 'OVC',
}
