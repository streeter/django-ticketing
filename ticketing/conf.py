from django.conf import settings

# Testing and Debug settings
TESTING = getattr(settings, 'TICKETING_TESTING', False)
DEBUG = getattr(settings, 'DEBUG', False) and not TESTING

# Let the user redefine the APP_LABEL, which is used for the table
# prefixes.
APP_LABEL = getattr(settings, 'TICKETING_APP_LABEL', 'ticketing')

# A list of names that define all the different ticketing tables. Every
# sequence is a sequence of tickets that can be retreived.
SEQUENCES = getattr(settings, 'TICKETING_SEQUENCES', ('default', ))

# When testing, add a second sequence so we can test specifying sequences
if TESTING:
    SEQUENCES = SEQUENCES + ('test', )

# The name of the default sequence that is queried when creating tickets.
DEFAULT_SEQUENCE = getattr(settings, 'TICKETING_DEFAULT_SEQUENCE', 'default')

if DEFAULT_SEQUENCE not in SEQUENCES:
    msg = ("Cannot specify a default sequence '%s' that " +
        "is not in the list of allowed sequences %s") % (
        DEFAULT_SEQUENCE, str(SEQUENCES)
    )
    from ticketing.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(msg)

