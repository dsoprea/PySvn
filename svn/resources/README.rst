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

Usage is divided between two clients that either allow for access to a local working-directory or a remote repository.

Both clients inherit a common set of methods that work with both local working-directories and remote repositories.


LocalClient
===========

*LocalClient* allows access to a local working copy.

Example *LocalClient* usage::

    import svn
    import pprint

    r = svn.LocalClient('/dev/repo')
    r.export('/tmp/export')

    pprint.pprint(r.info())

Output::

    {'commit#revision': 0,
     'commit/author': None,
     'commit/date': datetime.datetime(2014, 4, 1, 5, 50, 27, 826988, tzinfo=tzutc()),
     'entry#kind': 'dir',
     'entry#path': 'working_copy',
     'entry#revision': 0,
     'relative_url': '^/',
     'repository/root': 'file:///svn/test/repo',
     'repository/uuid': '48195b71-8d94-4528-a019-ec81ebc7e65a',
     'url': 'file:///svn/test/repo',
     'wc-info/depth': 'infinity',
     'wc-info/schedule': 'normal',
     'wc-info/wcroot-abspath': '/svn/dev/working_copy'}


RemoteClient
============

*RemoteClient* allows access to a remote repository.

- checkout(path)

Example *RemoteClient* usage::

    import svn

    r = svn.RemoteClient('https://repo.local/svn')
    r.checkout('/tmp/working')


Common Functionality
====================

These methods are available on both clients.

- info()
- export(path)
- cat(rel_filepath)
- log_default(timestamp_from_dt=None, timestamp_to_dt=None, limit=None)
