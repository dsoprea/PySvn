import os
import unittest

import svn.constants
import svn.test_support


class TestLocalClient(unittest.TestCase):
    def test_status(self):
        with svn.test_support.temp_repo():
            with svn.test_support.temp_checkout() as (wc, lc):
                svn.test_support.populate_bigger_file_changes1()

                file_in_cl = 'file_in_cl'
                with open(file_in_cl, 'w') as f:
                    f.write("data")

                lc.add(file_in_cl)
                lc.run_command('changelist', ['test-cl', file_in_cl])

                status = {}
                for s in lc.status():
                    filename = os.path.basename(s.name)
                    status[filename] = s

                added = status['added']
                self.assertIsNotNone(added)
                self.assertTrue(added.type, svn.constants.ST_ADDED)
                self.assertEqual(added.changelist, None)

                committed_deleted = status['committed_deleted']
                self.assertIsNotNone(committed_deleted)
                self.assertEqual(committed_deleted.type, svn.constants.ST_MISSING)
                self.assertEqual(added.changelist, None)

                in_cl = status[file_in_cl]
                self.assertIsNotNone(in_cl)
                self.assertEqual(in_cl.changelist, 'test-cl')


    def test_remove(self):
        with svn.test_support.temp_repo():
            with svn.test_support.temp_checkout() as (wc_path, lc):
                svn.test_support.populate_bigger_file_changes1()

                self.assertTrue(os.path.exists('new_file'))

                current_entries = lc.list()
                current_entries = list(current_entries)

                self.assertIn('new_file', current_entries)

                lc.remove('new_file')

                # Should no longer be on the disk.
                self.assertFalse(os.path.exists('new_file'))

                # Should still be in the repository.

                current_entries = lc.list()
                current_entries = list(current_entries)

                self.assertIn('new_file', current_entries)

                # Confirm that the entry now presents as "deleted".

                status_all = lc.status()
                status_all = list(status_all)

                status_index = {
                    s.name: s
                    for s
                    in status_all
                }

                filepath = os.path.join(wc_path, 'new_file')
                status = status_index[filepath]

                self.assertEquals(status.type, svn.constants.ST_DELETED)

                # Commit the change.

                lc.commit("Remove file.")

                # Should still be in the repository, because we haven't yet
                # updated.

                current_entries = lc.list()
                current_entries = list(current_entries)

                self.assertIn('new_file', current_entries)

                lc.update()

                # *Now* it should be gone.

                current_entries = lc.list()
                current_entries = list(current_entries)

                self.assertNotIn('new_file', current_entries)

    def test_cleanup(self):
        with svn.test_support.temp_repo():
            with svn.test_support.temp_checkout() as (_, lc):
                lc.cleanup()
