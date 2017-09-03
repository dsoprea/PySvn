|donate|

|Build\_Status|
|Coverage\_Status|


------------
Introduction
------------

*svn* is a simple Subversion library for Python. I wrote it so that there could be a lightweight and accessible library that was also available on *PyPI*. It is compatible with both Python 2.7 and 3.3+.

The library wraps the `svn` commandline client, which should consequently be installed on the local system.

Functions currently implemented:

- list
- info
- log
- checkout
- export
- cat
- diff
- diff_summary
- status
- add
- commit
- update
- cleanup

In addition, there is also an "admin" class (`svn.admin.Admin`) that provides a `create` method with which to create repositories.

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

You may pass `username` and `password` as optional arguments to both the constructor and utility function.


LocalClient
===========

*LocalClient* allows access to a local working copy.


RemoteClient
============

*RemoteClient* allows access to a remote repository.

SvnException
============

*SvnException* is raised whenever there is an issue with the svn repository. We are no longer supporting catching
*ValueError*.

checkout(path)
^^^^^^^^^^^^^^

Checkout a remote repository::

    import svn.remote

    r = svn.remote.RemoteClient('https://repo.local/svn')
    r.checkout('/tmp/working')


Common Functionality
====================

These methods are available on both clients.

info(rel_path=None)
^^^^^^^^^^^^^^^^^^^

Get information about the directory::

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

cat(rel_filepath)
^^^^^^^^^^^^^^^^^

Get file-data as string::

    import svn.local

    l = svn.local.LocalClient('/tmp/test_repo')
    content = l.cat('test_file')

log_default(timestamp_from_dt=None, timestamp_to_dt=None, limit=None, rel_filepath='', stop_on_copy=False, revision_from=None, revision_to=None, changelist=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Perform a log-listing that can be bounded by time or revision number and/or take a maximum-
count::

    import svn.local

    l = svn.local.LocalClient('/tmp/test_repo.co')

    for e in l.log_default():
        print(e)

    #LogEntry(date=datetime.datetime(2015, 4, 24, 3, 2, 39, 895975, tzinfo=tzutc()), msg='Added second file.', revision=2, author='dustin')
    #LogEntry(date=datetime.datetime(2015, 4, 24, 2, 54, 2, 136170, tzinfo=tzutc()), msg='Initial commit.', revision=1, author='dustin')

export(to_path, revision=None, force=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Checkout the tree without embedding an meta-information::

    import svn.remote

    r = svn.remote.RemoteClient('file:///tmp/test_repo')
    r.export('/tmp/test_export')

We can also use `force` option to force the svn export.

list(extended=False, rel_path=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return either a flat-list of filenames or a list of objects describing even
more information about each::

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

list_recursive(rel_path=None, yield_dirs=False, path_filter_cb=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List all entries at and beneath the root or given relative-path::

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

diff_summary(start_revision,  end_revision)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Summarizes all the diff between start and end revision id ::

    import svn.remote

    l = svn.remote.RemoteClient('http://svn.apache.org/repos/asf')
    print l.diff_summary(1760022, 1760023)

    # [{'item': 'modified',
    #  'kind': 'file',
    #  'path': 'http://svn.apache.org/repos/asf/sling/trunk/pom.xml'},
    # {'item': 'added',
    #  'kind': 'file',
    #  'path': 'http://svn.apache.org/repos/asf/sling/trunk/bundles/extensions/models/pom.xml'}]

diff(start_revision,  end_revision)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Finds all the diff between start and end revision id. Here another key of 'diff' is added which shows the diff of files.

.. |donate| image:: https://pledgie.com/campaigns/31718.png?skin_name=chrome
   :alt: Click here to lend your support to: PySvn and make a donation at pledgie.com !
   :target: https://pledgie.com/campaigns/31718
.. |Build_Status| image:: https://travis-ci.org/dsoprea/PySvn.svg?branch=master
   :target: https://travis-ci.org/dsoprea/PySvn
.. |Coverage_Status| image:: https://coveralls.io/repos/github/dsoprea/PySvn/badge.svg?branch=master
   :target: https://coveralls.io/github/dsoprea/PySvn?branch=master
