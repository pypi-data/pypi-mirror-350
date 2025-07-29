#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import unittest
import tempfile

import matplotlib
matplotlib.use('Agg')

import snowprofile
import snowprofile.plot

_here = os.path.dirname(os.path.realpath(__file__))


class TestIOCAAML6XML(unittest.TestCase):

    def test_plot_default_example(self):
        """
        Test file provided on caaml.org website (SnowProfile_IACS_SLF22950.xml)
        """
        sp = snowprofile.io.read_caaml6_xml(os.path.join(_here, 'resources', 'SnowProfile_IACS_SLF22950.xml'))
        fig_f = snowprofile.plot.plot_full(sp)
        fig_s = snowprofile.plot.plot_simple(sp)
        with tempfile.TemporaryDirectory(prefix='snowprofiletests') as dirname:
            filename = os.path.join(dirname, 'fig.png')
            fig_f.savefig(filename)
            fig_s.savefig(filename)

    def test_plot_example3(self):
        """
        Test Profile 3: a rather complete test snow observation.
        """
        sp = snowprofile.io.read_caaml6_xml(os.path.join(_here, 'resources', 'TestProfile3.caaml'))
        fig = snowprofile.plot.plot_full(sp)
        with tempfile.TemporaryDirectory(prefix='snowprofiletests') as dirname:
            filename = os.path.join(dirname, 'fig.png')
            fig.savefig(filename)


if __name__ == "__main__":
    unittest.main()
