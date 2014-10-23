from django.db import connections, models, OperationalError, transaction
exceptions = (OperationalError, )
try:
    # Also try to catch a MySQLdb-specific OperationalError
    from MySQLdb import OperationalError as MySQLOperationalError
    exceptions += (MySQLOperationalError, )
except ImportError:
    pass


class TicketingManager(models.Manager):

    def create(self):
        ticket_id = self.get_ticket()
        return self.model(id=ticket_id, stub=self.model.STUB_DEFAULT)

    def get_query_set(self):
        raise NotImplementedError()

    def get_empty_query_set(self):
        raise NotImplementedError()

    def _internal_get_ticket(self):
        sql = "REPLACE INTO `%s` " % (self.model._meta.db_table)
        sql += "(`stub`) VALUES (%s)"

        with transaction.atomic(using=self.db):
            cursor = connections[self.db].cursor()
            cursor.execute(sql, [self.model.STUB_DEFAULT])

            lastrow_id = getattr(cursor, 'lastrowid', None)
            if lastrow_id is None:
                # Hack. Select the row and get the id manually
                result = super(TicketingManager, self).get_query_set().filter(
                    stub=True)[0]
                lastrow_id = result.id

            return lastrow_id

    def get_ticket(self):
        try:
            return self._internal_get_ticket()
        except exceptions:
            connection = connections[self.db]
            # If the transaction is in an `atomic` block, and needs a rollback,
            # we should mark the database as rolled back. This is because the
            # database backend may not prevent running SQL queries in broken
            # transactions, in which case we need to say that we have handled
            # the rollback so we can try one more time.
            if (connection.in_atomic_block
                    and transaction.get_rollback(using=self.db)):
                transaction.set_rollback(False, using=self.db)
            return self._internal_get_ticket()
