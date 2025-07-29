#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import unittest
import tempfile

import snowprofile

_here = os.path.dirname(os.path.realpath(__file__))


def gen_snowprofile():
    sp = snowprofile.SnowProfile()
    sp.location.name = 'Col de Porte'
    sp.location.latitude = 45.295043
    sp.location.longitude = 5.76559
    import datetime
    sp.time.record_time = datetime.datetime(2019, 12, 25, 10, 0)
    sp.time.report_time = datetime.datetime.now()

    dp = snowprofile.profiles.DensityProfile(
        method_of_measurement="Snow Cutter",
        quality_of_measurement="Good",
        probed_thickness=0.03,  # 3cm cutter thickness
        data = {'top_height': [1.2, 1.1, 1.0, 0.50],
                'thickness': [0.1, 0.1, 0.5, 0.5],
                'density': [75, 100, 180, 230]}
    )
    sp.density_profiles.append(dp)
    return sp


class TestIOInternalJSON(unittest.TestCase):

    def test_to_from_snowprofile(self):
        sp = gen_snowprofile()

        json = snowprofile.io.to_json(sp)
        spn = snowprofile.io.from_json(json)

        assert spn.location.name == sp.location.name, 'Names differ'
        assert spn.time.record_time == sp.time.record_time, 'Time differs'
        assert sp.density_profiles[0].data.equals(spn.density_profiles[0].data), 'Density profiles differ'

    def test_write_read_internal_json(self):
        sp = gen_snowprofile()

        fd = tempfile.mkstemp(prefix='snowprofile-tests', suffix='.json')
        fn = snowprofile.io.write_internal_json(sp, fd[1])
        spn = snowprofile.io.read_internal_json(fn)

        assert spn.location.name == sp.location.name, f'Names differ, see {fn}'
        assert spn.time.record_time == sp.time.record_time, f'Time differs, see {fn}'
        assert sp.density_profiles[0].data.equals(spn.density_profiles[0].data), f'Density profiles differ, see {fn}'

        os.remove(fn)

    def test_to_from_real_data(self):
        sp = snowprofile.io.read_caaml6_xml(os.path.join(_here, 'resources', 'SnowProfile_IACS_SLF22950.xml'))
        json = snowprofile.io.to_json(sp)
        spn = snowprofile.io.from_json(json)

        assert len(sp.stability_tests) == len(spn.stability_tests)
        for i in range(len(sp.stability_tests)):
            assert isinstance(spn.stability_tests[i], type(sp.stability_tests[i]))


if __name__ == "__main__":
    unittest.main()
