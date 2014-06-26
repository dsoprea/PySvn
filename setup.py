import os.path
import setuptools

import svn

app_path = os.path.dirname(svn.__file__)

with open(os.path.join(app_path, 'resources', 'README.rst')) as f:
      long_description = ''.join(f.readlines())

with open(os.path.join(app_path, 'resources', 'requirements.txt')) as f:
      install_requires = map(lambda s: s.strip(), f)

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
    packages=setuptools.find_packages(exclude=['test']),
    include_package_data=True,
    zip_safe=False,
    package_data={
        'svn': ['resources/README.rst',
                'resources/requirements.txt'],
    },
    install_requires=install_requires,
)
