#! /usr/bin/env python
#
# Copyright (C) 2022 Autonomio

DESCRIPTION = 'Energy tracking for your machine learning experiments'
LONG_DESCRIPTION = '''\
EasyEnergy makes it easier to track energy usage for various machine learning
cycles, including model training, model inference and hyperparameter tuning.
'''

DISTNAME = 'easyenergy'
MAINTAINER = 'Mikko Kotila'
MAINTAINER_EMAIL = 'mailme@mikkokotila.com'
URL = 'http://autonom.io'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/autonomio/easyenergy/'

VERSION = '0.0.1'

try:
    from setuptools import setup

    _has_setuptools = True
except ImportError:
    from distutils.core import setup

install_requires = ['talos',
                    'numpy',
                    'pandas',
                    'tensorflow',
                    'scikit-learn']

if __name__ == '__main__':

    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=LICENSE,
        url=URL,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        install_requires=install_requires,
        packages=[
            'easyenergy'
        ],
        include_package_data=True,
        classifiers=[
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'License :: OSI Approved :: MIT License',
            'Topic :: Scientific/Engineering :: Human Machine Interfaces',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows :: Windows 10',
        ],
    )
