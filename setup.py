# !/usr/bin/env python

from navigation import __version__
from distutils.core import setup, find_packages


with open("README.md") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.md") as history_file:
    history = history_file.read()

setup(
    name='pynavigation',
    package=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={
        "navigation": "navigation"
    },
    py_modules=["sceptre"],
    version=__version__,
    description='A library that models units for navigation on Earth.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Niall Grant',
    license='Apache2',
    author_email='ngfgrant@gmail.com',
    url='https://github.com/ngfgrant/navigation',
    keywords=['navigation', 'waypoint', 'position', 'route',
              'latitude', 'longitude'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Navigation',
    ],
)
