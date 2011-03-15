from ticketing import conf
from django.db import models
from django.db.models.signals import post_syncdb
from ticketing.managers import TicketingManager

# Container for all the ticketing models
ticketing_models = {}

class BaseTicketing(models.Model):
    """
    The base class used by all Ticket generator models.
    
    Define the fields, methods and manager used by all
    classes that will inherit from this abstract model.
    All ticketing models that are created for each
    sequence defined in the configuration will inherit
    these properties.
    
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
        """Alias for id"""
        return self.id
    
    def __unicode__(self):
        return u'Ticket %d' % self.ticket
    
    def __str__(self):
        return str(unicode(self))
    
    class Meta:
        abstract = True

# Create each model for the ones defined in the configuration
for seq in conf.SEQUENCES:
    class Meta:
        pass
    
    # Set the application label
    setattr(Meta, 'app_label', conf.APP_LABEL)
    
    # __module__ is used with app_label to create the name of the table.
    # In addition, we want to have a Meta class so that the Django code
    # will work properly.
    attrs = {
        '__module__': seq,
        'Meta': Meta,
    }
    
    # Create the model definition
    model = type(seq, (BaseTicketing,), attrs)
    
    # Save the definition in a variable that we can use later. This will
    # also let Django find this model with some python dict traversal
    # goodness.
    ticketing_models[seq] = model

def get_ticket(sequence=conf.DEFAULT_SEQUENCE):
    """
    Get a ticket for the specified sequence.
    
    `sequence` defaults to the configuration parameter DEFAULT_SEQUENCE
    
    """
    if sequence not in ticketing_models:
        msg = "Sequence '%s' is not one of the configured sequences %s" % (
            sequence, conf.SEQUENCES
        )
        from ticketing.exceptions import BadSequenceName
        raise BadSequenceName(msg)
    ticket = ticketing_models[sequence].objects.create()
    return ticket.ticket
