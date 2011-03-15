"""
Ticketing
~~~~~~~~~
"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('django-ticketing').version
except Exception, e:
    VERSION = 'unknown'
