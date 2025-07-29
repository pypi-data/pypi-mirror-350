# -*- coding: utf-8 -*-

import logging

import matplotlib.pyplot as plt

from snowprofile.plot import plot_utils


def plot_full(sp,
              index_temperature_profiles = 'all',
              index_density_profiles = 'all', style_density_profiles = 'step',
              index_hardness_profiles = 'all', style_hardness_profiles = 'step',
              index_impurity_profiles = 'all', style_impurity_profiles = 'point',
              index_ssa_profiles = 'all', style_ssa_profiles = 'point',
              index_strength_profiles = 'all', style_strength_profiles = 'point',
              index_lwc_profiles = 'all', style_lwc_profiles = 'step',
              index_scalar_profiles = 'all',
              **kwargs):

    """
    Plot the data (only the vertical property profiles) of a :py:class:`snowprofile.snowprofile.SnowProfile` object.

    Once you have a SnowProfile object ``sp``, just do:

    .. code-block:: python

       import matplotlib.pyplot as plt
       from snowprofile.plot import plot_full
       plot_full(sp)
       plt.show()

    .. figure:: /images/plot_full.png
       :align: center

    **Style** : to be chosen for nearly all variables : may be ``'point'`` to plot with markers or
    ``'step'`` to do a step plot (only possible when thickness is correctly provided).

    **Index**: Except for stratigraphy, several profiles of each variables can be stored in SnowProfile object.
    You can select the profiles to plot by passing a list of indices or use the default value ``'all'`` to
    plot all available profiles.

    :param sp: SnowProfile object to be plotted
    :type sp: SnowProfile object
    :param index_temperature_profiles: index of the temperature profile to be plotted
    :type index_temperature_profiles: list of int

    :type index_hardness_profiles: list of int
    :param style_hardness_profiles: plotting style for hardness profiles
    :type style_hardness_profiles: str
    :type index_impurity_profiles: list of int
    :param style_impurity_profiles: plotting style for impurity profiles
    :type style_impurity_profiles: str
    :param index_ssa_profiles: index of the ssa profile to be plotted
    :type index_ssa_profiles: list of int
    :param style_ssa_profiles: plotting style for SSA profiles
    :type style_ssa_profiles: str
    :param index_strength_profiles: index of the strength profile to be plotted
    :type index_strength_profiles: list of int
    :param style_strength_profiles: plotting style for strength profiles
    :type style_strength_profiles: str
    :param index_lwc_profiles: index of the lwc profile to be plotted
    :type index_lwc_profiles: list of int
    :param style_lwc_profiles: plotting style for LWC profiles
    :type style_lwc_profiles: str
    :type index_scalar_profiles: list of int
    :param index_density_profiles: index of the density profile to be plotted
    :type index_density_profiles: list of int
    :param style_density_profiles: plotting style for density profiles
    :type style_density_profiles: str
    :returns: Matplotlib figure

    """

    to_plot = {
        'Stratigraphy profile': {
            'plot_style': 'profile',
            'key': 'hardness',
            'xlabel': 'Hand Hardness',
            'data': sp.stratigraphy_profile,
            'index': None},
        'Hardness profile': {
            'plot_style': style_hardness_profiles,
            'key': 'hardness',
            'xlabel': 'Hardness (N)',
            'data': sp.hardness_profiles,
            'index': index_hardness_profiles},
        'Temperature profile': {
            'plot_style': 'point',
            'key': 'temperature',
            'xlabel': 'Temperature (°C)',
            'data': sp.temperature_profiles,
            'index': index_temperature_profiles},
        'Density profile': {
            'plot_style': style_density_profiles,
            'key': 'density',
            'xlabel': 'Density (kg/m3)',
            'data': sp.density_profiles,
            'index': index_density_profiles},
        'LWC': {
            'plot_style': style_lwc_profiles,
            'key': 'lwc',
            'xlabel': 'LWC (%)',
            'data': sp.lwc_profiles,
            'index': index_lwc_profiles},
        'Strength profile': {
            'plot_style': style_strength_profiles,
            'key': 'strength',
            'xlabel': 'Strength (N)',
            'data': sp.strength_profiles,
            'index': index_strength_profiles},
        'SSA profile': {
            'plot_style': style_ssa_profiles,
            'key': 'ssa',
            'xlabel': 'SSA (m2/kg)',
            'data': sp.ssa_profiles,
            'index': index_ssa_profiles},
        'Impurity profile': {
            'plot_style': style_impurity_profiles,
            'key': 'mass_fraction',
            'xlabel': 'Impurity mass fraction',
            'data': sp.impurity_profiles,
            'index': index_impurity_profiles},
        'Other scalar profile': {
            'plot_style': 'point',
            'key': 'data',
            'xlabel': 'Other scalar variable',
            'data': sp.other_scalar_profiles,
            'index': index_scalar_profiles}, }

    step_profiles_key_list = ['hardness']

    n_to_plot = 0
    for p, v in to_plot.items():
        if v['data'] is not None and (not isinstance(v['data'], list)
                                      or (len(v['data']) > 0
                                      and v['index'] is not None)):
            v['ok'] = True
            n_to_plot += 1
        else:
            v['ok'] = False

    # Matplotlib figure
    fig, axs = plt.subplots(nrows=(n_to_plot - 1) // 4 + 1,
                            ncols=min(n_to_plot, 4),
                            figsize = (16, 15),
                            sharey=True,
                            gridspec_kw={'wspace': 0.4})
    axes = sum([list(a) for a in axs], [])

    n_subplots = 0
    for p, v in to_plot.items():
        if not v['ok']:
            continue

        common_kwargs = {
            'ylabel': 'Height (m)' if n_subplots % 4 == 0 else None}
        if v['plot_style'] == 'profile':
            plot_utils.plot_strati_profile(
                axes[n_subplots], v['data'], xlabel = v['xlabel'],
                **common_kwargs, **kwargs)
        elif v['plot_style'] == 'point':
            plot_utils.plot_point_profile(
                axes[n_subplots], v['data'], v['key'], v['index'], xlabel = v['xlabel'],
                **common_kwargs, **kwargs)
        elif v['plot_style'] == 'step':
            if v['key'] in step_profiles_key_list:
                plot_utils.plot_step_profile(
                    axes[n_subplots], v['data'], v['key'], v['index'], xlabel = v['xlabel'],
                    **common_kwargs, **kwargs)
            else:
                plot_utils.plot_vline_profile(
                    axes[n_subplots], v['data'], v['key'], v['index'], xlabel = v['xlabel'],
                    **common_kwargs, **kwargs)
        else:
            logging.error(f"Unknown style {v['plot_style']}. Should be either point or step.")
        n_subplots += 1

    return fig
