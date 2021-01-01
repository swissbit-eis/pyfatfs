#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""pyFAT package definition."""

import io
import re

from setuptools import setup, find_packages

SEMVER_REGEX = r'^(?P<major>0|[1-9]\d*)\.' \
               r'(?P<minor>0|[1-9]\d*)\.' \
               r'(?P<patch>0|[1-9]\d*)' \
               r'(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)' \
               r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))' \
               r'?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'

try:
    # pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # pip <= 9.0.3
    from pip.req import parse_requirements


def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [getattr(r, 'requirement',
            str(getattr(r, 'req', None))) for r in reqs]


def _get_attribute(name):
    """Get version information from __init__.py."""
    with io.open('pyfatfs/__init__.py') as f:
        return re.search(r"{}\s*=\s*'([^']+)'\s*".format(name),
                         f.read()).group(1)


def _get_copyright():
    """Get copyright holders and year information from license."""
    with io.open('LICENSE') as f:
        return re.search(r"^Copyright \(c\) (.*)$", f.read(),
                         flags=re.MULTILINE).group(1)


def _get_major_minor():
    """Get release (major.minor)."""
    version = _get_attribute('__version__')
    return '.'.join(re.search(SEMVER_REGEX, version).group("major", "minor"))


def _get_readme():
    """Get contents of README.rst."""
    with io.open('README.rst') as readme:
        return readme.read()


setup(name=_get_attribute('__name__'),
      version=_get_attribute('__version__'),
      description='FAT12/16/32 implementation with VFAT support',
      long_description=_get_readme(),
      long_description_content_type='text/x-rst',
      author=_get_attribute('__author__'),
      author_email=_get_attribute('__author_email__'),
      license=_get_attribute('__license__'),
      url='https://github.com/nathanhi/pyfat',
      packages=find_packages(),
      keywords=['filesystem', 'PyFilesystem2', 'FAT12',
                'FAT16', 'FAT32', 'VFAT', 'LFN'],
      python_requires='~=3.6',
      test_suite='tests',
      install_requires=load_requirements("requirements/install.txt"),
      setup_requires=['pytest-runner'],
      tests_require=load_requirements("requirements/test.txt"),
      entry_points={
          'fs.opener': ['fat = pyfatfs.PyFatFSOpener:PyFatFSOpener'],
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Filesystems'],
      command_options={
        'build_sphinx': {
            'project': ('setup.py', _get_attribute('__name__')),
            'version': ('setup.py', _get_major_minor()),
            'release': ('setup.py', _get_attribute('__version__')),
            'copyright': ('setup.py', _get_copyright()),
            'source_dir': ('setup.py', 'docs')}},
      )
