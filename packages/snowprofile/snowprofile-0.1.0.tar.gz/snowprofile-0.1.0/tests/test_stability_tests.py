#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from pydantic_core._pydantic_core import ValidationError

import snowprofile


class BaseTestStability:
    result = {}
    additional_keys = {}
    additional_keys_layer = {}

    def test_init_stab(self):
        """
        Check correct instantiation of the class with minimal data
        """
        st = self.CLASS(**self.additional_keys)
        assert st.id is None

    def test_init_stab_result(self):
        """
        Check initialization with a test result
        """
        st_r = self.CLASS_result(**self.result, **self.additional_keys_layer)
        st = self.CLASS(results = [st_r], **self.additional_keys)
        assert st.id is None

    def test_init_stab_result2(self):
        """
        Check adding a second test result
        """
        st_r = self.CLASS_result(**self.result, **self.additional_keys_layer)
        st_r2 = self.CLASS_result(**self.result2, **self.additional_keys_layer)
        st = self.CLASS(results = [st_r], **self.additional_keys)
        st.results.append(st_r2)
        assert len(st.results) == 2


class TestRBStabilityTest(unittest.TestCase, BaseTestStability):
    CLASS = snowprofile.stability_tests.RBStabilityTest
    CLASS_result = snowprofile.stability_tests.RBStabilityTestResult
    result = {'test_score': 2}
    result2 = {'test_score': 5, 'grain_1': 'PP', 'fracture_character': 'SP', 'release_type': 'WB'}
    additional_keys_layer = {'height': 0.21}


class TestCTStabilityTest(unittest.TestCase, BaseTestStability):
    CLASS = snowprofile.stability_tests.CTStabilityTest
    CLASS_result = snowprofile.stability_tests.CTStabilityTestResult
    result = {'test_score': 21}
    result2 = {'test_score': 29, 'grain_1': 'DF', 'fracture_character': 'BRK'}
    additional_keys_layer = {'height': 0.21}


class TestECTStabilityTest(unittest.TestCase, BaseTestStability):
    CLASS = snowprofile.stability_tests.ECTStabilityTest
    CLASS_result = snowprofile.stability_tests.ECTStabilityTestResult
    result = {'test_score': 21}
    result2 = {'test_score': 29, 'grain_1': 'PP', 'propagation': True}
    additional_keys_layer = {'height': 0.21}


class TestShearFrameStabilityTest(unittest.TestCase, BaseTestStability):
    CLASS = snowprofile.stability_tests.ShearFrameStabilityTest
    CLASS_result = snowprofile.stability_tests.ShearFrameStabilityTestResult
    result = {'force': 4}
    result2 = {'force': 8, 'grain_1': 'PP', 'fracture_character': 'SP'}
    additional_keys_layer = {'height': 0.21}


class TestPSTStabilityTest(unittest.TestCase):
    def test_init_stab(self):
        st = snowprofile.stability_tests.PSTStabilityTest(cut_length=0.12, propagation='End')
        assert st.id is None
        st = snowprofile.stability_tests.PSTStabilityTest(cut_length=0.12, column_length=2., propagation='Arr',
                                                          height=0.23, grain_1 = 'SH')
        assert st.id is None


if __name__ == "__main__":
    unittest.main()
