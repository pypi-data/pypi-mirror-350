#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import datetime

import snowprofile.io.mf_bdclim

try:
    from snowprofile.io.mf_bdclim import _mf_conn
    _c = _mf_conn(connect_timeout=1)
    _c.close()
    SKIP = False
except Exception:
    SKIP = True


class TestIOMFBdClim(unittest.TestCase):

    @unittest.skipIf(SKIP, 'Database not available')
    def test_search_mf_bdclim_dates(self):
        l_dates = snowprofile.io.mf_bdclim.search_mf_bdclim_dates('38472401', '2023', '2024')
        assert len(l_dates) > 0
        last_year = str(datetime.datetime.now().year - 1)
        l_dates = snowprofile.io.mf_bdclim.search_mf_bdclim_dates('38472401', last_year)

    @unittest.skipIf(SKIP, 'Database not available')
    def test_read_mf_bdclim(self):
        x = snowprofile.io.mf_bdclim.read_mf_bdclim('38472401', date=datetime.datetime(2024, 12, 18, 10, 30))
        assert x.profile_depth == 0.37
        assert x.weather.air_temperature == 12.8
        assert len(x.stratigraphy_profile.data) == 6

        # case of non-existing observation
        try:
            x = snowprofile.io.mf_bdclim.read_mf_bdclim('38472401', date=datetime.datetime(2024, 12, 18, 10, 0))
        except ValueError as e:
            assert str(e) == 'Could not find data at date 2024-12-18 10:00:00'


if __name__ == "__main__":
    unittest.main()
