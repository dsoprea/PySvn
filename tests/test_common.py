__author__ = 'tusharmakkar08'

import unittest

from resources.expected_output import diff_summary, diff
from svn.common import CommonClient


class TestCommonClient(unittest.TestCase):
    """
    For testing svn/common.py
    """

    def setUp(self):
        self.test_svn_url = 'http://svn.apache.org/repos/asf'
        self.test_start_revision = 1760022
        self.test_end_revision = 1760023

    def test_error_client_formation(self):
        """
        Testing Value error while client formation
        :return:
        """
        with self.assertRaises(ValueError):
            CommonClient(self.test_svn_url, 'random')

    def test_diff_summary(self):
        """
        Checking diff summary
        :return:
        """
        actual_answer = CommonClient(self.test_svn_url, 'url').diff_summary(self.test_start_revision,
                                                                            self.test_end_revision)
        self.assertEqual(actual_answer, diff_summary)

    def test_diff(self):
        """
        Checking diff
        :return:
        """
        actual_answer = CommonClient(self.test_svn_url, 'url').diff(self.test_start_revision, self.test_end_revision)
        for index, individual_diff in enumerate(actual_answer):
            for diff_key in individual_diff:
                if diff_key == 'diff':
                    self.assertTrue('sling/trunk/bundles/extensions/models/pom.xml' in
                                    individual_diff[diff_key] or 'sling/trunk/pom.xml' in individual_diff[diff_key])
                    self.assertTrue('<module>bundles/extensions/models</module>' in individual_diff[diff_key] or
                                    '<description>Apache Sling Models</description>' in individual_diff[diff_key])
                else:
                    self.assertEqual(individual_diff[diff_key], diff[index][diff_key])

if __name__ == '__main__':
    unittest.main()
