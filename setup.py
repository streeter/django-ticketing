#!/usr/bin/env python

import os
import sys

import ticketing

try:
    from setuptools import setup
    from setuptools.command.test import test
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
    from setuptools.command.test import test


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


packages = [
    'ticketing',
]

requires = [
]


class mytest(test):
    def run(self, *args, **kwargs):
        from runtests import runtests
        runtests()
        # Upgrade().run(dist=True)
        # test.run(self, *args, **kwargs)

setup(
    name='django-ticketing',
    version=ticketing.__version__,
    author='Chris Streeter',
    author_email='pypi@chrisstreeter.com',
    url='http://github.com/streeter/django-ticketing',
    description='Generate tickets efficiently in a database in Django',
    packages=packages,
    license=open('LICENSE').read(),
    zip_safe=False,
    install_requires=requires,
    test_suite='ticketing.tests',
    include_package_data=True,
    cmdclass={"test": mytest},
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development'
    ],
)
