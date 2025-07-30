#!/usr/bin/env python

"""
Purpose: unit and integration tests
"""

import unittest

from click.testing import CliRunner

from pkg_15903.run import main


class TestMain(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    ''' assert zero exit code with url success '''
    def test_main_url_option_success(self):
        result = self.runner.invoke(main, ['--url', 'https://google.com'])
        self.assertEqual(result.exit_code, 0)

    ''' assert non-zero exit code with url failure '''
    def test_main_url_option_failure(self):
        result = self.runner.invoke(main, ['--url', 'hello'])
        self.assertNotEqual(result.exit_code, 0)

    ''' assert non-zero exit code with url failure '''
    def test_main_url_option_missing_success(self):
        result = self.runner.invoke(main, ['--hello', 'False'])
        # print(result.stdout)
        self.assertNotEqual(result.exit_code, 0)

    ''' assert non-zero exit code with bad url failure '''
    def test_main_url_option_bad_url_success(self):
        result = self.runner.invoke(main, ['--url', 'https://iamnotarobotdotcom.ai'])
        self.assertNotEqual(result.exit_code, 0)

    ''' assert zero exit code without url option success '''
    def test_main_url_option_none_success(self):
        result = self.runner.invoke(main)
        self.assertEqual(result.exit_code, 0)
