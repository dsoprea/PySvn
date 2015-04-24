------------
Introduction
------------

*svn* is a simple Subversion library for Python. I wrote it so that there could be a lightweight and accessible library that was also available on *PyPI*. It is compatible with both Python 2.7 and 3.3+.

I've only implemented the functionality that I have required:

- Listing entries
- Getting info
- Getting log
- Checking-out
- Exporting

**You are more than welcome to submit pull-requests to add more support for additional subcommands.**


-----
Usage
-----

Usage is divided between two clients that either allow for access to a local 
working-directory or a remote repository.

Both clients inherit a common set of methods that work with both local working-
directories and remote repositories.

`svn.utility.get_client` is provided for convenience. If you provide a location 
that starts with a backslash, it will return a LocalClient instance. Otherwise, 
it will return a RemoteClient instance.


LocalClient
===========

*LocalClient* allows access to a local working copy.


RemoteClient
============

*RemoteClient* allows access to a remote repository.

- checkout(path)

Example::

    import svn.remote

    r = svn.remote.RemoteClient('https://repo.local/svn')
    r.checkout('/tmp/working')


Common Functionality
====================

These methods are available on both clients.

- info(rel_path=None)

    Get information about the directory.

Example::

    import pprint

    import svn.local

    r = svn.local.LocalClient('/tmp/test_repo.co')
    info = r.info()
    pprint.pprint(info)

    #{'commit#revision': 0,
    # 'commit/author': None,
    # 'commit/date': datetime.datetime(2015, 4, 24, 2, 53, 21, 874970, tzinfo=tzutc()),
    # 'commit_author': None,
    # 'commit_date': datetime.datetime(2015, 4, 24, 2, 53, 21, 874970, tzinfo=tzutc()),
    # 'commit_revision': 0,
    # 'entry#kind': 'dir',
    # 'entry#path': '/tmp/test_repo.co',
    # 'entry#revision': 0,
    # 'entry_kind': 'dir',
    # 'entry_path': '/tmp/test_repo.co',
    # 'entry_revision': 0,
    # 'relative_url': None,
    # 'repository/root': 'file:///tmp/test_repo',
    # 'repository/uuid': '7446d4e9-8846-46c0-858a-34a2a1739d1c',
    # 'repository_root': 'file:///tmp/test_repo',
    # 'repository_uuid': '7446d4e9-8846-46c0-858a-34a2a1739d1c',
    # 'url': 'file:///tmp/test_repo',
    # 'wc-info/depth': None,
    # 'wc-info/schedule': None,
    # 'wc-info/wcroot-abspath': None,
    # 'wcinfo_depth': None,
    # 'wcinfo_schedule': None,
    # 'wcinfo_wcroot_abspath': None}

    NOTE: The keys named with dashes, slashes, and hashes are considered 
          obsolete, and only available for backwards compatibility. We 
          have since moved to using only underscores to separate words.

- cat(rel_filepath)

    Get file-data as string.

Example::

    import svn.local

    l = svn.local.LocalClient('/tmp/test_repo')
    content = l.cat('test_file')

- log_default(timestamp_from_dt=None, timestamp_to_dt=None, limit=None, rel_filepath='')

    Perform a log-listing that can be bounded by time and/or take a maximum-
    count.

Example::

    import svn.local

    l = svn.local.LocalClient('/tmp/test_repo.co')

    for e in l.log_default():
        print(e)

    #LogEntry(date=datetime.datetime(2015, 4, 24, 3, 2, 39, 895975, tzinfo=tzutc()), msg='Added second file.', revision=2, author='dustin')
    #LogEntry(date=datetime.datetime(2015, 4, 24, 2, 54, 2, 136170, tzinfo=tzutc()), msg='Initial commit.', revision=1, author='dustin')

- export(to_path, revision=None)

    Checkout the tree without embedding an meta-information.

Example::

    import svn.remote

    r = svn.remote.RemoteClient('file:///tmp/test_repo')
    r.export('/tmp/test_export')

- list(extended=False, rel_path=None)

    Return either a flat-list of filenames or a list of objects describing even
    more information about each.

Example::

    import pprint

    import svn.local

    l = svn.local.LocalClient('/tmp/test_repo.co')
    
    # Flat list.

    entries = l.list()
    for filename in entries:
        print(filename)

    #aa
    #bb

    # Extended information.

    entries = l.list(extended=True)
    for entry in entries:
        pprint.pprint(entry)

    #{'author': 'dustin',
    # 'commit_revision': 1,
    # 'date': datetime.datetime(2015, 4, 24, 2, 54, 2, 136170, tzinfo=tzutc()),
    # 'is_directory': False,
    # 'kind': 'file',
    # 'name': 'aa',
    # 'size': 0,
    # 'timestamp': datetime.datetime(2015, 4, 24, 2, 54, 2, 136170, tzinfo=tzutc())}
    #{'author': 'dustin',
    # 'commit_revision': 2,
    # 'date': datetime.datetime(2015, 4, 24, 3, 2, 39, 895975, tzinfo=tzutc()),
    # 'is_directory': False,
    # 'kind': 'file',
    # 'name': 'bb',
    # 'size': 0,
    # 'timestamp': datetime.datetime(2015, 4, 24, 3, 2, 39, 895975, tzinfo=tzutc())}

- list_recursive(rel_path=None, yield_dirs=False, path_filter_cb=None)

    List all entries at and beneath the root or given relative-path.

Example::

    import pprint

    import svn.local

    l = svn.local.LocalClient('/tmp/test_repo.co')

    for rel_path, e in l.list_recursive():
        print('')
        print('[' + rel_path + ']')
        print('')

        pprint.pprint(e)

    #[]
    #
    #{'author': 'dustin',
    # 'commit_revision': 1,
    # 'date': datetime.datetime(2015, 4, 24, 2, 54, 2, 136170, tzinfo=tzutc()),
    # 'is_directory': False,
    # 'kind': 'file',
    # 'name': 'aa',
    # 'size': 0,
    # 'timestamp': datetime.datetime(2015, 4, 24, 2, 54, 2, 136170, tzinfo=tzutc())}
    #
    #[]
    #
    #{'author': 'dustin',
    # 'commit_revision': 2,
    # 'date': datetime.datetime(2015, 4, 24, 3, 2, 39, 895975, tzinfo=tzutc()),
    # 'is_directory': False,
    # 'kind': 'file',
    # 'name': 'bb',
    # 'size': 0,
    # 'timestamp': datetime.datetime(2015, 4, 24, 3, 2, 39, 895975, tzinfo=tzutc())}
    #
    #[dir1]
    #
    #{'author': 'dustin',
    # 'commit_revision': 3,
    # 'date': datetime.datetime(2015, 4, 24, 3, 25, 13, 479212, tzinfo=tzutc()),
    # 'is_directory': False,
    # 'kind': 'file',
    # 'name': 'cc',
    # 'size': 0,
    # 'timestamp': datetime.datetime(2015, 4, 24, 3, 25, 13, 479212, tzinfo=tzutc())}


Important
=========

Previously, the *LocalClient* and *RemoteClient* classes were exposed at the 
package level:

- svn.LocalClient
- svn.RemoteClient

Unfortunately, this interfered with dependency management during installation.
The imports will now have to be, respectively:

- svn.local (for LocalClient)
- svn.remote (for RemoteClient)

We're sorry for the inconvenience.
