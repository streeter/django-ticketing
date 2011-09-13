"""
Ticketing
~~~~~~~~~
"""

import pkg_resources

VERSION = tuple(map(int, pkg_resources.get_distribution('ticketing').version.split('.')))
__version__ = VERSION
