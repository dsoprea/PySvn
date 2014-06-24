import setuptools

long_description = ""

setuptools.setup(
    name='svn',
    version='0.3.16',
    description="Straight-forward Subversion wrapper.",
    long_description=long_description,
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Topic :: Software Development :: Version Control'],
    keywords='svn subversion',
    author='Dustin Oprea',
    author_email='myselfasunder@gmail.com',
    url='https://github.com/dsoprea/PySvn',
    license='GPL 2',
    packages=setuptools.find_packages(exclude=['test']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'python-dateutil==2.2',
    ],
)
