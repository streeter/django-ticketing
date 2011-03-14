## About

An implementation of a Django model that returns tickets, as described
by the [Flickr blog post][flickr].

## Installation

I uploaded it to [PyPi][pypi], so you can grab it there if you'd like with

    pip install django-ticketing

or install with pip the git address:

    pip install git+git@github.com:streeter/django-ticketing.git

You're choice.

## Usage

To use this, you can either use the model interface, or just the shortcut
function defined in `ticketing.models`. That usage looks like the following:

    # Import the function
    from ticketing.models import get_ticket
    # Go get yourself a ticket
    ticket = get_ticket()
    # Boom. That just happened

This assumes you've had the single table that needs to be created in the DB,
in other words, run `syncdb` or migrated with [South][south].

## Testing

There are some tests included. To run those tests, simply execute `runtests.py`:

    [streeter] $ python runtests.py
    ----------------------------------------------------------------------
    Ran 7 tests in 0.441s
    
    OK
    [streeter] $

The test suite can run on all DB backends supported by Django. By default
it runs using sqlite3. To run on MySQL, uncomment the section in `runtests.py`
and then create a DB that Django can connect to, and give the Django user
permissions to create a new testing DB, run the following commands:

    mysql -h localhost -u root -e "DROP DATABASE ticketing_test";
    mysql -h localhost -u root -e "CREATE DATABASE ticketing_test";
    mysql -h localhost -u root -e "GRANT ALL ON ticketing_test.* TO 'ticketing_test'@'localhost' IDENTIFIED BY ''"

Of course, you may need to change the host of the DB and user that connects, but
you should get the idea.

[flickr]: http://code.flickr.com/blog/2010/02/08/ticket-servers-distributed-unique-primary-keys-on-the-cheap/
[pypi]: http://pypi.python.org/pypi/django-ticketing/0.1.0
[south]: http://south.aeracode.org/