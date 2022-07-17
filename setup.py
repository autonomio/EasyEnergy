#! /usr/bin/env python
#
# Copyright (C) 2022 Autonomio
import setuptools


DESCRIPTION = 'Energy tracking for your machine learning experiments'
LONG_DESCRIPTION = '''\
EasyEnergy makes it easier to track energy usage for various machine learning
cycles, including model training, model inference and hyperparameter tuning.
'''

DISTNAME = 'EasyEnergy'
MAINTAINER = 'Mikko Kotila'
MAINTAINER_EMAIL = 'mailme@mikkokotila.com'
URL = 'http://autonom.io'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/autonomio/EasyEnergy/'

VERSION = '0.0.1'


install_requires = ['talos',
                    'numpy',
                    'pandas',
                    'tensorflow',
                    'scikit-learn']


setuptools.setup(
    name=DISTNAME,
    version=VERSION,
    author=MAINTAINER,
    author_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url=DOWNLOAD_URL,
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    include_package_data=True
)
