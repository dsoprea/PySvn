from setuptools import setup, find_packages
import sys, os

#import versioneer
#versioneer.VCS = 'git'
#versioneer.versionfile_source = 'svn/_version.py'
#versioneer.versionfile_build = 'svn/_version.py'
#versioneer.tag_prefix = ''
#versioneer.parentdir_prefix = 'svn-'

setup(name='svn',
      version='0.3.14',#versioneer.get_version(),
      description="Straight-forward Subversion wrapper.",
      long_description="""""",
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Software Development :: Version Control'],
      keywords='svn subversion',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://github.com/dsoprea/PySvn',
      license='GPL 2',
      packages=find_packages(exclude=['test']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
#      cmdclass=versioneer.get_cmdclass(),
)
