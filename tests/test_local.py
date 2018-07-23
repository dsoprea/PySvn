import unittest

from testfixtures import (
    compare,
    TempDirectory,
    )

import svn.local
import svn.admin
from svn.common import _STATUS_ENTRY


class TestLocalClient(unittest.TestCase):

    def setUp(self):
        self.dir = TempDirectory()
        self.addCleanup(self.dir.cleanup)

        self.admin = svn.admin.Admin()
        self.admin.create(self.dir.getpath('fakerepo'))

        self.local = svn.local.LocalClient.checkout(
            repo_path=self.dir.getpath('fakerepo'),
            checkout_path=self.dir.getpath('fakecheckout'))

    def test_add(self):
        self.dir.write('fakecheckout/testfile1.txt', 'testdata')
        self.local.add('testfile1.txt')
        expected = [
            _STATUS_ENTRY(
                name=self.dir.getpath('fakecheckout/testfile1.txt'),
                type_raw_name='added',
                type=1,
                revision=-1),
            ]
        actual = self.local.status()
        compare(expected=expected, actual=actual)

    # Commenting out until I have a .log method later
    # def test_commit(self):
    #     self.dir.write('fakecheckout/testfile1.txt', 'testdata_for_commit')
    #     self.local.add('testfile1.txt')
    #     self.local.commit('fakemessage')
    #     self.local.update()
    #     expected = 'todo'
    #     actual = self.local.log()
    #     compare(expected=expected, actual=actual)
