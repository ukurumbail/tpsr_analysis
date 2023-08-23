#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = [ ]

setup(
    author="Unni Kurumbail",
    author_email='ukurumbail@wisc.edu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Small set of scripts to collate and process TPSR data from the Hermans DRIFTS computer.",
    entry_points={
        'console_scripts': [
            'tpsr_analysis=tpsr_analysis.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='tpsr_analysis',
    name='tpsr_analysis',
    packages=find_packages(include=['tpsr_analysis', 'tpsr_analysis.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ukurumbail/tpsr_analysis',
    version='0.1.0',
    zip_safe=False,
)
