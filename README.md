## About

An implementation of a Django model that returns tickets, as described
by the [Flickr blog post][flickr].

## Installation

I uploaded it to [PyPi][pypi], so you can grab it there if you'd like with

    pip install django-ticketing

or install with pip the git address:

    pip install git+git@github.com:streeter/django-ticketing.git

You're choice. Then add `ticketing` to your `INSTALLED_APPS`.

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

### Multiple Sequences

`django-ticketing` also supports multiple sequences, which allows one to have
sequences of tickets that are independent. This means you could have a sequence
for users, a sequence for posts and a sequence for widgets. This is configured
through your Django settings configuration.

Simply define a setting called `TICKETING_SEQUENCES` with a tuple of sequence
names that can be valid table names. This defaults to the tuple `('default',)`.
In addition, you can define the default sequence new tickets are taken from with
the setting `TICKETING_DEFAULT_SEQUENCE`, which defaults to `'default'`.

Note that `TICKETING_DEFAULT_SEQUENCE` must a sequence name that is defined
inside of `TICKETING_SEQUENCES`, otherwise an exception will be raised at
during setup.

So to have sequences for the above example, put the following lines in your
`settings.py`:

    TICKETING_DEFAULT_SEQUENCE = 'users'
    TICKETING_SEQUENCES = ('users', 'posts', 'widgets', )

Then, to get a ticket from a specific sequence, pass in the sequence name to
`get_ticket()`:

    # Get yourself a user ticket
    user_ticket = get_ticket('users')
    # Get yourself another user ticket
    user_ticket = get_ticket()
    # Get yourself a posts ticket
    post_ticket = get_ticket('posts')

Notice that the default sequence for `get_ticket()` is the value of the
`TICKETING_DEFAULT_SEQUENCE` configuration variable.

Also, after you change the value of `TICKETING_SEQUENCES`, be sure to re-run
`syncdb` to make sure the new tables are created (or whatever DB table creation
you have in your environment).

### Other Configuration Options

`TICKETING_APP_LABEL`: This is used to specify the prefix for all the DB
tablenames. The default value is `'ticketing'`. Be sure you know what you are
doing when you change this.


## Testing

There are some tests included. To run those tests, simply execute `runtests.py`:

    [streeter] $ python runtests.py
    ----------------------------------------------------------------------
    Ran 6 tests in 0.213s
    
    OK
    [streeter] $

The test suite can run on all DB backends supported by Django. By default
it runs using sqlite3. To run on MySQL, uncomment the section in `runtests.py`
and then create a DB that Django can connect to, and give the Django user
permissions to create a new testing DB, run the following commands:

    mysql -u root -e "DROP DATABASE ticketing_test";
    mysql -u root -e "CREATE DATABASE ticketing_test";
    mysql -u root -e "GRANT ALL ON ticketing_test.* TO 'ticketing_test'@'localhost' IDENTIFIED BY ''"

Of course, you may need to change the host of the DB and user that connects, but
you should get the idea.

[flickr]: http://code.flickr.com/blog/2010/02/08/ticket-servers-distributed-unique-primary-keys-on-the-cheap/
[pypi]: http://pypi.python.org/pypi/django-ticketing/
[south]: http://south.aeracode.org/
