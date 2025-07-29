"""

TODO: add wikipedia links


This module is and implementation of the basic Priority Dispatcher (PD). It is the basis for all priority dispatching
based scheduling algorithms. It provides the structures to schedule operations one after another (or multiple at a
time), contains the logic which operations are allowed to be scheduled and manages this as actions (nomenclature from
machine learning: action=act of adding a set of operations to the schedule). It is itself already a scheduling
algorithm, but it is recommended to add some more intelligence by inheriting and changing the sort_actions() method.

The code excerpt is from the `priority_dispatching_framework.py` file and contains the implementation of the
`PDFramework` class, which is a solver for the Job Shop Scheduling Problem (JSSP). The class inherits from the
`JSSPSolver` class and implements the `compute_schedule` method, which takes an instance of the JSSP and computes a
schedule for it. The method uses a priority dispatching heuristic algorithm to determine the order in which jobs should
be processed on machines. The `PDFramework` class contains several instance variables, including the JSSP instance, a
list of possible actions, a dictionary of machines used in the JSSP, and a list of job groups. The class also contains
several methods, including `sort_actions`, which sorts the list of possible actions based on their priority, and `step`,
which chooses and takes an action according to the current policies. The `sort_actions` method sorts the list of
possible actions based on their priority. The method first sorts the list based on whether the action contains any dummy
steps, with actions containing dummy steps having lower priority. The method then sorts the list based on whether the
action is doable, with doable actions having higher priority. Finally, the method sorts the list based on whether the
action has partially started, with actions that have partially started having the highest priority. The `step` method
chooses and takes an action according to the current policies. The method first sorts the list of possible actions using
the `sort_actions` method. The method then selects the first action in the sorted list and assigns it to a machine. The
method updates the schedule and the list of possible actions based on the assigned action. The method continues to
choose and take actions until there are no more possible actions. Overall, the `PDFramework` class implements a priority
dispatching heuristic algorithm to solve the JSSP. The class uses several methods to sort the list of possible actions
and choose the best action to assign to a machine. The algorithm is relatively simple and easy to implement, making it a
popular choice for solving JSSP problems. However, the algorithm does not guarantee an optimal solution and may not be
suitable for all JSSP problems.

(GitHub Copilot:)
"""

# ruff:noqa: N806
# FIXME: improve single letter variable naming and reactivate rules above

import traceback
from dataclasses import dataclass, field
from datetime import datetime, timedelta

import networkx as nx

from labscheduler.logging_manager import scheduler_logger as logger
from labscheduler.solver_interface import AlgorithmInfo, JSSPSolver
from labscheduler.structures import (
    JSSP,
    Machine,
    MachineCollection,
    MoveOperation,
    Operation,
    Schedule,
    ScheduledAssignment,
    SolutionQuality,
)


class UsedMachine(Machine):
    """
    Represents a machine on which operations get scheduled.
    It is meant to be a utility class for organizing the schedule
    on one particular machine.
    """

    # TODO: check whether this is really necessary and class name is appropriate / could be improved e.g.
    # MachineInstance or CurrentMachine

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.operations_by_start = []
        self.operations_by_finish = []
        self.start = {}
        self.finish = {}

    def min_transfer_time(self) -> datetime:
        """
        Determines, when the machine will be able to receive/give labware.
        Some machines can not receive labware while working.
        :return: A datetime. the default return value is datetime.today() if no restrictions are in place
        """
        if not self.allows_overlap and self.operations_by_finish:
            return max(self.finish.values())
        return datetime.today()

    def min_start(self) -> datetime:
        """
        Determines when this machine is able to do its next operation.
        :return: A datetime. If there are no restrictions from the machine side, it's datetime.today()
        """
        # there can only be restrictions of any operation is already scheduled
        if self.operations_by_start:
            latest = self.operations_by_start[-1]
            # computes the number of running operations when the last one was started
            running_operations = [j for j in self.operations_by_start if self.finish[j.name] > self.start[latest.name]]
            # if this is the current limit, we have to wait until one is finished
            if len(running_operations) == self.process_capacity:
                return min(self.finish[j.name] for j in running_operations)
        # default return
        return datetime.today()

    def waiting(self, start: datetime) -> float:
        """
        Computes the time, the machine will be idle until the given point in time
        :param start:
        :return: waiting time in seconds
        """
        # check whether there are any operations scheduled
        if self.operations_by_start:
            latest = self.operations_by_start[-1]
            n_running_operations = len(
                [j for j in self.operations_by_start if self.finish[j.name] > self.finish[latest.name]],
            )
            if n_running_operations == 0:
                return (start - self.finish[latest.name]).total_seconds()
        return 0

    def add(self, operation: Operation, start) -> None:
        """
        Adds the given operation to the machines schedule at the given time
        :param operation:
        :param start:
        :return:
        """
        self.operations_by_finish.append(operation)
        self.operations_by_start.append(operation)
        self.start[operation.name] = start
        self.finish[operation.name] = start + timedelta(seconds=operation.duration)


