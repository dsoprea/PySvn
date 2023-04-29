#!/usr/bin/env python2.7

from __future__ import print_function          # PY3

import sys
import os
import os.path
from pprint import pprint

import svn
from svn.exception import SvnException
from svn.test_support import temp_repo, temp_checkout, populate_prop_files


def cont(conttext='continue'):
    try:
        ctext=raw_input('  ENTER to %s:' % conttext)
    except: # PY3
        ctext=input('  ENTER to %s:' % conttext)
    return ctext


tempdir = os.environ.get('TEMPDIR',os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../temp')))

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


with temp_repo() as (repo_path, _):
    print('Temp repo created at %s' % repo_path)
    
    with temp_checkout() as (wcpath, lc):
        print('Working Copy created at %s' % wcpath)

        populate_prop_files()
        lc.commit("Second revision.")
    
        lc.propset('svn:mime-type','image/jpeg', rel_path='foo.jpg')
        lc.propset('owner','sally', rel_path='foo.bar')
        lc.propset('svn:ignore','foo.bak') # set on directory level

        print('\n--- info for foo.bar ---')
        pprint(lc.info('foo.bar'))
        
        pprint(lc.properties('foo.bar'))

        print('\n--- info for foo.jpg ---')
        pprint(lc.info('foo.jpg'))
        pprint(lc.properties('foo.jpg'))

        cont('before committing properties')
        lc.commit('Committing properties')
        lc.update()

        print('\npropget for foo.jpg for svn:mime-type:', lc.propget('svn:mime-type', rel_path='foo.jpg'))

        print('\n--- info for foo.bar after setting properties owner svn:ignore & commit---')
        pprint(lc.info('foo.bar'))
        cont()

        lc.propset('svn:keywords','Author Date Rev', rel_path='foo.bar')

        print('\n--- info and properties for foo.bar ---')
        pprint(lc.info('foo.bar'))
        pprint(lc.properties(rel_path='foo.bar'))

        lc.propdel('owner', rel_path='foo.bar')

        lc.commit('Committing after deleting property')
        lc.update()
        cont()

        print('\nget property svn:ignore on . =', lc.propget('svn:ignore','.') )

        print('--- properties for foo.bar HEAD ---')
        pprint(lc.properties(rel_path='foo.bar'))

        print('info on foo.bar')
        pprint(lc.info(rel_path='foo.bar'))

        print('\n--- properties for foo.bar rev 1 ---')
        pprint(lc.properties(rel_path='foo.bar',revision=1))
        print('properties for foo.bar rev 2:')
        pprint(lc.properties(rel_path='foo.bar',revision=2))
        print('\n--- properties for foo.bar rev 3 ---')
        pprint(lc.properties(rel_path='foo.bar',revision=3))
                
#with self.assertRaises(Exception): # svn.exception.SvnException):
#    lc.propget('owner', rel_path='foo.bar')
# self.assertRaises(Exception, lc.propget,'owner', rel_path='foo.bar')

        try:
            lc.propget('owner', rel_path='foo.bar')
        except SvnException as sx:
            pass
                        
        print(lc.properties(rel_path='foo.bar'))
        
        cont('end of script')

