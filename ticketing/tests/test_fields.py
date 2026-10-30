import pytest
from django.db import connection, models
from django.db.migrations.state import ModelState
from django.test.utils import isolate_apps

from ticketing import conf
from ticketing.fields import BigAutoField, TicketField
from ticketing.models import get_ticket


@pytest.fixture
def ticketed_model(django_db_reset_sequences):
    with isolate_apps():

        class Ticketed(models.Model):
            ticket = TicketField(sequence="test")

            class Meta:
                app_label = "ticketing"

        with connection.schema_editor() as editor:
            editor.create_model(Ticketed)
        try:
            yield Ticketed
        finally:
            with connection.schema_editor() as editor:
                editor.delete_model(Ticketed)


def test_ticket_field_generates_from_requested_sequence(ticketed_model):
    instance = ticketed_model.objects.create()

    instance.refresh_from_db()
    assert instance.ticket > 0
    assert get_ticket("test") == instance.ticket + 1
    assert get_ticket(conf.DEFAULT_SEQUENCE) == 1


def test_ticket_field_preserves_explicit_value(ticketed_model):
    instance = ticketed_model.objects.create(ticket=123)

    instance.refresh_from_db()
    assert instance.ticket == 123
    assert get_ticket("test") == 1


def test_ticket_field_preserves_value_when_saved_again(ticketed_model):
    instance = ticketed_model.objects.create()
    ticket = instance.ticket

    instance.save()
    instance.refresh_from_db()

    assert instance.ticket == ticket
    assert get_ticket("test") == ticket + 1


@pytest.mark.parametrize("sequence", conf.SEQUENCES)
def test_migration_state_preserves_ticket_field_sequence(sequence):
    with isolate_apps():

        class Ticketed(models.Model):
            ticket = TicketField(sequence=sequence)

            class Meta:
                app_label = "ticketing"

        state = ModelState.from_model(Ticketed)

    assert state.fields["ticket"].sequence == sequence
    assert state.fields["ticket"].editable is False


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_big_auto_field_exceeds_32_bits():
    from ticketing.models import ticketing_models

    model = ticketing_models[conf.DEFAULT_SEQUENCE]
    assert isinstance(model._meta.pk, BigAutoField)
    large_id = 2**32
    with connection.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {connection.ops.quote_name(model._meta.db_table)} "
            "(id, stub) VALUES (%s, %s)",
            [large_id, model.STUB_DEFAULT],
        )

    assert get_ticket() > large_id
