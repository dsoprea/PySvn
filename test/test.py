#!/usr/bin/env python2.7

import sys
sys.path.insert(0, '..')

import svn

#r = svn.RemoteClient('https://opsvn.openpeak.com/svn/adam2/trunk')
r = svn.LocalClient('/Users/dustin/development/php/adam2')

#print(r)

import pprint
pprint.pprint(r.info())

#r.checkout('/tmp/checkout_2')
#r.export('/tmp/export_1')

#l = svn.LocalClient('/Users/dustin/development/php/adam2')
