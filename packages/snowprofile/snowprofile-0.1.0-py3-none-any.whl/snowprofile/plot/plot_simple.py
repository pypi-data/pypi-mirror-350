# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from snowprofile.plot import plot_utils


def plot_simple(sp,
                temperature_profiles=[0],
                density_profiles=[0],
                lwc_profiles=[0],
                hardness_profiles=[0],
                **kwargs):
    """
    Quickly plot the data of a :py:class:`snowprofile.snowprofile.SnowProfile` object.

    Once you have a SnowProfile object ``sp``, just do:

    .. code-block:: python

       import matplotlib.pyplot as plt
       from snowprofile.plot import plot_simple
       plot_simple(sp)
       plt.show()

    .. figure:: /images/plot_simple.png
       :align: center

       Example of a simple plot with the example of the profile observed on 2024-12-24 at Col de Porte (France).

    :param sp: SnowProfile object to be plotted
    :type sp: SnowProfile object
    :param temperature_profiles: ``'all'`` to plot all temperature profiles, ``None`` not to plot temperature
                                 or list of indices of the profiles to plot.
    :type temperature_profiles: None, ``'all'`` or list of int
    :param density_profiles: ``'all'`` to plot all density profiles, ``None`` not to plot density
                                 or list of indices of the profiles to plot.
    :type density_profiles: None, ``'all'`` or list of int
    :param lwc_profiles: ``'all'`` to plot all lwc profiles, ``None`` not to plot lwc
                                 or list of indices of the profiles to plot.
    :type lwc_profiles: None, ``'all'`` or list of int
    :param hardness_profiles: ``'all'`` to plot all hardness profiles, ``None`` not to plot hardness
                                 or list of indices of the profiles to plot.
    :type hardness_profiles: None, ``'all'`` or list of int
    :returns: Matplotlib figure

    """

    # Matplotlib figure
    fig, (ax1, ax2) = plt.subplots(nrows=1,
                                   ncols=2,
                                   figsize = (10, 8),
                                   sharey=True,
                                   gridspec_kw={'wspace': 0.2, 'bottom': 0.22, 'top': 0.92})

    if sp.stratigraphy_profile is not None:
        plot_utils.plot_strati_profile(ax2, sp.stratigraphy_profile,
                                       ylabel=None)

    ax1s = [ax1]

    def twinax1():
        ax = ax1.twiny()
        ax1s.append(ax)
        return ax

    # Temperature (blue)
    if len(sp.temperature_profiles) > 0 and temperature_profiles is not None:
        plot_utils.plot_point_profile(ax1, sp.temperature_profiles, 'temperature', temperature_profiles, xlabel = 'Temperature (°C)',
                                      color='b')
        ax1.xaxis.label.set_color('b')
        ax1.set_xlim(-20, 0)

    # Density (green)
    if len(sp.density_profiles) > 0 and density_profiles is not None:
        ax = twinax1()
        plot_utils.plot_vline_profile(ax, sp.density_profiles, 'density', density_profiles, xlabel = 'Density (kg/m3)',
                                      color='g')
        ax.xaxis.label.set_color('g')
        ax.set_xlim(0, 500)

    # LWC (red)
    if len(sp.lwc_profiles) > 0 and lwc_profiles is not None:
        ax = twinax1()
        plot_utils.plot_step_profile(ax, sp.lwc_profiles, 'lwc', lwc_profiles, xlabel = 'Liquid water content (%)',
                                     color='r')
        ax.xaxis.label.set_color('r')
        ax.set_xlim(10, 0)

    # Hardness (brown)
    if len(sp.hardness_profiles) > 0 and hardness_profiles is not None:
        ax = twinax1()
        plot_utils.plot_step_profile(ax, sp.hardness_profiles, 'hardness', hardness_profiles, xlabel = 'Hardness (N)',
                                     color='tab:brown')
        ax.xaxis.label.set_color('tab:brown')
        ax.set_xlim(1200, 0)

    ax1.set_ylabel('Height (m)')

    if len(ax1s) > 2:
        for i, ax in enumerate(ax1s[2:]):
            ax.xaxis.set_ticks_position("bottom")
            ax.xaxis.set_label_position("bottom")
            ax.spines["bottom"].set_position(("axes", -0.1 * (i + 1)))

    return fig
