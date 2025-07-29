#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import snowprofile


class TestSnowProfile(unittest.TestCase):
    def test_init_void_snowprofile(self):
        sp = snowprofile.SnowProfile()
        assert sp.id is None

    def test_example_snowprofile(self):
        sp = snowprofile.SnowProfile()
        sp.location.name = 'Col de Porte'
        sp.location.latitude = 45.295043
        sp.location.longitude = 5.76559
        import datetime
        sp.time.record_time = datetime.datetime(2019, 12, 25, 10, 0)
        sp.time.report_time = datetime.datetime.now()

    def test_add_profile(self):
        sp = snowprofile.SnowProfile()
        dp = snowprofile.profiles.DensityProfile(
            method_of_measurement="Snow Cutter",
            quality_of_measurement="Good",
            probed_thickness=0.03,  # 3cm cutter thickness
            data = {'top_height': [1.2, 1.1, 1.0, 0.5],
                    'thickness': [0.1, 0.1, 0.5, 0.5],
                    'density': [75, 100, 180, 230]}
        )
        sp.density_profiles.append(dp)


if __name__ == "__main__":
    unittest.main()
