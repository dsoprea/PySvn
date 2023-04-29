__author__ = 'dsoprea'

import unittest
import tempfile
import shutil
import logging

import svn.admin
import svn.remote

_LOGGER = logging.getLogger(__name__)


class TestAdmin(unittest.TestCase):
    """
    For testing svn/admin.py
    """

    def shortDescription(self):
        return None

    def test_create_repository(self):
        """
        Testing repository creation.
        :return:
        """

        temp_path = tempfile.mkdtemp()
        shutil.rmtree(temp_path)

        a = svn.admin.Admin()

        try:
            # Create.
            a.create(temp_path)

            # Do a read.
            rc = svn.remote.RemoteClient('file:///' + temp_path)
            info = rc.info()
            _LOGGER.debug("Info from new repository: [%s]", str(info))
        finally:
            try:
                shutil.rmtree(temp_path)
            except:
                pass

