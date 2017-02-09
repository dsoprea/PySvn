import os.path
import setuptools

import svn

_APP_PATH = os.path.dirname(svn.__file__)

with open(os.path.join(_APP_PATH, 'resources', 'README.rst')) as f:
    long_description = f.read()

with open(os.path.join(_APP_PATH, 'resources', 'requirements.txt')) as f:
    install_requires = list(map(lambda s: s.strip(), f.readlines()))

setuptools.setup(
    name='svn',
    version=svn.__version__,
    description="Intuitive Subversion wrapper.",
    long_description=long_description,
    classifiers=[],
    keywords='svn subversion',
    author='Dustin Oprea',
    author_email='myselfasunder@gmail.com',
    url='https://github.com/dsoprea/PySvn',
    license='GPL 2',
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    package_data={
        'svn': ['resources/README.rst',
                'resources/requirements.txt'],
    },
    install_requires=install_requires,
)
