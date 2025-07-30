"""
Durability tools for implementing custom durable functions.

Requires the following imports in the wit to work:
* import golem:rpc/types@0.2.3;
* import golem:api/host@1.1.7;
* import golem:api/oplog@1.1.7;
* import golem:durability/durability@1.2.1;
"""

from wit_world.imports import oplog as host_oplog
from wit_world.imports import durability as host_durability
from wit_world.imports import host
from wit_world.imports.golem_rpc_types import ValueAndType

class Durability:
    def __init__(
        self,
        interface: str,
        function: str,
        function_type: host_oplog.WrappedFunctionType,
    ) -> None:
        self.interface = interface
        self.function = function
        self.function_type = function_type
        self.forced_commit = False

        self.begin_index = host_durability.begin_durable_function(self.function_type)
        self.durable_execution_state = host_durability.current_durable_execution_state()

    def enable_forced_commit(self) -> None:
        self.forced_commit = True

    def is_live(self) -> bool:
        return self.durable_execution_state.is_live or isinstance(
            self.durable_execution_state.persistence_level,
            host.PersistenceLevel_PersistNothing,
        )

    def persist(self, input: ValueAndType, result: ValueAndType) -> None:
        if not isinstance(
            self.durable_execution_state.persistence_level,
            host.PersistenceLevel_PersistNothing,
        ):
            host_durability.persist_typed_durable_function_invocation(
                function_name=self._function_name(),
                request=input,
                response=result,
                function_type=self.function_type,
            )
            host_durability.end_durable_function(
                self.function_type, self.begin_index, self.forced_commit
            )

    def replay(self) -> tuple[ValueAndType, host_durability.OplogEntryVersion]:
        oplog_entry = host_durability.read_persisted_typed_durable_function_invocation()
        validate_oplog_entry(oplog_entry, self._function_name())
        host_durability.end_durable_function(
            self.function_type, self.begin_index, False
        )

        return (oplog_entry.response, oplog_entry.entry_version)

    def _function_name(self) -> str:
        if self.interface == "":
            # For backward compatibility - some of the recorded function names were not following the pattern
            return self.function
        else:
            return f"{self.interface}:{self.function}"


def validate_oplog_entry(
    oplog_entry: host_durability.PersistedTypedDurableFunctionInvocation,
    expected_function_name: str,
) -> None:
    if oplog_entry.function_name != expected_function_name:
        raise ValueError(
            f"Unexpected imported function call entry in oplog: expected {expected_function_name}, got {oplog_entry.function_name}"
        )