@dataclass
class Action:
    """
    Represents an action in the sense of a scheduling agent:
    Deciding to add a certain (set of) operations to the schedule with intended/scheduled starting times on certain
    machines.
    """

    operations: list[Operation]
    machine: UsedMachine
    priority: float
    assigned_tags: dict[str, UsedMachine] = field(default_factory=dict)
    min_start_job: datetime | None = None
    min_start_machine: datetime | None = None
    min_start: datetime | None = None
    wait_job: timedelta = timedelta(seconds=0)  # time, the job has to wait, if this action is chosen
    wait_machine: timedelta = timedelta(seconds=0)  # time, the machine has to wait, if this action is chosen
    doable: bool = True

    def __post_init__(self):
        start_time = datetime.today()
        if self.min_start_job is None:
            self.min_start_job = start_time
        if self.min_start_machine is None:
            self.min_start_machine = start_time
        if self.min_start is None:
            self.min_start = start_time

    def __str__(self):
        s = f"{[operation.name for operation in self.operations]}"
        for k, v in self.assigned_tags.items():
            if k == "target" and hasattr(v, "name"):
                s += f"-->{v.name}"
        s += f", {self.doable}"
        # s += f"{self.operation.name}, {self.min_start.hour}:{self.min_start.minute}:{self.min_start.second},
        # {self.operation.duration}"
        return s


@dataclass
class JobGroup:
    """
    Captures information on a special set of operations. Special means, that one operation has more than one direct
    predecessor and possibly multiple direct successors. The utility functions of this class help with scheduling such
    operation constellations correctly.
    """

    in_moves: list[str]
    out_moves: list[str]
    priority_moves: list[str]
    started: bool = False
    finished: bool = False

    def allowed(self, idx: str, possible_operation: list[str], past: list[str]):
        if not all(idx_o in possible_operation or idx_o in past for idx_o in self.in_moves):
            return False
        if idx in self.priority_moves:
            return True
        if len(self.priority_moves) > 0:
            return any(idx_o in past for idx_o in self.priority_moves)
        if idx in self.in_moves:
            return True
        return len(self.in_moves) == 0

    def remove(self, idx: str) -> None:
        """removes the given operation from this group's lists and sets the finished-flag if none is left"""
        if idx in self.in_moves:
            self.in_moves.remove(idx)
        if idx in self.out_moves:
            self.out_moves.remove(idx)
        if idx in self.priority_moves:
            self.priority_moves.remove(idx)
        self.finished = len(self.out_moves) == 0

    def is_partially_done(self, past: list[str]) -> bool:
        """Checks, whether any but not all the moves in this group have been done"""
        if self.finished:
            return False
        return any(idx in past for idx in self.in_moves)

    def update(self, past: list[str]) -> None:
        """removes all steps from its lists that have been done (are in past)."""
        for idx in past:
            # does not do anything if idx is not actually in this group
            self.remove(idx)


