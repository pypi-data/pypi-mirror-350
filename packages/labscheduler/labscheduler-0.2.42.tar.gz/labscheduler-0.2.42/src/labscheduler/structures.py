"""
Here we define the structures of a process, a scheduling instance etc.
"""

from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import NamedTuple

import networkx as nx

from labscheduler.logging_manager import scheduler_logger as logger


@dataclass
class Machine:
    """Container for a machine.

    Args:
        name: The name of the machine.
        type: The type of the machine.
        max_capacity: The maximum number of labware this machine can hold.
        min_capacity: The minimum number of labware, this machine has to hold to be operational
        process_capacity: The maximum number of operations this machine can do at a time.
        allows_overlap: Whether operations, that have overlapping but not identical execution_time are allowed.
    """

    name: str
    type: str
    max_capacity: int
    min_capacity: int = 1
    process_capacity: int = 1
    allows_overlap: bool = False


class RequiredMachine(NamedTuple):
    """Container for a requirement of an operation"""

    type: str
    tag: str
    preferred: str | None = None


@dataclass
class Operation:
    """Editable data collection for a general operations in a workflow."""

    name: str  # important for referencing.
    duration: float  # duration of the operation in seconds
    start: datetime | None = None
    finish: datetime | None = None
    preceding_operations: list[str] = field(default_factory=list)  # list of the names of operations required for this
    required_machines: list[RequiredMachine] = field(default_factory=list)
    wait_cost: dict[str, float] = field(default_factory=dict)  # waiting costs after prior operations(linked by name)
    max_wait: dict[str, int] = field(default_factory=dict)  # maximum waiting times after prior operations
    min_wait: dict[str, int] = field(default_factory=dict)  # minimum waiting times after prior operations
    wait_to_start_costs: float = 0.5  # for numeric reasons we do not want it to be 0

    @property
    def main_machine(self) -> RequiredMachine | None:
        for used_machine in self.required_machines:
            if used_machine.tag == "main":
                return used_machine
        return None


@dataclass
class MoveOperation(Operation):
    """Operation resembling a movement of a container"""

    pref_dest_pos: int | None = None  # optional preferences for the destination slot number
    destination_pos: int = 0  # actual destination slot number (set at execution runtime)
    origin_pos: int = 0  # this should not be relevant for the execution but might be nice for logging

    @property
    def origin_machine(self) -> RequiredMachine | None:
        for used_machine in self.required_machines:
            if used_machine.tag == "origin":
                return used_machine
        return None

    @property
    def target_machine(self) -> RequiredMachine | None:
        for used_machine in self.required_machines:
            if used_machine.tag == "target":
                return used_machine
        return None


@dataclass
class ScheduledAssignment:
    """
    Every operation is assigned this data in a schedule
    """

    start: datetime  # scheduled start of the operation
    # List of operations scheduled involving the same machine(s), that have to finish prior
    machine_precedences: list[str] = field(default_factory=list)
    # participating are assigned by their tag in used_machines. e.g.: 'target'->'Carousel' or 'main'->'F5'
    machines_to_use: dict[str, str] = field(default_factory=dict)


Schedule = dict[str, ScheduledAssignment]


class MachineCollection:
    """
    This class is defined by just the list of available machines, but provides certain utilities
    """

    machine_by_id: dict[str, Machine]
    machine_class_sizes: dict[str, int]
    machine_by_class: dict[str, list[Machine]]
    n_machine_classes: int
    n_machines: int
    min_capacity_machines: dict[str, Machine]
    dump: Machine

    def __init__(self, machines: list[Machine]):
        # this avoids changing the original job shop (,i.e., adding a dummy)
        machines = deepcopy(machines)
        # create a dumping place so the schedule is for cut off workflows is still feasible
        self.dump = Machine(
            name="DummyDump",
            type="Dump",
            max_capacity=999,
            process_capacity=999,
            allows_overlap=True,
        )
        machines.append(self.dump)
        # create some convenience dictionaries
        self.machine_by_id = {m.name: m for m in machines}
        machine_classes = {m.type for m in machines}
        self.machines_by_class = {cls: [m for m in machines if m.type == cls] for cls in machine_classes}
        self.n_machine_classes = len(machine_classes)
        self.n_machines = len(machines)
        self.machine_class_sizes = {cls: len(self.machines_by_class[cls]) for cls in machine_classes}
        self.min_capacity_machines = {m.name: m for m in machines if m.min_capacity > 1}


