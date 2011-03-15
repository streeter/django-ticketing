from ticketing import conf
from django.db import models

class TicketingManager(models.Manager):
    
    def create(self):
        id = self.get_ticket()
        return super(TicketingManager, self).get_query_set().get(pk=id)
    
    def get_query_set(self):
        raise NotImplementedError()
    
    def get_empty_query_set(self):
        raise NotImplementedError()
    
    def get_ticket(self):
        from django.db import connections, transaction
        cursor = connections[self.db].cursor()
        
        sql = "REPLACE INTO `%s` " % (self.model._meta.db_table)
        sql += "(`stub`) VALUES (%s)"
        
        result = cursor.execute(sql, [True])
        transaction.commit_unless_managed(using=self.db)
        if hasattr(cursor, 'lastrowid') and cursor.lastrowid:
            return cursor.lastrowid
        else:
            # Hack. Select the row and get the id manually
            object = super(TicketingManager, self).get_query_set()\
                .filter(stub=True)[0]
            return object.id
    
