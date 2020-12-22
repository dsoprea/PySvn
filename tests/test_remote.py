import glob
import os
import shutil
import unittest

import svn.constants
import svn.exception
import svn.remote
import svn.test_support


class TestRemoteClient(unittest.TestCase):
    """
    For testing svn/remote.py
    """

    def shortDescription(self):
        return None

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
        Testing checkout of incorrect URL
        :return:
        """
        try:
            svn.remote.RemoteClient(self.test_fake_url).checkout('.')
        except svn.exception.SvnException:
            pass
        else:
            raise Exception("Expected exception for bad URL.")

    def test_checkout(self):
        """
        Testing checkout
        :return:
        """
        svn.remote.RemoteClient(self.test_svn_url).checkout('trial')
        self.assertTrue(os.path.exists('trial'))

    def test_error_checkout_depth(self):
        """
        Testing checkout with incorrect argument for option depth
        :return:
        """
        repo = "trial_checkout_opt_err"
        try:
            svn.remote.RemoteClient(self.test_svn_url).checkout(repo, depth="toto")
        except svn.exception.SvnException:
            self.assertFalse(os.path.exists(repo))
        else:
            if os.path.exists(repo):
                shutil.rmtree(repo)
            raise Exception("Expected exception for bad URL.")

    def test_checkout_options(self):
        """
        Testing options of checkout
        :return:
        """
        repo = "trial_checkout_opt"
        rc = svn.remote.RemoteClient(self.test_svn_url)

        rc.checkout(repo, force=True)
        self.assertTrue(os.path.exists(repo))
        shutil.rmtree(repo)

        rc.checkout(repo, depth="empty")
        self.assertTrue(os.path.exists(repo))
        self.assertListEqual(glob.glob(repo + "/*.*"), [])
        shutil.rmtree(repo)

        rc.checkout(repo, ignore_ext=True)
        self.assertTrue(os.path.exists(repo))
        shutil.rmtree(repo)

    def test_remove(self):
        """
        Testing remove
        :return:
        """
        with svn.test_support.temp_repo() as (_, rc):
            with svn.test_support.temp_checkout():
                svn.test_support.populate_bigger_file_changes1()

            current_entries = rc.list()
            current_entries = list(current_entries)

            self.assertIn('new_file', current_entries)

            # Confirm it's there.

            current_entries = rc.list()
            current_entries = list(current_entries)

            self.assertIn('new_file', current_entries)

            # Remove.

            rc.remove('new_file', "Remove file.")

            # Confirm that it's gone.

            current_entries = rc.list()
            current_entries = list(current_entries)

            self.assertNotIn('new_file', current_entries)
