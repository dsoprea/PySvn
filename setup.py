from setuptools import setup, find_packages
import sys, os

setup(name='svn',
      version='0.1.0',
      description="Straight-forward Subversion wrapper.",
      long_description="""""",
      classifiers=[],
      keywords='svn subversion',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='',
      license='GPL 2',
      packages=find_packages(exclude=['test']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      entry_points="""""",
)
