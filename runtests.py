#!/usr/bin/env python
import sys
from os.path import dirname, abspath, join

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'NAME': 'ticketing_test',
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        
        # Uncomment below to run tests with mysql
        #DATABASES={
        #    'default': {
        #        'NAME': 'ticketing_test',
        #        'ENGINE': 'django.db.backends.mysql',
        #        'USER': 'ticketing_test',
        #        'HOST': '/var/mysql/mysql.sock',
        #    }
        #},
        
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django.contrib.sites',
            
            # Included to fix Disqus' test Django which solves IntegrityMessage case
            'django.contrib.contenttypes',
            'ticketing',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
        TICKETING_TESTING=True,
    )


def runtests(*test_args):
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()
    
    if not test_args:
        test_args = ['ticketing']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    
    test_runner = TestRunner(verbosity=0, interactive=True, failfast=True)
    failures = test_runner.run_tests(test_args)
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests(*sys.argv[1:])