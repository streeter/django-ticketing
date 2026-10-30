import pytest

from ticketing import conf
from ticketing.exceptions import BadSequenceName
from ticketing.models import get_ticket, ticketing_models

pytestmark = pytest.mark.django_db


def test_get_ticket():
    assert get_ticket() > 0


def test_get_tickets():
    first = get_ticket()
    second = get_ticket()

    assert 0 < first < second


def test_get_n_tickets():
    tickets = [get_ticket() for _ in range(200)]

    assert tickets[0] > 0
    assert all(first < second for first, second in zip(tickets, tickets[1:]))


@pytest.mark.parametrize("sequence", conf.SEQUENCES)
def test_get_from_sequence(sequence):
    tickets = [get_ticket(sequence) for _ in range(10)]

    assert tickets[0] > 0
    assert all(first < second for first, second in zip(tickets, tickets[1:]))


def test_get_sequences_in_order():
    assert len(conf.SEQUENCES) > 1
    for expected in range(1, 10):
        for sequence in conf.SEQUENCES:
            assert get_ticket(sequence) == expected


def test_bad_sequence():
    with pytest.raises(BadSequenceName, match="bad_sequence"):
        get_ticket("bad_sequence")


def test_default_sequence():
    assert get_ticket() == 1
    assert get_ticket(conf.DEFAULT_SEQUENCE) == 2


def test_ticket_model_string():
    ticket = ticketing_models[conf.DEFAULT_SEQUENCE].objects.create()

    assert ticket.ticket == ticket.pk
    assert str(ticket) == f"Ticket {ticket.pk}"
