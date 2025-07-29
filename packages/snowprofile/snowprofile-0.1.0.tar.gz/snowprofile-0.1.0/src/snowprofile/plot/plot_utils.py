# -*- coding: utf-8 -*-

import logging
import os.path

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from snowprofile.plot import plot_dictionnaries

__all__ = ['plot_vline_profile', 'plot_step_profile', 'plot_point_profile', 'plot_strati_profile']


def plot_vline_profile(ax, variable_profiles, name_profile, index_profiles,
                       xlabel = 'Variable (unit)', ylabel = 'Height (m)',
                       color = None,
                       **kwargs):
    """
    Function to plot a set of profiles on an axis.

    .. figure:: /images/plot_vline_profile.png
       :align: center

    """
    colors = iter(plt.cm.tab10(np.linspace(0, 1, 10)))

    if index_profiles == 'all':
        index_profiles = range(len(variable_profiles))

    for i in index_profiles:
        data = variable_profiles[i].data_dict

        if name_profile not in data:
            logging.error(f'Data from key {name_profile} not found.')
            continue

        if color is None:
            c = next(colors)
        else:
            c = color

        if 'top_height' in data and 'bottom_height' in data:
            ax.vlines(x = data[name_profile],
                      ymin = data['bottom_height'],
                      ymax = data['top_height'],
                      label = str(i), color = c, **kwargs)
        elif 'height' in data:
            height = data['height']
            ax.plot(data[name_profile], height,
                    label = str(i), ls = ':', marker='o', **kwargs)

    ax.set_xlabel(xlabel)
    ax.grid(ls=':')
    if ylabel is not None:
        ax.set_ylabel(ylabel)


def plot_step_profile(ax, variable_profiles, name_profile, index_profiles,
                      xlabel = 'Variable (unit)', ylabel = 'Height (m)',
                      color = None,
                      **kwargs):
    """
    Function to plot a set of profiles on an axis.

    .. figure:: /images/plot_step_profile.png
       :align: center

    """
    colors = iter(plt.cm.tab10(np.linspace(0, 1, 10)))

    if index_profiles == 'all':
        index_profiles = range(len(variable_profiles))

    for i in index_profiles:
        data = variable_profiles[i].data_dict

        if name_profile not in data:
            logging.error(f'Data from key {name_profile} not found.')
            continue

        if color is None:
            c = next(colors)
        else:
            c = color

        if 'top_height' in data and 'bottom_height' in data:
            ax.step(x = data[name_profile],
                    y = data['top_height'],
                    label = str(i), color = c, **kwargs)
            ax.vlines(x = data[name_profile][-1],
                      ymax = data['top_height'][-1],
                      ymin = data['bottom_height'][-1], color = c, **kwargs)
        elif 'height' in data:
            logging.error('A step plot was not possible as no tickness is associated to the data.')
            height = data['height']
            ax.plot(data[name_profile], height,
                    label = str(i), ls = ':', marker='o', **kwargs)

    ax.set_xlabel(xlabel)
    ax.grid(ls=':')
    if ylabel is not None:
        ax.set_ylabel(ylabel)


def plot_point_profile(ax, variable_profiles, name_profile, index_profiles,
                       xlabel = 'Variable (unit)', ylabel = 'Height (m)',
                       color = None,
                       **kwargs):
    """
    Function to plot a set of profiles on an axis.

    .. figure:: /images/plot_point_profile.png
       :align: center

    """
    colors = iter(plt.cm.tab10(np.linspace(0, 1, 10)))

    if index_profiles == 'all':
        index_profiles = range(len(variable_profiles))

    for i in index_profiles:
        data = variable_profiles[i].data_dict

        if name_profile not in data:
            logging.error(f'Data from key {name_profile} not found.')
            continue

        if color is None:
            c = next(colors)
        else:
            c = color

        if 'top_height' in data and 'thickness' in data:
            height = np.array(data['top_height']) - np.array(data['thickness']) / 2
        elif 'height' in data:
            height = data['height']
        else:
            logging.error('Either height or top_height/thickness should be provided')
            continue
        ax.plot(variable_profiles[i].data_dict[name_profile], height,
                label = str(i), ls = ':', marker='o', color=c, **kwargs)

    ax.set_xlabel(xlabel)
    ax.grid(ls=':')
    if ylabel is not None:
        ax.set_ylabel(ylabel)


def plot_strati_profile(ax, stratigraphy, xlabel = 'Hand harness', ylabel = 'Height (m)',
                        grain_labels=True, use_hardness=True, **kwargs):
    """
    Plot stratigraphy- (layers, colored according to grains, with grain symbol
    and with the hand-hardness)

    .. figure:: /images/plot_strati_profile.png
       :align: center


    :param ax: Matplotlib axis to plot on
    :type ax: Matplotlib axis
    :param stratigraphy: SnowProfile stratigraphy element to plot
    :type stratigraphy: :py:class:`snowprofile.classes.Stratigraphy`
    :param xlabel: The x-axis label
    :type xlabel: str
    :param ylabel: The y-ayis label
    :type ylabel: str
    :param grain_labels: Whether or not to plot the grain labels
    :type grain_labels: bool
    :param use_hardness: Whether or not to use the hand hardness

    """

    _here = os.path.dirname(os.path.realpath(__file__))
    snowiacs = os.path.join(_here, './SnowSymbolsIACS.ttf')
    if not os.path.isfile(snowiacs):
        snowiacs = matplotlib.font_manager.findfont('SnowSymbolsIACS')
    snowsymb = matplotlib.font_manager.FontProperties(fname=snowiacs)

    # get data
    data = stratigraphy.data_dict
    height = data['top_height']
    height.append(data['bottom_height'][-1])

    if use_hardness:
        hardness = data['hardness']
    else:
        hardness = [1] * (len(height) - 1)
    grain1 = data['grain_1']
    grain2 = data['grain_2']

    for i in range(len(grain1)):
        c = plot_dictionnaries.get_grain_color(grain1[i])
        width = plot_dictionnaries.get_hardness_value(hardness[i])  # width of the rectangle
        delta_h = height[i] - height[i + 1]  # height of the rectangle

        ax.add_patch(Rectangle((0., height[i + 1]), width, delta_h, color = c))

        ax.hlines(y=height[i + 1], xmin=0, xmax=width, linewidth=1, color='k')
        ax.hlines(y=height[i], xmin=0, xmax=width, linewidth=1, color='k')

        if grain_labels:
            text = plot_dictionnaries.get_grain_text(grain1[i]) + plot_dictionnaries.get_grain_text(grain2[i])
            ax.text(width / 2, height[i + 1] + delta_h / 2, text,
                    horizontalalignment='center', verticalalignment='center',
                    fontproperties=snowsymb, fontsize=12, color='k', fontweight='bold')

    ax.set_xlim(xmax=6)
    ax.set_xlabel(xlabel)
    ax.grid(ls=':')
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if use_hardness:
        tick_hardness_str = list(plot_dictionnaries.hardness_str_values.keys())
        tick_hardness_nb = list(plot_dictionnaries.hardness_str_values.values())
        ax.set_xticks(tick_hardness_nb)  # Set the tick positions
        ax.set_xticklabels(tick_hardness_str)  # Set the tick labels
