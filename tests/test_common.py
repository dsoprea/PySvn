__author__ = 'tusharmakkar08'

import os
import unittest

from resources.expected_output import diff_summary, diff, cat
from svn.common import CommonClient, SvnException


class TestCommonClient(unittest.TestCase):
    """
    For testing svn/common.py
    """

    def setUp(self):
        self.test_svn_url = 'http://svn.apache.org/repos/asf'
        self.test_start_revision = 1760022
        self.test_end_revision = 1760023

    def tearDown(self):
        if os.path.exists('README'):
            os.remove('README')

    def test_error_client_formation(self):
        """
        Testing SvnException error while client formation
        :return:
        """
        with self.assertRaises(SvnException):
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

    def test_list(self):
        """
        Checking list
        :return:
        """
        actual_answer = CommonClient(self.test_svn_url, 'url').list()
        self.assertEqual(actual_answer.next(), 'abdera/')

    def test_info(self):
        """
        Checking info
        :return:
        """
        actual_answer = CommonClient(self.test_svn_url, 'url').info()
        self.assertEqual(actual_answer['entry_path'], 'asf')
        self.assertEqual(actual_answer['repository_root'], 'http://svn.apache.org/repos/asf')
        self.assertEqual(actual_answer['entry#kind'], 'dir')
        self.assertEqual(actual_answer['repository/uuid'], '13f79535-47bb-0310-9956-ffa450edef68')

    def test_log(self):
        """
        Checking log
        :return:
        """
        actual_answer = CommonClient(self.test_svn_url, 'url').log_default(revision_from=1761404, revision_to=1761403)
        self.assertEqual(actual_answer.next().author, 'sseifert')

    def test_cat(self):
        """
        Checking cat
        :return:
        """
        actual_answer = CommonClient(self.test_svn_url, 'url').cat('abdera/abdera2/README', revision=1761404)
        self.assertEqual(cat, actual_answer)

    def test_export(self):
        """
        Checking export
        :return:
        """
        CommonClient(self.test_svn_url+'/abdera/abdera2/README', 'url').export(to_path='', revision=1761404)
        self.assertTrue(os.path.exists('README'))

if __name__ == '__main__':
    unittest.main()
