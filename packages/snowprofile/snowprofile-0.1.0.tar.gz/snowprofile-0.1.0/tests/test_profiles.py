#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import datetime

from pydantic_core._pydantic_core import ValidationError
import numpy as np

import snowprofile


class BaseTestProfiles:
    values = [100, 75]
    additional_keys = {}

    def test_init_profile(self):
        """
        Check correct instantiation of the class with minimal data
        """
        sp_pd = self.CLASS(data={'top_height': [1, 2],
                                 'thickness': [1, 1],
                                 self.key: self.values, },
                           **self.additional_keys)
        assert sp_pd.id is None

    def test_edit_values(self):
        sp_pd = self.CLASS(data={'top_height': [1, 2],
                                 'thickness': [1, 1],
                                 self.key: self.values, },
                           **self.additional_keys)
        data = sp_pd.data
        data.loc[data.index[1], 'top_height'] += 1

        # check that at this stage values are unchanged and correctly sorted
        assert (sp_pd.data['top_height'].values == np.array([2, 1])).all()

        # Update with inconsistencies
        try:
            sp_pd.data = data
            assert False, 'Inconsistent data should rise an error'
        except ValueError:
            pass

        # Do a correct update
        data.loc[data.index[1], 'thickness'] += 1
        sp_pd.data = data
        # Check correctly updated
        assert (sp_pd.data['top_height'].values == np.array([2, 2])).all()

    def test_init_profile_fail(self):
        """
        check there is a fail if minimal data is not present
        """
        self.assertRaises(
            ValueError,
            self.CLASS, data={'top_height': [1, 2],
                              self.key: self.values, },
            **self.additional_keys
        )

    def test_init_profile_quality_uncertainty_layer(self):
        """
        Check the possibility to add quality and uncertainty flags
        """
        sp_pd = self.CLASS(data={'top_height': [1, 2],
                                 'thickness': [1, 1],
                                 self.key: self.values,
                                 'quality': ['Good', 'Uncertain'],
                                 'uncertainty': [10, 60], },
                           **self.additional_keys)
        assert sp_pd.id is None
        assert (sp_pd.data['quality'].loc[sp_pd.data['top_height'] == 1] == 'Good').all()
        assert (sp_pd.data['quality'].loc[sp_pd.data['top_height'] == 2] == 'Uncertain').all()

        try:
            sp_pd = self.CLASS(data={'top_height': [1, 2],
                                     'thickness': [1, 1],
                                     self.key: self.values,
                                     'quality': ['Good', 'Bof'], },
                               **self.additional_keys)
            assert False, 'Should prevent from incorrect quality flags'
        except ValueError:
            pass

    def test_init_profile_quality_uncertainty_profile(self):
        sp_pd = self.CLASS(data={'top_height': [1, 2],
                                 'thickness': [1, 1],
                                 self.key: self.values, },
                           quality_of_measurement="Bad",
                           uncertainty_of_measurement=20,
                           **self.additional_keys)
        assert sp_pd.quality_of_measurement == "Bad"
        assert sp_pd.uncertainty_of_measurement == 20

        sp_pd.quality_of_measurement = 'Good'
        sp_pd.uncertainty_of_measurement = 22
        assert sp_pd.quality_of_measurement == "Good"
        assert sp_pd.uncertainty_of_measurement == 22

        try:
            sp_pd.quality_of_measurement = "Bof bof"
            assert False, 'Should raise an error when an incorrect value is proposed.'
        except ValidationError:
            pass

        try:
            sp_pd.uncertainty_of_measurement = -22
            assert False, 'Should raise an error when an incorrect value is proposed (uncertainty should be >0).'
        except ValidationError:
            pass

    def test_init_profile_with_metadata(self):
        sp_pd = self.CLASS(data={'top_height': [1, 2],
                                 'thickness': [1, 1],
                                 self.key: self.values, },
                           comment=f"My beautiful {self.key} profile",
                           id=f"profile_{self.key}_01",
                           name=f"{self.key} 01",
                           **self.additional_keys)
        sp_pd.record_time = datetime.datetime.now()
        sp_pd.name = f"{self.key} 02"
        assert sp_pd.name == f"{self.key} 02"


class TestDensityProfile(unittest.TestCase, BaseTestProfiles):
    CLASS = snowprofile.profiles.DensityProfile
    key = 'density'


class TestLWCProfile(unittest.TestCase, BaseTestProfiles):
    CLASS = snowprofile.profiles.LWCProfile
    key = 'lwc'


class TestSSAProfile(unittest.TestCase, BaseTestProfiles):
    CLASS = snowprofile.profiles.SSAProfile
    key = 'ssa'


class TestHardnessProfile(unittest.TestCase, BaseTestProfiles):
    CLASS = snowprofile.profiles.HardnessProfile
    key = 'hardness'


class TestStrengthProfile(unittest.TestCase, BaseTestProfiles):
    CLASS = snowprofile.profiles.StrengthProfile
    key = 'strength'


class TestImpurity1Profile(unittest.TestCase, BaseTestProfiles):
    CLASS = snowprofile.profiles.ImpurityProfile
    key = 'volume_fraction'
    additional_keys = {'impurity_type': 'Black Carbon'}


class TestImpurity2Profile(unittest.TestCase, BaseTestProfiles):
    CLASS = snowprofile.profiles.ImpurityProfile
    key = 'mass_fraction'
    additional_keys = {'impurity_type': 'Black Carbon'}


class TestOtherProfile(unittest.TestCase, BaseTestProfiles):
    CLASS = snowprofile.profiles.ScalarProfile
    key = 'data'
    additional_keys = {'unit': 'm', 'parameter': 'A random length in m',
                       'method_of_measurement': '?'}


class TestOtherVectorialProfile(unittest.TestCase, BaseTestProfiles):
    CLASS = snowprofile.profiles.VectorialProfile
    key = 'data'
    additional_keys = {'unit': 'm', 'parameter': 'A random length in m', 'rank': 2,
                       'method_of_measurement': '?'}
    values = [[100, 100], [75, 76]]

    def test_edit_values(self):
        # Edit has to be checked because it raises a warning
        pass


if __name__ == "__main__":
    unittest.main()
