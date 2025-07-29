#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import unittest
import tempfile

from lxml import etree

import snowprofile

_here = os.path.dirname(os.path.realpath(__file__))


class TestIOCAAML6XML(unittest.TestCase):

    def test_read_caaml6_xml_default_example(self):
        """
        Test file provided on caaml.org website (SnowProfile_IACS_SLF22950.xml)
        """
        sp = snowprofile.io.read_caaml6_xml(os.path.join(_here, 'resources', 'SnowProfile_IACS_SLF22950.xml'))

        assert sp.observer.source_name == 'WSL Insitute for Snow and Avalanche Research SLF'
        assert sp.location.name == 'Chörbschhorn - Hanengretji - Davos'
        assert sp.application == 'SnowProfiler'
        assert sp.weather.cloudiness == 'FEW'
        assert sp.profile_depth == 1.831
        assert len(sp.temperature_profiles) == 1
        assert len(sp.density_profiles) == 1
        assert len(sp.impurity_profiles) == 1
        assert sp.impurity_profiles[0].impurity_type == 'Black Carbon'

    def test_read_write_caaml6_xml_example2(self):
        """
        A rather simple profile, but with diffrent data compated to the basic test file provided on caaml.org website.
        """
        sp = snowprofile.io.read_caaml6_xml(os.path.join(_here, 'resources', 'TestProfile2.caaml'))

        with tempfile.TemporaryDirectory(prefix='snowprofiletests') as dirname:
            filename = os.path.join(dirname, 'testcaaml.caaml')
            snowprofile.io.write_caaml6_xml(sp, filename)

            # Test CAAML6 validity
            xmlschema_path = os.path.join(_here, 'resources', 'CAAMLv6.0.5_SnowProfileIACS.xsd')
            xmlschema_doc = etree.parse(xmlschema_path)
            xmlschema = etree.XMLSchema(xmlschema_doc)

            xml_doc = etree.parse(filename)
            result = xmlschema.validate(xml_doc)
            assert result, f'Invalid CAAML output:\n{xmlschema.error_log}'

            # Re-read
            sp_reread = snowprofile.io.read_caaml6_xml(filename)

        assert snowprofile.io.to_json(sp) == snowprofile.io.to_json(sp_reread)

    def test_write_caaml6_xml_example3_v605(self):
        """
        Test Profile 3: a rather complete test snow observation.
        Write in CAAML 6.0.5 version
        """
        sp = snowprofile.io.read_caaml6_xml(os.path.join(_here, 'resources', 'TestProfile3.caaml'))

        with tempfile.TemporaryDirectory(prefix='snowprofiletests') as dirname:
            filename = os.path.join(dirname, 'testcaaml.caaml')
            snowprofile.io.write_caaml6_xml(sp, filename, version='6.0.5')

            # Test CAAML6 validity
            xmlschema_path = os.path.join(_here, 'resources', 'CAAMLv6.0.5_SnowProfileIACS.xsd')
            xmlschema_doc = etree.parse(xmlschema_path)
            xmlschema = etree.XMLSchema(xmlschema_doc)

            xml_doc = etree.parse(filename)
            result = xmlschema.validate(xml_doc)
            assert result, f'Invalid CAAML output:\n{xmlschema.error_log}'

    def test_read_write_caaml6_xml_example3_v606(self):
        """
        Test Profile 3: a rather complete test snow observation.
        Write in CAAML 6.0.6 version and ensure no data is lost.
        """
        sp = snowprofile.io.read_caaml6_xml(os.path.join(_here, 'resources', 'TestProfile3.caaml'))

        with tempfile.TemporaryDirectory(prefix='snowprofiletests') as dirname:
            filename = os.path.join(dirname, 'testcaaml.caaml')
            snowprofile.io.write_caaml6_xml(sp, filename, version='6.0.6')

            # Test CAAML6 validity
            xmlschema_path = os.path.join(_here, 'resources', 'CAAMLv6.0.6_SnowProfileIACS.xsd')
            xmlschema_doc = etree.parse(xmlschema_path)
            xmlschema = etree.XMLSchema(xmlschema_doc)

            xml_doc = etree.parse(filename)
            result = xmlschema.validate(xml_doc)
            assert result, f'Invalid CAAML output:\n{xmlschema.error_log}'

            # Re-read
            sp_reread = snowprofile.io.read_caaml6_xml(filename)

        assert snowprofile.io.to_json(sp) == snowprofile.io.to_json(sp_reread)

    def test_write_caaml6_xml_example4_v605(self):
        """
        Test Profile 4: A profile with exotic things not present in test 3
        Write in CAAML 6.0.5 version
        """
        sp = snowprofile.io.read_caaml6_xml(os.path.join(_here, 'resources', 'TestProfile3.caaml'))

        with tempfile.TemporaryDirectory(prefix='snowprofiletests') as dirname:
            filename = os.path.join(dirname, 'testcaaml.caaml')
            snowprofile.io.write_caaml6_xml(sp, filename, version='6.0.5')

            # Test CAAML6 validity
            xmlschema_path = os.path.join(_here, 'resources', 'CAAMLv6.0.5_SnowProfileIACS.xsd')
            xmlschema_doc = etree.parse(xmlschema_path)
            xmlschema = etree.XMLSchema(xmlschema_doc)

            xml_doc = etree.parse(filename)
            result = xmlschema.validate(xml_doc)
            assert result, f'Invalid CAAML output:\n{xmlschema.error_log}'

    def test_read_write_caaml6_xml_example4_v606(self):
        """
        Test Profile 4: A profile with exotic things not present in test 3
        Write in CAAML 6.0.6 version and ensure no data is lost.
        """
        sp = snowprofile.io.read_caaml6_xml(os.path.join(_here, 'resources', 'TestProfile4.caaml'))

        with tempfile.TemporaryDirectory(prefix='snowprofiletests') as dirname:
            filename = os.path.join(dirname, 'testcaaml.caaml')
            snowprofile.io.write_caaml6_xml(sp, filename, version='6.0.6')

            # Test CAAML6 validity
            xmlschema_path = os.path.join(_here, 'resources', 'CAAMLv6.0.6_SnowProfileIACS.xsd')
            xmlschema_doc = etree.parse(xmlschema_path)
            xmlschema = etree.XMLSchema(xmlschema_doc)

            xml_doc = etree.parse(filename)
            result = xmlschema.validate(xml_doc)
            assert result, f'Invalid CAAML output:\n{xmlschema.error_log}'

            # Re-read
            sp_reread = snowprofile.io.read_caaml6_xml(filename)

        assert snowprofile.io.to_json(sp) == snowprofile.io.to_json(sp_reread)


if __name__ == "__main__":
    unittest.main()
