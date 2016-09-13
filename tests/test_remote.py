__author__ = 'tusharmakkar08'

import os
import shutil
import unittest

from svn.remote import RemoteClient
from svn.common import SvnException


class TestRemoteClient(unittest.TestCase):
    """
    For testing svn/remote.py
    """

    def setUp(self):
        self.test_svn_url = 'http://svn.apache.org/repos/asf/ace/trunk/cnf/lib/kxml2'
        self.test_fake_url = 'http://svn_abc.1apache.org1/repos/asf/src'
        self.test_start_revision = 1760022
        self.test_end_revision = 1760023

    def tearDown(self):
        if os.path.exists('trial'):
            shutil.rmtree('trial')

    def test_error_client_formation(self):
        """
        Testing Value error while client formation
        :return:
        """
        with self.assertRaises(SvnException):
            RemoteClient(self.test_fake_url).checkout('.')

    def test_checkout(self):
        """
        Testing checkout
        :return:
        """
        RemoteClient(self.test_svn_url).checkout('trial')
        self.assertTrue(os.path.exists('trial'))

if __name__ == '__main__':
    unittest.main()
