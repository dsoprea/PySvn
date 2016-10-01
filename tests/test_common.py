__author__ = 'tusharmakkar08'

import os
import unittest
import shutil

from tests.resources.expected_output import diff_summary, diff_summary_2, cat
from svn.common import CommonClient, SvnException

# TODO(dustin): We need to refactor this to depend on a test SVN tree that's 
#               stored within the project.


class TestCommonClient(unittest.TestCase):
    """
    For testing svn/common.py
    """

    def setUp(self):
        self.test_svn_url = 'http://svn.apache.org/repos/asf'
        self.test_start_revision = 1760022
        self.test_end_revision = 1760023

    def tearDown(self):
        if os.path.exists('CHANGES'):
            shutil.rmtree('CHANGES')

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
        self.assertTrue(actual_answer == diff_summary or actual_answer == diff_summary_2)

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
                elif diff_key == 'path':
                    self.assertTrue('http://svn.apache.org/repos/asf/sling/trunk/bundles/extensions/models/pom.xml' in
                                    individual_diff[diff_key] or
                                    'http://svn.apache.org/repos/asf/sling/trunk/pom.xml' in individual_diff[diff_key])

    def test_list(self):
        """
        Checking list
        :return:
        """
        actual_answer = CommonClient(self.test_svn_url, 'url').list()
        self.assertEqual(next(actual_answer), 'abdera/')

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
        self.assertEqual(next(actual_answer).author, 'sseifert')

    def test_cat(self):
        """
        Checking cat
        :return:
        """
        actual_answer = CommonClient(self.test_svn_url, 'url').cat('abdera/abdera2/README', revision=1761404)
        self.assertEqual(cat, actual_answer.decode())

    def test_export(self):
        """
        Checking export
        :return:
        """
        CommonClient('http://svn.apache.org/repos/asf/tcl/websh/trunk/', 'url').export(to_path='CHANGES',
                                                                                       revision=1761404)
        self.assertTrue(os.path.exists('CHANGES'))

    def test_force_export(self):
        """
        Checking export with force option
        :return:
        """
        CommonClient('http://svn.apache.org/repos/asf/tcl/websh/trunk/', 'url').export(to_path='CHANGES',
                                                                                       revision=1761404)
        self.assertTrue(os.path.exists('CHANGES'))
        with self.assertRaises(SvnException):
            CommonClient('http://svn.apache.org/repos/asf/tcl/websh/trunk/', 'url').export(to_path='CHANGES',
                                                                                           revision=1761404)
        try:
            CommonClient('http://svn.apache.org/repos/asf/tcl/websh/trunk/', 'url').export(to_path='CHANGES',
                                                                                           revision=1761404,
                                                                                           force=True)
        except SvnException:
            self.fail("Svn Exception raised with Force also")

if __name__ == '__main__':
    unittest.main()
