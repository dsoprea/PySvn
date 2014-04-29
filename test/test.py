#!/usr/bin/env python2.7

import sys
sys.path.insert(0, '..')

import svn

#r = svn.RemoteClient('https://opsvn.openpeak.com/svn/adam2/trunk')
r = svn.LocalClient('/Users/dustin/development/php/adam2')

#print(r.cat('sfs/package/DEBIAN/postinst'))

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

#print(r.info().items())
#print(r.info().getchildren())

#import pprint
#pprint.pprint(r.info())

#r.checkout('/tmp/checkout_2')
#r.export('/tmp/export_1')

#l = svn.LocalClient('/Users/dustin/development/php/adam2')