class JSSP:
    """
    An instance of a special operation shop problem
    """

    operations_by_id: dict[str, Operation]
    machine_collection: MachineCollection
    _dummys: list[str]

    def __init__(self, operations: Iterable[Operation], machines: list[Machine]):
        self.machine_collection = MachineCollection(machines)
        self.operations_by_id = {op.name: op for op in operations}
        self._dummys = []
        self._wfg = None

    def is_dummy(self, op: Operation) -> bool:
        """
        Utilitxy function to check whether an operation is an artificial node (dummy)
        :param op:
        :return:
        """
        return op.name in self._dummys

    def add_dummys(self):
        """
        Utility function adding dummy nodes to ensure solvability of truncated workflows
        """
        if not self.machine_collection.machines_by_class["MoverServiceResource"]:
            # no movers means no dummy movements
            return
        # detect all last operations
        all_priors = set()
        for op in self.operations_by_id.values():
            all_priors.update(op.preceding_operations)
        last_operations = list(filter(lambda idx: idx not in all_priors, self.operations_by_id))
        # filter for those last operations leaving ending in places of limited space
        critical_last_op = []
        moveable_objects = len(last_operations)  # TODO How to I really extract this number from the problem???
        for idx in last_operations:
            op = self.operations_by_id[idx]
            if isinstance(op, MoveOperation):
                ending_place = op.target_machine
            else:
                ending_place = op.main_machine
            # get the spacial capacity if the executors or the minimum of all possile executors
            if ending_place.preferred:
                capacity = self.machine_collection.machine_by_id[ending_place.preferred].max_capacity
            else:
                possible_executors = self.machine_collection.machines_by_class[ending_place.type]
                capacity = min(machine.max_capacity for machine in possible_executors)
            if capacity < moveable_objects:
                critical_last_op.append(op)

        logger.debug(f"adding {len(last_operations)} dummys to {last_operations}")

        for i, op in enumerate(critical_last_op):
            if isinstance(op, MoveOperation):
                last_place = op.target_machine
            else:
                last_place = op.main_machine
            dump = self.machine_collection.dump
            mover_name = self.machine_collection.machines_by_class["MoverServiceResource"][0].name
            move_to_dump = MoveOperation(
                name=f"move_{i}_to_dump",
                preceding_operations=[op.name],
                duration=50,
                wait_cost={op.name: 1},
                min_wait={op.name: 0},
                max_wait={op.name: 2**31},
                required_machines=[
                    RequiredMachine(last_place.type, tag="origin", preferred=last_place.preferred),
                    RequiredMachine(type="MoverServiceResource", tag="main", preferred=mover_name),
                    RequiredMachine(type=dump.type, tag="target", preferred=dump.name),
                ],
            )
            self.operations_by_id[move_to_dump.name] = move_to_dump
            self._dummys.append(move_to_dump.name)

    def remove_dummys(self, schedule: Schedule):
        """
        Utility function removing the dummy nodes which are created to ensure solveability of truncated workflows
        :param schedule:
        """
        for dummy in self._dummys:
            if dummy in schedule:
                schedule.pop(dummy)

    def start_operation_ids(self) -> list[str]:
        """
        Utility function to get all operations that have no precedence constraints
        :return:
        """
        return [idx for idx, op in self.operations_by_id.items() if not op.preceding_operations]

    def start_occupations(self) -> dict[str, int]:
        """
        Utility function to extract the initial occupation of all machines before the processes start
        """
        occupation = dict.fromkeys(self.machine_collection.machine_by_id, 0)
        for start_id in self.start_operation_ids():
            start_op = self.operations_by_id[start_id]
            if isinstance(start_op, MoveOperation):
                start_machine = start_op.origin_machine
            else:
                start_machine = start_op.main_machine
            # TODO this does not find those containers that have an operation in their starting machine and counts
            # double reagents that have multiple parallel starting moves
            if start_machine.preferred:
                occupation[start_machine.preferred] += 0  # TODO change this 0 to 1 when the rest works
        return occupation

    def create_wfg(self) -> nx.DiGraph:
        """
        Utility function creating a networkx graph of the problems workflow
        :return: A directed graph of type networkx.DiGraph
        """
        g = nx.DiGraph()
        for idx, op in self.operations_by_id.items():
            g.add_node(idx)
            for prior in op.preceding_operations:
                g.add_edge(prior, idx)
        return g

    @property
    def wfg(self) -> nx.DiGraph:
        if not self._wfg:
            self._wfg = self.create_wfg()
        return self._wfg


class SolutionQuality(Enum):  # FIXME: add some obvious output when schedule is stuck.
    OPTIMAL = 1
    FEASIBLE = 2
    INFEASIBLE = 3
