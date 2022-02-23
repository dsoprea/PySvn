import os
import contextlib
import tempfile
import shutil
import uuid

import svn.constants
import svn.common
import svn.remote
import svn.local
import svn.admin

@contextlib.contextmanager
def temp_path():
    original_wd = os.getcwd()

    temp_path = None
    try:
        temp_path = tempfile.mkdtemp()
        os.chdir(temp_path)

        yield temp_path
    finally:
        os.chdir(original_wd)

        if temp_path is not None and os.path.exists(temp_path) is True:
            try:
                shutil.rmtree(temp_path)
            except:
                pass

@contextlib.contextmanager
def temp_repo():
    """Initialize a repository in the current path."""

    with temp_path() as repo_path:
        a = svn.admin.Admin()
        a.create('.')

        rc = svn.remote.RemoteClient('file://{}'.format(repo_path))

        yield repo_path, rc

@contextlib.contextmanager
def temp_checkout():
    """Checkout a temporary working directory from the repository in the
    current path.
    """

    repo_path = os.getcwd()

    with temp_path() as working_path:
        rc = svn.remote.RemoteClient('file://{}'.format(repo_path))
        rc.checkout('.')

        lc = svn.local.LocalClient(working_path)

        yield working_path, lc

@contextlib.contextmanager
def temp_common():
    """Initialize a repository in the current path and return a CC. This is
    used to test CC functionality that should work identically regardless of
    local or remote.
    """

    with temp_repo() as (repo_path, _):
        with temp_checkout() as (working_path, _):
            cc = svn.common.CommonClient(
                    working_path,
                    svn.constants.LT_PATH)

            yield repo_path, working_path, cc

def populate_bigger_file_changes1():
    """Establish a deterministic history of changes."""

    assert \
        os.path.exists('.svn') is True, \
        "test_local_populate1() must be called with the working-directory " \
        "as the CWD."

    working_path = os.getcwd()
    lc = svn.local.LocalClient(working_path)

    # Create a file that will not be committed.

    rel_filepath = 'new_file'
    with open(rel_filepath, 'w') as f:
        pass

    lc.add(rel_filepath)

    # Create a file that will be committed and remain unchanged.

    rel_filepath = 'committed_unchanged'
    with open(rel_filepath, 'w') as f:
        pass

    lc.add(rel_filepath)

    # Create a file that will be committed and then changed.

    rel_filepath_changed = 'committed_changed'
    with open(rel_filepath_changed, 'w') as f:
        pass

    lc.add(rel_filepath_changed)

    # Create a file that will be committed and then delete.

    rel_filepath_deleted = 'committed_deleted'
    with open(rel_filepath_deleted, 'w') as f:
        pass

    lc.add(rel_filepath_deleted)

    # Commit the new files.
    lc.commit("Initial commit.")

    # Do an update to pick-up the changes from the commit.
    lc.update()

    # Change the one committed file so that it will show up as modified.

    with open(rel_filepath_changed, 'w') as f:
        f.write("new data")

    # Commit the file change.
    lc.commit("Change file.")

    # Delete the one committed file so that it will show up as deleted.
    os.unlink(rel_filepath_deleted)

    # Create a file that will be added and not committed.

    rel_filepath = 'added'
    with open(rel_filepath, 'w') as f:
        pass

    lc.add(rel_filepath)

def populate_bigger_file_change1():
    """Upload a file having many lines and then do another commit with
    several changed.
    """

    assert \
        os.path.exists('.svn') is True, \
        "test_local_populate1() must be called with the working-directory " \
        "as the CWD."

    working_path = os.getcwd()
    lc = svn.local.LocalClient(working_path)

    # Create a file that will be committed and then changed a lot.

    rel_filepath = 'big_{}'.format(str(uuid.uuid4()))
    with open(rel_filepath, 'w') as f:
        f.write("""\
Lorem ipsum
dolor sit
amet, consectetur
adipiscing elit,
sed do
eiusmod tempor
incididunt ut
labore et
dolore magna
aliqua. Ut
enim ad
minim veniam,
quis nostrud
exercitation ullamco
laboris nisi
ut aliquip
ex ea
commodo consequat.
Duis aute
irure dolor
in reprehenderit
in voluptate
velit esse
cillum dolore
eu fugiat
nulla pariatur.
Excepteur sint
occaecat cupidatat
non proident,
sunt in
culpa qui
officia deserunt
mollit anim
id est
laborum."
""")

    lc.add(rel_filepath)

    # Commit the new files.
    lc.commit("Commit first version of file (big diff).")

    # Apply the bigger change.

    with open(rel_filepath, 'w') as f:
        f.write("""\
Lorem ipsum
dolor sit
amet, consectetur
adipiscing elit,
sed do
!newline1
eiusmod tempor
incididunt ut
labore et
dolore magna
aliqua. Ut
enim ad
minim veniam,
quis nostrud
exercitation ullamco
laboris nisi
ut aliquip
ex ea
commodo consequat.
Duis aute
irure dolor
in reprehenderit
in voluptate
velit esse
cillum dolore
eu fugiat
nulla pariatur.
Excepteur sint
occaecat cupidatat
!newline2
non proident,
sunt in
culpa qui
officia deserunt
mollit anim
id est
laborum."
""")

    lc.commit("Commit second version of file (big diff).")

    # Do an update to pick-up the changes from the commit.
    lc.update()

    return rel_filepath
