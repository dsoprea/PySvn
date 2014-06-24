Introduction
------------

*svn* is a simple Subversion library for Python. I wrote it so that there could be a lightweight and accessible library that was also available on *PyPI*. It is compatible with both Python 2.7 and 3.3+.

**I've only implemented the functionality that I have required: getting the tree, and getting the repository info. You are more than welcome to submit pull-requests to add more support for additional subcommands.**

Usage
-----

Usage is divided between two clients that either allow for access to a local working-directory or a remote repository.

Both clients inherit a common set of methods that work with both local working-directories and remote repositories.

### LocalClient

*LocalClient* allows access to a local working copy.

Example *LocalClient* usage:

```
import svn
import pprint

r = svn.LocalClient('/home/dustin/dev/repo')
r.export('/tmp/export')

i = r.info()

print(i.attrib['kind'])
print(i.attrib['path'])
print(i.attrib['revision'])

print(i.find('url').text)
print(i.find('relative-url').text)

repo = i.find('repository')
print(repo.find('root').text)
print(repo.find('uuid').text)

commit = i.find('commit')
print(commit.find('author').text)
print(commit.find('date').text)
```

Output:

```
dir
/Users/dustin/development/php/adam2
2030
https://opsvn.openpeak.com/svn/adam2/trunk
^/trunk
https://opsvn.openpeak.com/svn/adam2
7661bf0e-5f5b-4f8e-ab15-2494a5b67ce4
dustin
2014-04-03T13:58:08.396645Z
```

### RemoteClient

*RemoteClient* allows access to a remote repository.

- checkout(path)

Example *RemoteClient* usage:

```
import svn

r = svn.RemoteClient('https://repo.local/svn')
r.checkout('/tmp/working')
```

### Common Functionality

These methods are available on both clients.

- info()
- export(path)
- cat(rel_filepath)
- log_default(timestamp_from_dt=None, timestamp_to_dt=None, limit=None)
