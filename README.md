Introduction
------------

*svn* is a simple Subversion library for Python. I wrote it so that there could be a lightweight and accessible library that was also available on *PyPI*. It is compatible with both Python 2.7 and 3.3+

**I've only implemented the functionality that I have required: getting the tree, and getting the repository "info". You are more than welcome to submit pull-requests to add more support for additional subcommands.**

Usage
-----

Usage is divide between two clients that either allow for access to a local working-directory or a remote repository.

Both clients inherit a common set of methods that work with both local working-directories and remote repositories.

### LocalClient

*LocalClient* controls access to a local working copy.

```
import svn
import pprint

r = svn.LocalClient('/home/dustin/dev/repo')
r.export('/tmp/export')

pprint.pprint(r.info())
```

Output:

```
{u'last changed author': u'dustin',
 u'last changed date': u'2014-03-28 13:49:33 -0400 (Fri, 28 Mar 2014)',
 u'last changed rev': u'1910',
 u'node kind': u'directory',
 u'path': u'/home/dustin/dev/repo',
 u'relative url': u'^/svn',
 u'repository root': u'https://repo.local',
 u'repository uuid': u'7661bf0e-5f5b-4f8e-ab15-2494a5b67ce4',
 u'revision': u'1910',
 u'schedule': u'normal',
 u'url': u'https://repo.local/svn',
 u'working copy root path': u'/home/dustin/dev/repo'}
```

### RemoteClient

*RemoteClient* controls access to a remote repository.

- checkout(path)

```
import svn

r = svn.RemoteClient('https://repo.local/svn')
r.checkout('/tmp/working')
```

### Common Functionality

- info()
- export(path)
