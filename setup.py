#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = [
    "markdown",
    "gitpython",
    "tinydb",
    "tinyrecord"
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='blogdown',
    version='0.0.1',
    description="the first ever blog thingy in historingy.",
    author="Rodrigo Palacios",
    author_email='rodrigopala91@gmail.com',
    url='https://github.com/rodricios/blogdown',
    packages=[
        'blogdown',
    ],
    package_dir={'blogdown':'blogdown'},
    package_data={'blogdown':['blogdown/template/*']},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='blogdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
