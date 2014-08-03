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

- export(path)

Example *LocalClient* usage::

    import svn.local
    import pprint

    r = svn.local.LocalClient('/dev/repo')
    r.export('/tmp/export')

    pprint.pprint(r.info())

Output::

    { 'commit#revision': 0,
      'commit/author': None,
      'commit/date': datetime.datetime(2014, 4, 1, 5, 50, 27, 826988, tzinfo=tzutc()),
      'commit_author': None,
      'commit_date': datetime.datetime(2014, 4, 1, 5, 50, 27, 826988, tzinfo=tzutc()),
      'commit_revision': 0,
      'entry#kind': 'dir',
      'entry#path': 'working_copy',
      'entry#revision': 0,
      'entry_kind': 'dir',
      'entry_path': 'working_copy',
      'entry_revision': 0,
      'relative_url': '^/',
      'repository/root': 'file:///Users/dustin/development/python/svn/test/repo',
      'repository/uuid': '48195b71-8d94-4528-a019-ec81ebc7e65a',
      'repository_root': 'file:///Users/dustin/development/python/svn/test/repo',
      'repository_uuid': '48195b71-8d94-4528-a019-ec81ebc7e65a',
      'url': 'file:///Users/dustin/development/python/svn/test/repo',
      'wc-info/depth': None,
      'wc-info/schedule': None,
      'wc-info/wcroot-abspath': None,
      'wcinfo_depth': None,
      'wcinfo_schedule': None,
      'wcinfo_wcroot_abspath': None }


RemoteClient
============

*RemoteClient* allows access to a remote repository.

- checkout(path)
- export(path)

Example *RemoteClient* usage::

    import svn.remote

    r = svn.remote.RemoteClient('https://repo.local/svn')
    r.checkout('/tmp/working')


Common Functionality
====================

These methods are available on both clients.

- info()
- cat(rel_filepath)
- log_default(timestamp_from_dt=None, timestamp_to_dt=None, limit=None)


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
