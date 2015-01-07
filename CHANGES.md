Changelog
---------

# 0.7.3

* TicketField will only generate a new ticket value when the field value is None (potentially breaking change)

# 0.7.2

* Ensure that we only try to set the rollback status if the connection
is inside of an atomic block.


# 0.7.1

* Fixes [#6](https://github.com/streeter/django-ticketing/issues/6) by marking
the database as not needing a rollback after catching an exception to retry
generating a ticket.


# 0.7.0

* Requires Django 1.6 or higher
* Adds a single retry to generating a ticket in the case of a database
`OperationError` (ie. deadlock).


# 0.6.3

* Update the package system and improve setup.py


# 0.6.2

* Change how version is being stored.


# 0.6.1

* Fix some typos in the README. Thanks [blueyed](https://github.com/blueyed)!


# 0.6.0

* Fix calling of parent methods in fields.


# 0.5.1

* TODO


# 0.5.0

* Fixed a race condition in TicketManager.create() I wanted to emulate the
default behavior and return a Ticket instance, but I was doing so by executing
a second get query to get the object with that new ticket id. But that object
isn't guaranteed to exist!


# 0.4.0

* Add TicketField, which allows one to use a ticket as a field in other classes.


# 0.3.0

* Added BigAutoField, which allows for extra large tickets on MySQL backends


# 0.2.1

* Updated README


# 0.2.0

* Added support for multiple sequences


# 0.1.0
* Initial implementation
