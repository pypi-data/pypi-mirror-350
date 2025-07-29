# -*- coding: utf-8 -*-

import os
import os.path
import unittest

import pandas as pd

import snowprofile


_here = os.path.dirname(os.path.realpath(__file__))


class TestIOCsvProfile(unittest.TestCase):

    def test_read_density_profile(self):
        path_density = os.path.join(_here, "resources", "densitydata_20240420.txt")
        density_mapper = dict(
            top_height = dict(
                column = "Heigth[cm]",
                scale_factor = 0.01),
            thickness = dict(
                value = 0.025
            ),
            density = dict(
                column = "Density[kg/m3]",
                scale_factor = 1)
        )
        sp = snowprofile.io.read_csv_profile(path_density, sep="\t", skiprows=8, mapper=density_mapper,
                                             profile_class="DensityProfile")
        assert(len(sp.density_profiles) == 1)
        expected_density = pd.Series(
            [113.68, 137.12, 177.08, 130.0, 286.24, 273.36, 302.44, 291.92, 309.04, 333.48, 223.04])
        assert sp.density_profiles[0].data["density"].equals(expected_density)

    def test_read_scalar_profile(self):
        path_scalar = os.path.join(_here, "resources", "medianDerivatives.csv")
        scalar_point_mapper = dict(
            top_height = dict(
                column = "corrected height [mm]",
                scale_factor = 0.001),
            thickness = dict(
                value = 0.005
            ),
            data = dict(
                column = "L2012_lambda [1/mm]", scale_factor = 1000
            ),
            uncertainty = dict(
                value = 0.005  # Arbitrary value
            ),
            quality = dict(
                value = "Good"
            )
        )
        sp = snowprofile.io.read_csv_profile(
            path_scalar,
            sep=",",
            skiprows=0,
            mapper=scalar_point_mapper,
            profile_class="ScalarProfile",
            metadata= dict(
                parameter = "L2012_lambda",
                unit = "1/m",
                method_of_measurement = "Unknown"
            )
        )
        assert len(sp.other_scalar_profiles) == 1
        assert sp.other_scalar_profiles[0].data.loc[:10, "data"].equals(
            pd.Series(
                [21042069.4, 311975.5, 238303.5, 1511739.5, 281864.0,
                 569550.1000000001, 726504.5, 1265936.3, 334452.7, 367673.80000000005, 332738.5]))
        assert sp.other_scalar_profiles[0].parameter == "L2012_lambda"
        assert sp.other_scalar_profiles[0].unit == "1/m"
