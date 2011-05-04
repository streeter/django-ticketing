#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
    from setuptools.command.test import test
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    from setuptools.command.test import test


class mytest(test):
    def run(self, *args, **kwargs):
        from runtests import runtests
        runtests()
        # Upgrade().run(dist=True)
        # test.run(self, *args, **kwargs)

setup(
    name='django-ticketing',
    version='0.6.1',
    author='Chris Streeter',
    author_email='pypi@chrisstreeter.com',
    url='http://github.com/streeter/django-ticketing',
    description = 'Generate tickets efficiently in a database in Django',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
    ],
    test_suite = 'ticketing.tests',
    include_package_data=True,
    cmdclass={"test": mytest},
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
