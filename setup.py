#!/usr/bin/env python

'''
wind Docker management utility

Installs a python package called "windutil" and places
a generated script in the user's path called "wutil".

Run "wutil init" to create a ~/.wutilrc file and add your image and
container information.  "wuitl -h" for help.
'''

from setuptools import setup

setup(
    name="windutil",
    version="1.0.8",
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'wutil=windutil.main:main',
        ],
    },
    packages=['windutil'],
    author="Amaret, Inc",
    author_email="develop@amaret.com",
    description=("A command-line utility to manage the docker containers "
                 "of the Wind application."),
    license="APACHE2",
    keywords="python docker",
    url="https://github.com/amaret/wind.util",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Topic :: Software Development :: Compilers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
)
