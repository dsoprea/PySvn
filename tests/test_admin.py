__author__ = 'dsoprea'

import unittest
import tempfile
import shutil

import svn.admin


class TestAdmin(unittest.TestCase):
    """
    For testing svn/admin.py
    """

    def test_create_repository(self):
        """
        Testing repository creation.
        :return:
        """

        temp_path = tempfile.mkdtemp()
        shutil.rmtree(temp_path)

        a = svn.admin.Admin()

        try:
            a.create(temp_path)
        finally:
            try:
                shutil.rmtree(temp_path)
            except:
                pass
