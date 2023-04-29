from __future__ import print_function          # PY3

import os
import unittest
import shutil
import tempfile

import svn.common
import svn.local
import svn.utility
import svn.test_support
from svn.common import normpath2  # unify file paths for comparison (win)
from svn.exception import SvnException

class TestCommonClient(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.maxDiff = None
        super(TestCommonClient, self).__init__(*args, **kwargs)

    def test_update(self):
        with svn.test_support.temp_repo():
            with svn.test_support.temp_checkout() as (_, lc):
                svn.test_support.populate_bigger_file_changes1()

                lc.commit("Second commit.")
                lc.update()
                self.assertEqual(3, lc.info()['commit_revision'])

                lc.update(revision=1)
                self.assertEqual(1, lc.info()['commit_revision'])

    def test_diff_summary(self):
        with svn.test_support.temp_repo() as (repo_path, _):
            with svn.test_support.temp_checkout() as (_, lc):
                svn.test_support.populate_bigger_file_changes1()
                lc.commit("Second revision.")

            cc = svn.utility.get_common_for_cwd()

            diff = cc.diff_summary(1, 2)

            index = {
                diff['path']: diff
                for diff
                in diff
            }

            self.assertEquals(len(index), 1)

            file_uri2 = 'file:///{}'.format(normpath2( os.path.join(repo_path, 'committed_changed')))
            self.assertEquals(index[file_uri2]['item'], 'modified')

    def test_diff__with_diff(self):
        with svn.test_support.temp_common() as (_, working_path, cc):
            svn.test_support.populate_bigger_file_changes1()
            svn.test_support.populate_bigger_file_change1()

            actual = \
                cc.diff(
                    1,
                    2)

            filepath = normpath2(os.path.join(working_path, 'committed_changed'))

            expected = {
                filepath: {
                    'right_phrase': [
                        filepath,
                        '(revision 2)'
                    ],
                    'hunks': [
                        {
                            'body': '+new data\n\\ No newline at end of file',
                            'lines_phrase': '@@ -0,0 +1 @@'
                        }
                    ],
                    'left_phrase': [
                        filepath,
                        '(revision 1)'
                    ]
                }
            }

            self.assertEqual(actual, expected)

    def test_diff__with_add(self):
        # Make sure that we correctly handle an add, which represents in the
        # results with a `None` value.

        with svn.test_support.temp_common() as (_, working_path, cc):
            svn.test_support.populate_bigger_file_changes1()
            rel_filepath2 = svn.test_support.populate_bigger_file_change1()
            actual = \
                cc.diff(
                    2,
                    3)
                    
            filepath1 = normpath2(os.path.join(working_path, 'added'))
            filepath2 = normpath2(os.path.join(working_path, rel_filepath2))

            expected = {
                filepath1: None,
                filepath2: {
                    'right_phrase': [filepath2, '(revision 3)'],
                    'hunks': [{
                        'body': '+Lorem ipsum\n+dolor sit\n+amet, consectetur\n+adipiscing elit,\n+sed do\n+eiusmod tempor\n+incididunt ut\n+labore et\n+dolore magna\n+aliqua. Ut\n+enim ad\n+minim veniam,\n+quis nostrud\n+exercitation ullamco\n+laboris nisi\n+ut aliquip\n+ex ea\n+commodo consequat.\n+Duis aute\n+irure dolor\n+in reprehenderit\n+in voluptate\n+velit esse\n+cillum dolore\n+eu fugiat\n+nulla pariatur.\n+Excepteur sint\n+occaecat cupidatat\n+non proident,\n+sunt in\n+culpa qui\n+officia deserunt\n+mollit anim\n+id est\n+laborum."',
                        'lines_phrase': '@@ -0,0 +1,35 @@'
                    }],
                    'left_phrase': [filepath2, '(nonexistent)']
                }
            }

            self.assertEqual(actual, expected)

    def test_list(self):
        with svn.test_support.temp_common() as (_, _, cc):
            svn.test_support.populate_bigger_file_changes1()

            entries = cc.list()
            entries = sorted(entries)

            expected = [
                'committed_changed',
                'committed_deleted',
                'committed_unchanged',
                'new_file',
            ]

            self.assertEqual(entries, expected)

    def test_info(self):
        with svn.test_support.temp_common() as (repo_path, _, cc):
            svn.test_support.populate_bigger_file_changes1()

            info = cc.info()

            self.assertEqual(
                info['entry_path'],
                '.')

            uri = 'file:///{}'.format(repo_path)

            self.assertEqual(
                normpath2(info['repository_root']),
                normpath2(uri))

            self.assertEqual(
                info['entry#kind'],
                'dir')

    def test_info_revision(self):
        with svn.test_support.temp_common() as (_, working_path, cc):
            svn.test_support.populate_bigger_file_changes1()

            # There's already an add staged.

            lc = svn.local.LocalClient(working_path)
            lc.commit("Second changes.")

            # Get info for an older revision (to make sure the revision
            # argument is applied).

            info1 = cc.info(revision=1)
            self.assertEquals(info1['commit_revision'], 1)

            info2 = cc.info(revision=2)
            self.assertEquals(info2['commit_revision'], 2)

    def test_log(self):
        with svn.test_support.temp_common() as (_, _, cc):
            svn.test_support.populate_bigger_file_changes1()

            history = cc.log_default()
            history = list(history)

            self.assertEquals(len(history), 1)

            l = history[0]

            self.assertEquals(l.revision, 1)
            self.assertEquals(l.msg, 'Initial commit.')

    def test_cat(self):
        with svn.test_support.temp_common() as (_, _, cc):
            svn.test_support.populate_bigger_file_changes1()

            content1 = cc.cat('committed_changed', revision=1)
            self.assertEqual(content1, b'')

            content2 = cc.cat('committed_changed', revision=2)
            self.assertEqual(content2, b'new data')

    def test_export(self):
        with svn.test_support.temp_common() as (_, _, cc):
            svn.test_support.populate_bigger_file_changes1()

            # Just a name. Will be created by the export.
            temp_path = tempfile.mktemp()

            try:
                cc.export(to_path=temp_path, revision=2)

                with open('committed_changed') as f:
                    content = f.read()

                self.assertEquals(content, "new data")
            finally:
                try:
                    shutil.rmtree(temp_path)
                except:
                    pass

    def test_force__export(self):
        with svn.test_support.temp_common() as (_, _, cc):
            svn.test_support.populate_bigger_file_changes1()

            with svn.test_support.temp_path() as temp_path:
                cc.export(to_path=temp_path, revision=2, force=True)

                with open('committed_changed') as f:
                    content = f.read()

                self.assertEquals(content, "new data")

class TestCommonProperties(unittest.TestCase):
    def test_prop_commands(self):
        with svn.test_support.temp_repo():
            with svn.test_support.temp_checkout() as (wc, lc):
                svn.test_support.populate_prop_files()
    
                lc.propset('svn:mime-type','image/jpeg', rel_path='foo.jpg')
                lc.propset('owner','sally', rel_path='foo.bar')
                lc.propset('svn:ignore','foo.bak') # set on directory level
                
                lc.commit('Committing properties')
                lc.update()
                
                lc.propset('svn:keywords','Author Date Rev', rel_path='foo.bar')
                
                propdict = lc.propget('svn:mime-type', rel_path='foo.jpg')
                path1 = normpath2(os.path.join(wc, 'foo.jpg'))
                self.assertEquals(len(propdict), 1)
                self.assertEquals(propdict[path1], 'image/jpeg')

                propdict = lc.propget('svn:ignore', '.') # at directory level
                path1 = normpath2(os.path.join(wc, '.'))
                self.assertEquals(len(propdict), 1)
                self.assertEquals(propdict[path1], 'foo.bak')
                
                propdict = lc.properties(rel_path='foo.bar')
                self.assertEquals(len(propdict), 2)
                self.assertEquals(propdict['owner'], 'sally')
                self.assertEquals(propdict['svn:keywords'], 'Author Date Rev')
                
                lc.propdel('owner', rel_path='foo.bar')
                
                lc.commit('Committing after deleting property')
                lc.update()

                propdict = lc.properties(rel_path='foo.bar')
                self.assertEquals(len(propdict), 1)
                self.assertEquals(propdict['svn:keywords'], 'Author Date Rev')
                
                propdict = lc.properties(rel_path='foo.bar',revision=1)
                self.assertEquals(len(propdict), 0)

                propdict = lc.properties(rel_path='foo.bar',revision=2)
                self.assertEquals(len(propdict), 1)
                self.assertEquals(propdict['owner'], 'sally')

                propdict = lc.propget('owner', rel_path='foo.bar',revision=2)
                path1 = normpath2(os.path.join(wc, 'foo.bar'))
                self.assertEquals(len(propdict), 1)
                self.assertEquals(propdict[path1], 'sally')

                # property was deleted before
                with self.assertRaises(SvnException) as cx:
                    lc.propget('owner', rel_path='foo.bar')              
                """
                # to get the multi-line error message
                #exc = cx.exception
                #print('\nMessage =\n',exc.message)
                """
