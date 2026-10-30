import os
from unittest.mock import Mock

import pytest
from django.db import IntegrityError, OperationalError, connection, transaction

from ticketing import conf
from ticketing.models import get_ticket, ticketing_models


@pytest.fixture
def manager():
    return ticketing_models[conf.DEFAULT_SEQUENCE].objects


@pytest.mark.django_db
def test_retries_once_after_operational_error(manager, monkeypatch):
    allocate = Mock(side_effect=[OperationalError("deadlock"), 42])
    monkeypatch.setattr(manager, "_internal_get_ticket", allocate)

    assert manager.get_ticket() == 42
    assert allocate.call_count == 2


@pytest.mark.django_db
def test_propagates_repeated_operational_error(manager, monkeypatch):
    allocate = Mock(side_effect=OperationalError("deadlock"))
    monkeypatch.setattr(manager, "_internal_get_ticket", allocate)

    with pytest.raises(OperationalError, match="deadlock"):
        manager.get_ticket()
    assert allocate.call_count == 2


@pytest.mark.django_db
def test_does_not_retry_unrelated_error(manager, monkeypatch):
    allocate = Mock(side_effect=IntegrityError("constraint violation"))
    monkeypatch.setattr(manager, "_internal_get_ticket", allocate)

    with pytest.raises(IntegrityError, match="constraint violation"):
        manager.get_ticket()
    assert allocate.call_count == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_retry_after_failed_sql_preserves_outer_transaction(manager):
    attempts = 0

    def fail_once(execute, sql, params, many, context):
        nonlocal attempts
        if sql.startswith("REPLACE INTO"):
            attempts += 1
            if attempts == 1:
                raise OperationalError("deadlock")
        return execute(sql, params, many, context)

    with transaction.atomic(), connection.execute_wrapper(fail_once):
        assert manager.get_ticket() > 0
        assert get_ticket() > 0

    assert attempts == 3
    assert get_ticket() > 0


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_retry_works_without_outer_transaction(manager):
    attempts = 0

    def fail_once(execute, sql, params, many, context):
        nonlocal attempts
        if sql.startswith("REPLACE INTO"):
            attempts += 1
            if attempts == 1:
                raise OperationalError("deadlock")
        return execute(sql, params, many, context)

    with connection.execute_wrapper(fail_once):
        assert manager.get_ticket() > 0

    assert attempts == 2


@pytest.mark.django_db
def test_only_latest_ticket_row_is_retained():
    tickets = [get_ticket() for _ in range(10)]
    model = ticketing_models[conf.DEFAULT_SEQUENCE]
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT id FROM {connection.ops.quote_name(model._meta.db_table)}"
        )
        rows = cursor.fetchall()

    assert list(rows) == [(tickets[-1],)]


@pytest.mark.django_db
@pytest.mark.skipif(connection.vendor != "mysql", reason="Requires a MySQL server")
def test_mysql_version_matches_tox_environment():
    assert connection.mysql_version >= (8, 4)
    requested = os.environ.get("TOX_ENV_NAME", "").partition("-mysql-")[2]
    if requested:
        assert connection.mysql_version[:2] == tuple(map(int, requested.split(".")))
