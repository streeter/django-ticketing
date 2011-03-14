from django.db import models
from ticketing.managers import TicketingManager

class Ticketing(models.Model):
    """
    The model that represents a ticket instance.
    
    """
    
    # Explicitly set the id of the model, even though it is the same
    # as the one Django gives it.
    id = models.AutoField(null=False, primary_key=True)
    
    # This is just the smallest placeholder we can create that we can
    # replace into to generate a new id.
    stub = models.BooleanField(null=False, default=True, unique=True)
    
    # Override the default manager
    objects = TicketingManager()
    
    @property
    def ticket(self):
        return self.id
    
    def __unicode__(self):
        return u'Ticket %d' % self.ticket
    
    def __str__(self):
        return str(unicode(self))

def get_ticket():
    ticket = Ticketing.objects.create()
    return ticket.ticket