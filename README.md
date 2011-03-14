## About
An implementation of a Django model that returns tickets, as described
by the [Flickr blog post][flickr].


## Testing

There are some tests included. To run those tests, simply execute `runtests.py`:

    [streeter] $ python runtests.py
    ----------------------------------------------------------------------
    Ran 5 tests in 0.341s
    
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
