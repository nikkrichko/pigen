import os
import unittest
from unittest import mock
import pkg_resources

from support import preflight


class PreflightTests(unittest.TestCase):
    def test_missing_env_raises(self):
        with self.assertRaises(EnvironmentError):
            preflight.preflight_check(env_vars=['MISSING'], requirements=[])

    def test_missing_package_raises(self):
        os.environ['OPENAI_API_KEY'] = 'x'
        with mock.patch('pkg_resources.require', side_effect=pkg_resources.DistributionNotFound('demo')):
            with self.assertRaises(ImportError):
                preflight.preflight_check(env_vars=['OPENAI_API_KEY'], requirements=['demo'])

    def test_success(self):
        os.environ['OPENAI_API_KEY'] = 'x'
        with mock.patch('pkg_resources.require', return_value=None) as req:
            result = preflight.preflight_check(env_vars=['OPENAI_API_KEY'], requirements=['demo'])
        self.assertTrue(result)
        req.assert_called_once_with(['demo'])


if __name__ == '__main__':
    unittest.main()
