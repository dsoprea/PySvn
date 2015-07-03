#!/usr/bin/env python2.7

import sys
import os.path
dev_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, dev_path)

import logging
_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)
logging.getLogger('boto').setLevel(logging.INFO)

ch = logging.StreamHandler()

FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(FMT)
ch.setFormatter(formatter)
_logger.addHandler(ch)

print("Printing log.")

import pprint

import svn.local

l = svn.local.LocalClient('/tmp/test_repo.co')

for rel_path, e in l.list_recursive():
    print('')
    print('[' + rel_path + ']')
    print('')
    pprint.pprint(e)

#LogEntry(date=datetime.datetime(2015, 4, 24, 3, 2, 39, 895975, tzinfo=tzutc()), msg='Added second file.', revision=2, author='dustin')
#LogEntry(date=datetime.datetime(2015, 4, 24, 2, 54, 2, 136170, tzinfo=tzutc()), msg='Initial commit.', revision=1, author='dustin')

sys.exit(0)

import svn.local
import svn.remote
import pprint

#r = svn.remote.RemoteClient('https://xyz/svn/adam2/trunk')
#r = svn.local.LocalClient('/Users/dustin/development/php/adam2')

import svn.local
import pprint

l = svn.local.LocalClient('/tmp/test_repo.co')
info = l.info()
pprint.pprint(info)

sys.exit(0)

#print(list(r.list(extended=True)))

l = r.list_recursive(rel_path=None, yield_dirs=False, path_filter_cb=None)
l = list(l)

pprint.pprint(l)

#print(r.cat('sfs/package/DEBIAN/postinst'))

#import dateutil.parser
#import datetime
#
#from_ = datetime.datetime.now().replace(day=21)
#for e in r.log_default(timestamp_from_dt=from_):
#    print(e)
#
#sys.exit(0)

#i = r.info()
#print(i)
sys.exit(0)

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

#l = svn.local.LocalClient('/Users/dustin/development/php/adam2')
