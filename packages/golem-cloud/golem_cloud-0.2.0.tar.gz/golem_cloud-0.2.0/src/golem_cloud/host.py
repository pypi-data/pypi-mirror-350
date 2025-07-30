"""
Host functions to control various behaviours of the golem runtime.

Requires the following imports in the wit to work:
* import golem:api/host@1.1.7;
"""

from wit_world.imports.host import (
    mark_begin_operation,
    mark_end_operation,
    RetryPolicy,
    get_retry_policy,
    set_retry_policy,
    get_idempotence_mode,
    set_idempotence_mode,
    PersistenceLevel,
    get_oplog_persistence_level,
    set_oplog_persistence_level,
)
from contextlib import contextmanager


@contextmanager
def atomic_operation_context():
    """
    Marks a block as an atomic operation

    When the context is exited, the operation gets committed.
    If the context exits with an error, the whole operation will be re-executed during retry
    """
    begin_index = mark_begin_operation()
    yield
    mark_end_operation(begin_index)


@contextmanager
def use_retry_policy(policy: RetryPolicy):
    """
    Temporarily sets the retry policy to the given value.

    When the context is exited, the original retry policy is restored
    """
    original = get_retry_policy()
    set_retry_policy(policy)
    try:
        yield
    finally:
        set_retry_policy(original)


@contextmanager
def use_idempotence_mode(value: bool):
    """
    Temporarily sets the idempotence mode to the given value.

    When the context is exited, the original idempotence mode is restored.
    """
    original = get_idempotence_mode()
    set_idempotence_mode(value)
    try:
        yield
    finally:
        set_idempotence_mode(original)


@contextmanager
def use_persistence_level(value: PersistenceLevel):
    """
    Temporarily sets the oplog persistence level to the given value.

    When the context is exited, the original persistence level is restored.
    """
    original = get_oplog_persistence_level()
    set_oplog_persistence_level(value)
    try:
        yield
    finally:
        set_oplog_persistence_level(original)
