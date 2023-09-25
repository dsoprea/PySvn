import os
from shutil import rmtree
from svn.exception import SvnException
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

    def test_add(self):
        with svn.test_support.temp_repo():
            with svn.test_support.temp_checkout() as (_, lc):
                dir1 = "d1"
                dir12 = os.path.join(dir1, "d2")
                dir123 = os.path.join(dir12, "d3")
                dir124 = os.path.join(dir12, "d4")
                for dir_ in [dir1, dir12, dir123, dir124]:
                    if os.path.isdir(dir_):
                        rmtree(dir_)
                    os.mkdir(dir_)

                added = "added"
                f12 = os.path.join(dir12, "f12")
                f123_1 = os.path.join(dir123, "f123.1")
                f123_2 = os.path.join(dir123, "f123.2")
                f124 = os.path.join(dir124, "f124")
                for file in [added, f12, f123_1, f123_2, f124]:
                    with open(file, 'w') as f:
                        pass

                lc.add(dir1, depth="empty")
                self.assertRaises(SvnException, lc.info, dir12)
                lc.run_command("revert", [dir1])

                lc.add(added)
                info = lc.info(added)
                self.assertEqual(info["wcinfo_schedule"], "add")

                lc.add(f124, do_include_parents=True)
                for path in [f124, dir124]:
                    info = lc.info(path)
                    self.assertEqual(info["wcinfo_schedule"], "add")

                lc.add(dir123, depth="infinity")
                for path in [f123_1, f123_2]:
                    info = lc.info(path)
                    self.assertEqual(info["wcinfo_schedule"], "add")



    def test_commit(self):
        with svn.test_support.temp_repo():
            with svn.test_support.temp_checkout() as (_, lc):
                svn.test_support.populate_bigger_file_changes1()

                rel_dirpath = "dir_to_be_added"
                if os.path.isdir(rel_dirpath):
                    rmtree(rel_dirpath)
                os.mkdir(rel_dirpath)
                lc.add(rel_dirpath)

                rel_filepath_added = os.path.join(rel_dirpath, "added")
                with open(rel_filepath_added, 'w') as f:
                    pass
                lc.add(rel_filepath_added)

                rel_filepath_committed = "committed"
                with open(rel_filepath_committed, 'w') as f:
                    pass
                lc.add(rel_filepath_committed)

                lc.commit("empty commit", ["."], depth="empty")
                info = lc.info(rel_filepath_committed)
                info_in_dir = lc.info(rel_filepath_added)
                self.assertEqual(info["wcinfo_schedule"], "add")
                self.assertEqual(info_in_dir["wcinfo_schedule"], "add")

                lc.commit("commit files", depth="files")
                info = lc.info(rel_filepath_committed)
                info_in_dir = lc.info(rel_filepath_added)
                self.assertEqual(info["wcinfo_schedule"], "normal")
                self.assertEqual(info_in_dir["wcinfo_schedule"], "add")

                lc.commit("commit all", depth="infinity")
                info_in_dir = lc.info(rel_filepath_added)
                self.assertEqual(info_in_dir["wcinfo_schedule"], "normal")

                lc.commit("commit external", include_ext=True)
                # TODO: include_ext/--include-externals not really tested
