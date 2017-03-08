__author__ = 'tusharmakkar08'

import os
import unittest
import shutil
import tempfile
import logging

from tests.resources.expected_output import diff_summary, diff_summary_2, cat

import svn.constants
import svn.exception
import svn.common
import svn.local
import svn.remote
import svn.admin

_LOGGER = logging.getLogger(__name__)

# TODO(dustin): Refactor to build and use an adhoc SVN repository for the
#               tests.


class TestCommonClient(unittest.TestCase):
    """
    For testing svn/common.py
    """

    def __get_temp_path_to_use(self):
        # Determine a temporary location for our repository.
        temp_path = tempfile.mkdtemp()
        os.rmdir(temp_path)

        return temp_path

    def setUp(self):
        self.test_svn_url = 'http://svn.apache.org/repos/asf'
        self.test_start_revision = 1760022
        self.test_end_revision = 1760023

        self.__setup_test_environment()

    def __setup_test_environment(self):

        # Create test repository.
        self.__temp_repo_path = self.__get_temp_path_to_use()
        print("REPO_PATH: {}".format(self.__temp_repo_path))

        a = svn.admin.Admin()
        a.create(self.__temp_repo_path)

        # Check-out the test repository.

        self.__temp_co_path = self.__get_temp_path_to_use()
        print("CO_PATH: {}".format(self.__temp_co_path))

        r = svn.remote.RemoteClient('file://' + self.__temp_repo_path)
        r.checkout(self.__temp_co_path)

        # Create a client for it.
        self.__temp_lc = svn.local.LocalClient(self.__temp_co_path)

    def tearDown(self):
