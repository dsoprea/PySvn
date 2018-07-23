import unittest
from getpass import getuser

from testfixtures import (
    compare,
    TempDirectory,
    )

import svn.local
import svn.admin
from svn.common import (
    _STATUS_ENTRY,
    LOG_ENTRY,
    )


class TestLocalClient(unittest.TestCase):

    def setUp(self):
        self.dir = TempDirectory()
        self.addCleanup(self.dir.cleanup)

        self.admin = svn.admin.Admin()
        self.admin.create(self.dir.getpath('fakerepo'))

        self.local = svn.local.LocalClient.checkout(
            repo_path=self.dir.getpath('fakerepo'),
            checkout_path=self.dir.getpath('fakecheckout'))
        self.dir.write('fakecheckout/initial.txt', b'initial')
        self.local.add('initial.txt')
        self.local.commit('initial checkin')

    def test_add(self):
        self.dir.write('fakecheckout/add.txt', b'add')
        self.local.add('add.txt')
        expected = [
            _STATUS_ENTRY(
                name=self.dir.getpath('fakecheckout/add.txt'),
                type_raw_name='added',
                type=1,
                revision=-1),
            ]
        actual = self.local.status()
        compare(expected=expected, actual=actual)

    def test_delete(self):
        self.local.delete('initial.txt')
        expected = [
            _STATUS_ENTRY(
                name=self.dir.getpath('fakecheckout/initial.txt'),
                type_raw_name='deleted',
                type=3,
                revision=1),
            ]
        actual = self.local.status()
        compare(expected=expected, actual=actual)

    def test_move(self):
        self.local.move('initial.txt', 'moved.txt')
        expected = [
            _STATUS_ENTRY(
                name=self.dir.getpath('fakecheckout/initial.txt'),
                type_raw_name='deleted',
                type=3,
                revision=1),
            _STATUS_ENTRY(
                name=self.dir.getpath('fakecheckout/moved.txt'),
                type_raw_name='added',
                type=1,
                revision=None),
            ]
        actual = self.local.status()
        compare(expected=expected, actual=actual)

    def test_commit(self):
        self.dir.write('fakecheckout/testfile1.txt', b'testdata_for_commit')
        self.local.add('testfile1.txt')
        self.local.commit('fakemessage')
        self.local.update()
        actual = list(self.local.log_default(limit=1))
        expected = [
            LOG_ENTRY(
                # This (grabbing our expected from a component in
                # actual) is quite naughty, but I don't yet want to
                # write a custom comparer for integration tests where
                # dates are real.
                date=actual[0].date,
                # Back to more orthodox testing...
                msg='fakemessage',
                revision=2,
                author=getuser(),
                changelist=None),
            ]
        compare(expected=expected, actual=actual)
