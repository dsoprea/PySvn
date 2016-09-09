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
        self.assertEqual(actual_answer, diff)

if __name__ == '__main__':
    unittest.main()
