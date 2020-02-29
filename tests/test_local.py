import os
import unittest

import svn.constants
import svn.test_support


class TestLocalClient(unittest.TestCase):
    def test_status(self):
        with svn.test_support.temp_repo():
            with svn.test_support.temp_checkout() as (_, lc):
                svn.test_support.populate_bigger_file_changes1()

                status = {}
                for s in lc.status():
                    filename = os.path.basename(s.name)
                    status[filename] = s

                added = status['added']
                self.assertTrue(added is not None and added.type == svn.constants.ST_ADDED)

                committed_deleted = status['committed_deleted']
                self.assertTrue(committed_deleted is not None and committed_deleted.type == svn.constants.ST_MISSING)

    def test_cleanup(self):
        with svn.test_support.temp_repo():
            with svn.test_support.temp_checkout() as (_, lc):
                lc.cleanup()
