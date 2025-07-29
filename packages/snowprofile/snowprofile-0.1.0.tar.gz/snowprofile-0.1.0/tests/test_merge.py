#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import snowprofile


def gen_snowprofile(offset=0):
    sp = snowprofile.SnowProfile()
    sp.location.name = 'Col de Porte'
    sp.location.latitude = 45.295043
    sp.location.longitude = 5.76559
    import datetime
    sp.time.record_time = datetime.datetime(2019, 12, 25, 10, 0)
    sp.time.report_time = datetime.datetime(2023, 11, 2)

    dp = snowprofile.profiles.DensityProfile(
        method_of_measurement="Snow Cutter",
        quality_of_measurement="Good",
        probed_thickness=0.03,  # 3cm cutter thickness
        data = {'top_height': [1.2 + offset, 1.1 + offset, 1.0 + offset, 0.50],
                'thickness': [0.1, 0.1, 0.5, 0.5],
                'density': [75, 100, 180, 230]}
    )
    sp.density_profiles.append(dp)
    return sp


class TestMerge(unittest.TestCase):

    def test_merge(self):
        sp1 = gen_snowprofile()
        sp1_ref = gen_snowprofile()
        sp2 = gen_snowprofile(offset=1)

        sp1.merge(sp2)

        assert sp1.location.name == sp1_ref.location.name
        assert len(sp1.density_profiles) == len(sp1_ref.density_profiles) + len(sp2.density_profiles)


if __name__ == "__main__":
    unittest.main()