# TODO(dustin): !! This has to be refactored to use a random temporary file.
        if os.path.exists('CHANGES'):
            shutil.rmtree('CHANGES')

        try:
            shutil.rmtree(self.__temp_co_path)
        except:
            _LOGGER.exception("Could not cleanup temporary checkout path: [%s]", self.__temp_co_path)

        try:
            shutil.rmtree(self.__temp_repo_path)
        except:
            _LOGGER.exception("Could not cleanup temporary repository path: [%s]", self.__temp_repo_path)

    def __stage_co_directory_1(self):
        """Establish a new file, an added file, a committed file, and a changed file."""

        # Create a file that will not be committed.

        rel_filepath = 'new_file'
        filepath = os.path.join(self.__temp_co_path, rel_filepath)
        with open(filepath, 'w') as f:
            pass

        self.__temp_lc.add(rel_filepath)

        # Create a file that will be committed and remain unchanged.

        rel_filepath = 'committed_unchanged'
        filepath = os.path.join(self.__temp_co_path, rel_filepath)
        with open(filepath, 'w') as f:
            pass

        self.__temp_lc.add(rel_filepath)

        # Create a file that will be committed and then changed.

        rel_filepath_changed = 'committed_changed'
        filepath_changed = os.path.join(self.__temp_co_path, rel_filepath_changed)
        with open(filepath_changed, 'w') as f:
            pass

        self.__temp_lc.add(rel_filepath_changed)

        # Create a file that will be committed and then delete.

        rel_filepath_deleted = 'committed_deleted'
        filepath_deleted = os.path.join(self.__temp_co_path, rel_filepath_deleted)
        with open(filepath_deleted, 'w') as f:
            pass

        self.__temp_lc.add(rel_filepath_deleted)

        # Commit the new files.

        self.__temp_lc.commit("Initial commit.")

        # Do an update to pick-up the changes from the commit.

        self.__temp_lc.update()

        # Change the one committed file so that it will show up as modified.

        with open(filepath_changed, 'w') as f:
            f.write("new data")

        # Delete the one committed file so that it will show up as deleted.

        os.unlink(filepath_deleted)

        # Create a file that will be added and not committed.

        rel_filepath = 'added'
        filepath = os.path.join(self.__temp_co_path, rel_filepath)
        with open(filepath, 'w') as f:
            pass

        self.__temp_lc.add(rel_filepath)

    def test_status(self):
        self.__stage_co_directory_1()

        status = {}
        for s in self.__temp_lc.status():
            _LOGGER.debug("STATUS: %s", s)

            filename = os.path.basename(s.name)
            status[filename] = s

        added = status['added']
        self.assertTrue(added is not None and added.type == svn.constants.ST_ADDED)

        committed_changed = status['committed_changed']
        self.assertTrue(committed_changed is not None and committed_changed.type == svn.constants.ST_MODIFIED)

        committed_deleted = status['committed_deleted']
        self.assertTrue(committed_deleted is not None and committed_deleted.type == svn.constants.ST_MISSING)

    def test_error_client_formation(self):
        """
        Testing svn.exception.SvnException error while client formation
        :return:
        """
        with self.assertRaises(svn.exception.SvnException):
            svn.common.CommonClient(self.test_svn_url, 'random')

    def __get_cc(self):
        return svn.common.CommonClient(self.test_svn_url, 'url')

    def test_diff_summary(self):
        """
        Checking diff summary
        :return:
        """
        cc = self.__get_cc()
        actual_answer = \
            cc.diff_summary(
                self.test_start_revision,
                self.test_end_revision)

        self.assertTrue(
            actual_answer == diff_summary or \
            actual_answer == diff_summary_2)

    def test_diff(self):
        """
        Checking diff
        :return:
        """
        cc = self.__get_cc()
        actual_answer = \
            cc.diff(self.test_start_revision, self.test_end_revision)

        for index, individual_diff in enumerate(actual_answer):
            for diff_key in individual_diff:
                if diff_key == 'diff':
                    self.assertTrue(
                        'sling/trunk/bundles/extensions/models/pom.xml' \
                            in individual_diff[diff_key] or \
                        'sling/trunk/pom.xml' \
                            in individual_diff[diff_key])
                    self.assertTrue(
                        '<module>bundles/extensions/models</module>' \
                            in individual_diff[diff_key] or
                        '<description>Apache Sling Models</description>' \
                            in individual_diff[diff_key])
                elif diff_key == 'path':
                    self.assertTrue(
                        'http://svn.apache.org/repos/asf/sling/trunk/bundles/extensions/models/pom.xml' \
                            in individual_diff[diff_key] or \
                        'http://svn.apache.org/repos/asf/sling/trunk/pom.xml' \
                            in individual_diff[diff_key])

    def test_list(self):
        """
        Checking list
        :return:
        """
        cc = self.__get_cc()
        actual_answer = cc.list()
        self.assertEqual(next(actual_answer), 'abdera/')

    def test_info(self):
        """
        Checking info
        :return:
        """
        cc = self.__get_cc()
        actual_answer = cc.info()

        self.assertEqual(
            actual_answer['entry_path'],
            'asf')

        self.assertEqual(
            actual_answer['repository_root'],
            'http://svn.apache.org/repos/asf')

        self.assertEqual(
            actual_answer['entry#kind'],
            'dir')

        self.assertEqual(
            actual_answer['repository/uuid'],
            '13f79535-47bb-0310-9956-ffa450edef68')

    def test_log(self):
        """
        Checking log
        :return:
        """
        cc = self.__get_cc()
        actual_answer = \
            cc.log_default(revision_from=1761404, revision_to=1761403)
        self.assertEqual(next(actual_answer).author, 'sseifert')

    def test_cat(self):
        """
        Checking cat
        :return:
        """
        cc = self.__get_cc()
        actual_answer = cc.cat('abdera/abdera2/README', revision=1761404)
        self.assertEqual(cat, actual_answer.decode())

    def test_update(self):
        """
        Checking update
        :return:
        """
        cc = self.__get_cc()
        cc.update('.')

    def test_export(self):
        """
        Checking export
        :return:
        """
        cc = \
            svn.common.CommonClient(
                'http://svn.apache.org/repos/asf/tcl/websh/trunk/',
                'url')

        cc.export(to_path='CHANGES', revision=1761404)
        self.assertTrue(os.path.exists('CHANGES'))

    def test_force_export(self):
        """
        Checking export with force option
        :return:
        """
        cc = svn.common.CommonClient('http://svn.apache.org/repos/asf/tcl/websh/trunk/', 'url')
        cc.export(to_path='CHANGES', revision=1761404)
        self.assertTrue(os.path.exists('CHANGES'))

        with self.assertRaises(svn.exception.SvnException):
            cc.export(to_path='CHANGES', revision=1761404)
        try:
            cc.export(to_path='CHANGES', revision=1761404, force=True)
# TODO(dustin): This except probably unnecessary (any exception should likely
#               trigger failure).
        except svn.exception.SvnException:
            self.fail("SvnException raised with force export")
