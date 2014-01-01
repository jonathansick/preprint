#!/usr/bin/env python

PROJECT = 'preprint'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Tools for writing latex papers',
    long_description=long_description,

    author='Jonathan Sick',
    author_email='jonathansick@mac.com',

    url='http://jonathansick.ca',
    download_url='',

    classifiers=['Development Status :: 3 - Alpha',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'preprint = preprint.main:main'
        ],
        'preprint.commands': [
            'simple = preprint.simple:Simple',
            'two_part = preprint.simple:Simple',
            'error = preprint.simple:Error',
        ],
    },

    zip_safe=False,
)
