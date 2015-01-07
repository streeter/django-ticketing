from ticketing import conf
from django.db import models


def _conn_is_mysql(connection):
    return (bool(connection) and
            connection.settings_dict['ENGINE'] == 'django.db.backends.mysql')


class BigAutoField(models.AutoField):

    def db_type(self, connection):
        if _conn_is_mysql(connection):
            return 'bigint UNSIGNED AUTO_INCREMENT'
        else:
            return super(BigAutoField, self).db_type(connection)


class TicketField(models.BigIntegerField):

    description = "A big integer pre-populated from a ticket"

    def __init__(self, sequence=None, **kwargs):
        """
        Set up this field with the name of the sequence to use
        """
        self.sequence = sequence or conf.DEFAULT_SEQUENCE
        kwargs['editable'] = False
        super(TicketField, self).__init__(**kwargs)

    def pre_save(self, model_instance, add):
        """
        When saving the DB, if we are adding this instance, get a ticket
        value for this field. Otherwise pull it from the model instance.
        If the field on the instance already has a value, we won't
        a new ticketing value.
        """
        if add and not getattr(model_instance, self.attname):
            from ticketing.models import get_ticket
            value = get_ticket(self.sequence)
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(TicketField, self).pre_save(model_instance, add)

    def db_type(self, connection):
        if _conn_is_mysql(connection):
            return 'bigint UNSIGNED'
        else:
            return super(TicketField, self).db_type(connection)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = 'ticketing.fields.TicketField'
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(rules=[
        (
            [TicketField],  # Class(es) these apply to
            [],             # Positional arguments (not used)
            {               # Keyword argument
                "sequence": ["sequence", {"default": None}],
            },
        ),
    ], patterns=["^ticketing\.fields\.TicketField"])
except ImportError:
    pass
