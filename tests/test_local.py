__author__ = 'tusharmakkar08'

import os
import shutil
import unittest

from svn.local import LocalClient


class TestRemoteClient(unittest.TestCase):
    """
    For testing svn/remote.py
    """

    def setUp(self):
        create_svn = "svnadmin create temp_repo"
        os.system(create_svn)
        os.mkdir("temp")
        os.mkdir("check_temp")
        os.chdir("temp")
        with open('trial.txt', 'a'):
            pass
        os.chdir("..")
        make_file = "svn import temp/ file://" + os.getcwd() + "/temp_repo -m 'Initial commit'"
        os.system(make_file)
        os.system("cd check_temp; svn co file://" + os.getcwd() + "/temp_repo; cd temp_repo; "
                  "touch 'new.txt'; svn add 'new.txt'; svn commit -m 'second_commit'")
        self.test_local_url = os.getcwd() + '/temp_repo'
        self.fake_local_url = os.getcwd() + '/tt'

    def tearDown(self):
        shutil.rmtree('temp')
        shutil.rmtree('check_temp')
        shutil.rmtree('temp_repo')

    def test_error_client_formation(self):
        """
        Testing Value error while client formation
        :return:
        """
        with self.assertRaises(EnvironmentError):
            LocalClient(self.fake_local_url)

    def test_normal_flow(self):
        """
        Testing checkout
        :return:
        """
        try:
            LocalClient(self.test_local_url)
        except EnvironmentError:
            self.fail("Issue with Setting up of svn")

if __name__ == '__main__':
    unittest.main()