class PDFramework(JSSPSolver):
    """
    Copilot:
    Priority Dispatching Framework (PDF) is a heuristic algorithm for solving the Job Shop Scheduling Problem (JSSP).
    This class implements the PDF algorithm as a JSSP solver.
    The usual PDF constructs a schedule by adding operations one by one. In each step all operations with their
    preceding operations already scheduled are collected. Then the one with the highest priority is chosen and added
    to the schedule with the earliest possible starting time. This adding is called action.
    In our case an action cal also consist of adding multiple operations at once or the decision to scip an operation.
    Our addable operations are further restricted by capacity constraints.
    To more likely succeed, this framework applies the following rule:
    If one operation O has multiple preceding operations O_p, none of O_p shall be added to the schedule, before all
    of them are addable. After one of O_p was added, all of O_p have to be added, before any other operation is added.
    Afterward, O has to be added.
    This rule uses the class JobGroup.
    If an operation has no specified executing machine (only a machine type) and there are multiple machines of that
    type the heuristic will create multiple actions (one for adding the operation on each machine) and one will be
    chosen.
    """

    jssp: JSSP
    possible_actions: list[Action]
    min_start: datetime
    machine_by_name: dict[str, UsedMachine]
    reagent_names: list[str]
    groups: list[JobGroup]
    operation_to_group: dict[str, JobGroup | None]
    current_group: JobGroup | None
    schedule: Schedule
    load: dict[str, int]

    def compute_schedule(
        self,
        inst: JSSP,
        time_limit: float,
        offset: float,
        **kwargs,
    ) -> tuple[Schedule | None, SolutionQuality]:
        """
        Computes the schedule for the given JSSP instance using the PDF algorithm.

        :param inst: JSSP instance to solve.
        :param time_limit: Time limit for the solver.
        :param offset: Offset for the solver.
        :param kwargs: Additional arguments.
        :return: Schedule for the given JSSP instance.
        """
        self.jssp = inst
        for idx, step in inst.operations_by_id.items():
            logger.debug(f"{idx}: {step.required_machines}")
        now = datetime.now()
        self.reset(offset=offset)
        logger.debug(f"resetting took {(datetime.now() - now).total_seconds()}")
        now = datetime.now()
        quality = SolutionQuality.FEASIBLE
        while len(self.possible_actions) > 0:
            if not self.step():
                # break when no feasible step can be done
                quality = SolutionQuality.INFEASIBLE
                break
        logger.debug(f"making the actual steps took {(datetime.now() - now).total_seconds()}")
        for idx, assignment in self.schedule.items():
            logger.debug(idx, assignment.machines_to_use)
        return self.schedule, quality

    @staticmethod
    def get_algorithm_info() -> AlgorithmInfo:
        """
        Returns information about the PDF algorithm.

        :return: Information about the PDF algorithm.
        """
        return AlgorithmInfo(name="BasicPDHeur", is_optimal=False, success_guaranty=False, max_problem_size=500)

    def is_solvable(self, inst: JSSP) -> bool:
        """
        Determines whether the given JSSP instance is solvable using the PDF algorithm.

        :param inst: JSSP instance to check.
        :return: True if the given JSSP instance is solvable using the PDF algorithm, False otherwise.
        """
        return True

    def sort_actions(self, action_list: list[Action]):
        """
        Sorts the given list of actions according to the current policies.

        :param action_list: List of actions to sort.
        :return: Sorted version of the input list.
        """

        def partially_started(a: Action):
            return a.operations[0].start if a.operations[0].start is not None else datetime.max

        now = datetime.now()
        return sorted(
            action_list,
            key=lambda a: (
                now - partially_started(a),
                a.doable,
                not any(self.jssp.is_dummy(operation) for operation in a.operations),
            ),
        )

    def step(self) -> bool:
        """
        Chooses and takes an action according to the current policies.
        :return: Whether the step was successfully done
        """
        J = self.jssp.operations_by_id  # TODO: find a more expressive name than J
        lab = self.jssp.machine_collection
        if len(self.possible_actions) > 0:
            for action in self.possible_actions:
                # calculate minimal stating time
                self.set_min_start(action, J)

                # calculate waiting times
                action.wait_machine = action.machine.waiting(action.min_start)
                action.wait_job = action.min_start - action.min_start_job

                # check doability
                action.doable = self.is_doable(action)

            # choose the next action
            self.possible_actions = self.sort_actions(self.possible_actions)
            action = self.possible_actions.pop()
            assigned_machines = {}
            if not action.doable and not all(operation.start for operation in action.operations):
                # impossible operations from the past do not matter, so this is only a problem is none has its start set
                logger.warning("Heuristic thinks, this is infeasible!!")
                logger.debug([str(a) for a in self.possible_actions])
                for key, val in self.load.items():
                    logger.debug(key, val)
                return False

            for operation in action.operations:
                if isinstance(operation, MoveOperation):
                    # update the loads of origin and destination of the movement
                    source = self.get_origin(operation)
                    target = self.get_target(operation, action)
                    self.load[source] -= 1
                    self.load[target] += 1
                    assigned_machines["origin"] = source
                    assigned_machines["target"] = target

            # adds the action to the schedule and machines
            self.take_action(action, assigned_machines)
            # update the inner utility structures accordingly
            self.update_groups(action)
            self.update_possible_actions(lab, J)
            return True
        return None  # FIXME: no behavior was defined if len(possible_actions) == 0. Should it be None or False?

    def set_min_start(self, action: Action, J: dict[str, Operation]):
        """
        Determines what the earliest starting time for this action is.

        :param action: Action to determine the earliest starting time for.
        :param J: Dictionary of operations by ID.
        """
        # check when the machine has time for this operation(s)
        action.min_start_machine = action.machine.min_start()
        action.min_start_job = self.min_start

        for operation in action.operations:
            # ensure it does not start before a prior operation ends (+ min waiting time)
            for idx in operation.preceding_operations:
                prior_end = self.schedule[idx].start + timedelta(seconds=J[idx].duration)
                # add the eventual minimum waiting time
                if idx in operation.min_wait:
                    prior_end += timedelta(seconds=operation.min_wait[idx])
                action.min_start_job = max(action.min_start_job, prior_end)

            # for move operations we also need to check whether source or target are too busy
            # (capacity is handled elsewhere)
            if isinstance(operation, MoveOperation):
                source_machine = self.machine_by_name[self.get_origin(operation)]
                target_machine = self.machine_by_name[self.get_target(operation, action)]
                for machine in [source_machine, target_machine]:
                    # if the machine does not allow transfer while working and has already scheduled operations,
                    # we have to wait until they are finished
                    ready = machine.min_transfer_time()
                    action.min_start_machine = max(ready, action.min_start_machine)

            action.min_start = max([action.min_start_machine, action.min_start_job])
            # do not change starting times from the past
            if operation.start is not None:
                action.min_start = operation.start

    def is_doable(self, action: Action) -> bool:
        """
        Checks whether the given action is also possible in the current state of the machines.
        :param action:
        :return:
        """
        for operation in action.operations:
            if isinstance(operation, MoveOperation):
                # check whether the target has enough capacity
                target = self.get_target(operation, action)
                if self.load[target] >= self.machine_by_name[target].max_capacity:
                    return False
            operation_group = self.operation_to_group[operation.name]
            if operation_group:
                if self.current_group:
                    if self.current_group != operation_group:
                        return False
                else:
                    # a group should not be started if not all its starting operations are available
                    possible_operations = []
                    for a in self.possible_actions:
                        possible_operations.extend(operation.name for operation in a.operations)
                    if not operation_group.allowed(operation.name, possible_operations, list(self.schedule.keys())):
                        return False
        return True

    def update_groups(self, action_taken: Action):
        """
        Updates the intern operation group classes according to the taken action.
        :param action_taken:
        :return:
        """
        for operation in action_taken.operations:
            # update the operation_groups
            operation_group = self.operation_to_group[operation.name]
            if operation_group is not None:
                operation_group.started = True
                self.current_group = operation_group
                operation_group.remove(operation.name)
                if operation_group.finished:
                    self.current_group = None
                    # this can happen id a operation the just finished group is also part of another group
                    past = list(self.schedule.keys())
                    for operation_group in self.groups:
                        if operation_group.is_partially_done(past):
                            self.current_group = operation_group
                            operation_group.update(past)
                            break  # important in case more than one group was started

    def get_executor(self, op: Operation, lab: MachineCollection) -> list[UsedMachine]:
        """
        Determines which machine should execute this operation. For non move operations, we have to check what the
        last preceding move to device of the required type was. This should be the executor... also this is not failsafe
        """
        mach_pref = op.main_machine.preferred
        # if a certain machine is preferred and this is available, we only allow that
        if mach_pref and mach_pref in lab.machine_by_id:
            executors = [self.machine_by_name[mach_pref]]
        else:
            machine_type = op.main_machine.type
            if isinstance(op, MoveOperation):
                executors = lab.machines_by_class[machine_type]
            else:
                # check what is the last (or none existing) preceding MoveOperation to a machine of the required type
                # that should be the executing machine
                g = self.jssp.wfg
                j = self.jssp.operations_by_id
                preceding = nx.ancestors(g, op.name)
                scheduled_preceding_moves = [
                    j[idx] for idx in preceding if idx in self.schedule and isinstance(j[idx], MoveOperation)
                ]
                sorted_moves = sorted(scheduled_preceding_moves, key=lambda move: self.schedule[move.name].start)
                for move in sorted_moves:
                    if not isinstance(move, MoveOperation):
                        msg = "move is not a MoveOperation object."
                        raise TypeError(msg)
                    if move.target_machine.type == machine_type:
                        scheduled_target_name = self.schedule[move.name].machines_to_use["target"]
                        executors = [self.machine_by_name[scheduled_target_name]]
                        break
                else:
                    # if no such movement exists, we allow any devices
                    executors = lab.machines_by_class[machine_type]
        return executors

    def update_possible_actions(self, lab: MachineCollection, J: dict[str, Operation]):  # noqa: PLR0912, C901
        # FIXME: This function is very complex, consider refactoring and re-activating rules above
        """
        Updates the list of possible actions assuming the given action has been taken.
        :param lab:
        :param J:
        :return:
        """
        # TODO this code should be writeable much nicer
        # collect all operations that's prerequisites are fulfilled but are not scheduled, yet
        possible_operations = []
        for idx, operation in J.items():
            if idx not in self.schedule and all(idx_o in self.schedule for idx_o in operation.preceding_operations):
                possible_operations.append(operation)

        # collect all possible assignments
        operation_machine_tuples: list[tuple[Operation, UsedMachine, dict[str, UsedMachine]]] = []
        for operation in possible_operations:
            possible_executors = self.get_executor(operation, lab)
            for executor in possible_executors:
                if isinstance(operation, MoveOperation):
                    target_pref = operation.target_machine.preferred
                    if target_pref and target_pref in self.machine_by_name:
                        operation_machine_tuples.append(
                            (operation, executor, {"target": self.machine_by_name[target_pref]}),
                        )
                    else:
                        operation_machine_tuples.extend(
                            (operation, executor, {"target": possible_target})
                            for possible_target in lab.machines_by_class[operation.target_machine.type]
                        )
                else:
                    operation_machine_tuples.append((operation, executor, {}))

        self.possible_actions = []
        for machine in self.machine_by_name.values():
            for_this_machine = list(filter(lambda triple: triple[1].name == machine.name, operation_machine_tuples))
            op_for_this_machine = [triple[0] for triple in for_this_machine]
            # here, we handle the operations for min_capacity machines special
            if machine.min_capacity > 1:
                if not machine.allows_overlap:
                    # in that case, all operations need to have the same duration
                    lengths = {op.duration for op in op_for_this_machine}
                    lengths.add(-1)
                    for length in lengths:
                        mathing_operations = [op for op in op_for_this_machine if op.duration == length]
                        # for finished operations, the lengths is irrelevant
                        if length == -1:
                            mathing_operations = [op for op in op_for_this_machine if op.start]
                        # iterate over all possibilities of how many and which ones to schedule
                        for num in range(machine.min_capacity, 1 + min(len(mathing_operations), machine.max_capacity)):
                            # todo go through all possible combinations instead of simple taking the first num
                            operations = mathing_operations[:num]
                            # set the waiting cost of the action to the maximum waiting
                            # of the participating operations
                            wait_cost = 0
                            for operation in operations:
                                for costs in operation.wait_cost.values():
                                    wait_cost = max(wait_cost, costs)
                            self.possible_actions.append(Action(operations, machine, wait_cost))
                else:
                    for num in range(machine.min_capacity, 1 + min(len(op_for_this_machine), machine.max_capacity)):
                        # todo go through all possible combinations instead of simple taking the first num
                        operations = op_for_this_machine[:num]
                        # set the waiting cost of the action to the maximum waiting
                        # of the participating operations
                        wait_cost = 0
                        for operation in operations:
                            for costs in operation.wait_cost.values():
                                wait_cost = max(wait_cost, costs)
                        self.possible_actions.append(Action(operations, machine, wait_cost))
            else:
                for operation, _m, tag_assignments in for_this_machine:
                    wait_cost = max(operation.wait_cost.values()) if operation.wait_cost else 0
                    self.possible_actions.append(Action([operation], machine, wait_cost, assigned_tags=tag_assignments))

    def take_action(self, action: Action, assigned_machines: dict[str, str]):
        """
        Adds the operations of this action to the schedule on the chosen machine
        :param action:
        :param assigned_machines:
        :return:
        """
        for operation in action.operations:
            action.machine.add(operation, action.min_start)
            assigned_machines["main"] = action.machine.name
            # add operation to schedule
            self.schedule[operation.name] = ScheduledAssignment(
                start=action.min_start,
                machines_to_use=assigned_machines,
            )

    def get_origin(self, operation: MoveOperation) -> str:
        """
        Determines the or at least a possible source machine for this move
        :param operation:
        :return:
        """
        origin_type = operation.origin_machine.type
        try:
            # check for the last matching operation:
            # either a movement with fitting target or an operation on a fitting device
            j = self.jssp.operations_by_id
            for idx in operation.preceding_operations:
                op = j[idx]
                if op.main_machine.type == origin_type:
                    return self.schedule[idx].machines_to_use["main"]
                if isinstance(op, MoveOperation) and op.target_machine.type == origin_type:
                    return self.schedule[idx].machines_to_use["target"]
        except Exception:  # noqa: BLE001
            logger.exception(f"Exception during get_origin().\n{traceback.print_exc()}")
        source_pref = operation.origin_machine.preferred
        # use the preference if it is available
        if source_pref and source_pref in self.jssp.machine_collection.machine_by_id:
            return source_pref
        # todo go back further in the workflow until we find a matching operation
        # else take the first of the required type
        source = self.jssp.machine_collection.machines_by_class[origin_type][0].name
        logger.warning(f"We are not sure, whether {source} is really the source of {operation.name}")
        return source

    def get_target(self, operation: MoveOperation, action: Action) -> str:
        """
        Determines the or at least a possible target machine for this move
        :param operation:
        :return:
        """
        return action.assigned_tags["target"].name

    def schedule_started_operations(self):
        """
        Adds all already started operations to the schedule and
        sets up the inner variables to build the complete schedule from there
        """
        # todo: implement this. It not essential but should speed up the solving process.

        # add all started operations to schedule and the respective machines
        # set the current loading state
        # set the current group

    def reset(self, offset: float = 10):
        """
        Prepares to compute a new schedule by resetting all the inner structures.
        :param offset:
        :return:
        """
        self.possible_actions = []
        J = self.jssp.operations_by_id
        self.schedule = {}
        lab = self.jssp.machine_collection
        self.min_start = datetime.today() + timedelta(seconds=offset)
        self.machine_by_name = {name: UsedMachine(**machine.__dict__) for name, machine in lab.machine_by_id.items()}
        self.load = dict.fromkeys(self.machine_by_name, 0)
        self.groups = []
        self.operation_to_group = dict.fromkeys(J)
        self.current_group = None

        # identify operations that have multiple operation as prerequisites.Those should be scheduled together
        # or a machine might get into a loading deadlock
        moves = [idx for idx, op in J.items() if isinstance(op, MoveOperation)]
        for idx, operation in J.items():
            if len(operation.preceding_operations) > 1:
                in_moves = list(operation.preceding_operations)
                out_moves = [
                    idx_o
                    for idx_o, operation_o in J.items()
                    if idx in operation_o.preceding_operations and idx_o in moves
                ]
                priority_moves = [idx for idx in in_moves if operation.preceding_operations]
                group = JobGroup(in_moves, out_moves, priority_moves)
                self.groups.append(group)
                self.operation_to_group[idx] = group
                for idx_o in out_moves:
                    self.operation_to_group[idx_o] = group
                for idx_o in in_moves:
                    # it's possible that a move is in_move of one group and out_move of another group
                    if not self.operation_to_group[idx_o]:
                        self.operation_to_group[idx_o] = group

        self.schedule_started_operations()
        self.update_possible_actions(lab, J)
