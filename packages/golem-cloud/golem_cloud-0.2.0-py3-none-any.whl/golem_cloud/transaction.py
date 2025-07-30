"""
Tools to perform transactional operations using compensating actions.

Requires the following imports in the wit to work:
* import golem:api/host@1.1.7;
"""

from dataclasses import dataclass
from wit_world import types
from wit_world.types import Result, Ok
from wit_world.imports.host import set_oplog_index, get_oplog_index
from typing import Callable
from .host import atomic_operation_context


@dataclass
class Operation[In, Out, Err]:
    """
    An operation that can be executed as part of transaction. Consists of an action and a compensating action
    that can undo the side effects of the action.
    """

    _execute: Callable[[In], Result[Out, Err]]
    _compensate: Callable[[In, Out], Result[None, Err]]

    def execute(self, input: In) -> Result[Out, Err]:
        return self._execute(input)

    def compensate(self, input: In, result: Out) -> Result[None, Err]:
        return self._compensate(input, result)


def operation[In, Out, Err](
    execute: Callable[[In], Result[Out, Err]],
    compensate: Callable[[In, Out], Result[None, Err]],
) -> Operation[In, Out, Err]:
    """
    Create a new Operation from two functions.
    """
    return Operation(execute, compensate)


@dataclass
class FailedAndRolledBackCompletely[Err]:
    """
    The transaction has failed and all compensating actions have successfully completed.
    """

    error: Err


@dataclass
class FailedAndRolledBackPartially[Err]:
    """
    The transaction has failed and the compensating actions failed to complete.
    """

    error: Err
    compensation_failure: Err


type TransactionFailure[Err] = (
    FailedAndRolledBackCompletely[Err] | FailedAndRolledBackPartially[Err]
)

type TransactionResult[Out, Err] = Result[Out, TransactionFailure[Err]]


@dataclass
class FallibleTransaction[Err]:
    """
    Fallible transaction execution. If any operation fails, all the already executed
    successful operation's compensation actions are executed in reverse order and the transaction
    returns with a failure.
    """

    compensations: list[Callable[[], Result[None, Err]]]

    def execute[In, Out](
        self, op: Operation[In, Out, Err], input: In
    ) -> Result[Out, Err]:
        result = op.execute(input)
        if isinstance(result, Ok):
            self.compensations.append(lambda: op.compensate(input, result.value))
        return result

    def _on_failure(self, failure: Err) -> TransactionFailure[Err]:
        for compensation in self.compensations[::-1]:
            comp_result = compensation()
            if isinstance(comp_result, types.Err):
                return FailedAndRolledBackPartially(failure, comp_result.value)
        return FailedAndRolledBackCompletely(failure)


def fallible_transaction[Out, Err](
    f: Callable[[FallibleTransaction[Err]], Result[Out, Err]],
) -> TransactionResult[Out, Err]:
    """
    Execute a fallible transaction.
    """
    transaction = FallibleTransaction([])
    result = f(transaction)
    if isinstance(result, types.Err):
        return types.Err(transaction._on_failure(result.value))
    else:
        return result


@dataclass
class InfallibleTransaction:
    """
    Retry the transaction in case of failure. If any operation returns with a failure, all
    the already executed successful operation's compensation actions are executed in reverse order
    and the transaction gets retried, using Golem's active retry policy.
    """

    compensations: list[Callable[[], None]]
    begin_oplog_index: int

    def execute[In, Out, Err](self, op: Operation[In, Out, Err], input: In) -> Out:
        result = op.execute(input)
        if isinstance(result, Ok):

            def compensation() -> None:
                comp_result = op.compensate(input, result.value)
                if isinstance(comp_result, types.Err):
                    raise ValueError(
                        "Compensating actions are not allowed to fail in infallible transaction",
                        comp_result.value,
                    )
                self.compensations.append(compensation)

            return result.value
        else:
            self._retry()
            raise ValueError("unreachable")

    def _retry(self) -> None:
        # rollback all completed operations and try again
        for compensation in self.compensations[::-1]:
            compensation()
        set_oplog_index(self.begin_oplog_index)


def infallible_transaction[Out](f: Callable[[InfallibleTransaction], Out]) -> Out:
    """
    Execute an infallible transaction.
    """
    with atomic_operation_context():
        begin_oplog_index = get_oplog_index()
        transaction = InfallibleTransaction([], begin_oplog_index)
        return f(transaction)
