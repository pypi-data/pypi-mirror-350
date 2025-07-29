"""
Basic priority dispatching framework
This module contains a basic implementation of the priority dispatching framework.

The priority dispatching framework is a general framework for solving scheduling problems. It is based on the idea of
assigning priorities to actions (operations or jobs) and then scheduling them in order of priority. The framework
consists of a class PDFramework, which implements the basic algorithm, and a class Action, which represents an action
that can be scheduled. The framework can be extended by subclassing PDFramework and overriding the sort_actions method.

The basic algorithm works as follows:
    1. The algorithm is initialized with a list of actions to be scheduled.
    2. The algorithm sorts the actions according to their priority.
    3. The algorithm iterates over the sorted list of actions. For each action, it tries to schedule it as early as
        possible, without violating any constraints. If this is not possible, the action is scheduled as late as
        possible.
    4. The algorithm returns the schedule.

This module contains an extension of the basic priority dispatching framework, called MachinePriorityHeuristic.
It gives priority to operations on machines with a more critical workload and the waiting times on those.
The module also defines a function to get algorithm information.
An extension of the basic priority dispatching framework.
"""

from datetime import datetime, timedelta
from random import randint

from labscheduler.logging_manager import scheduler_logger as logger
from labscheduler.scheduler_interface import AlgorithmInfo
from labscheduler.solvers.priority_dispatching_framework import Action, PDFramework
from labscheduler.structures import MoveOperation


class BottleneckPD(PDFramework):
    """
    Simple extension of the priority dispatching heuristic,
    that gives priority to operations on machines with a more critical workload and the waiting times on those, i.e.,
    where the ratio of the total duration of all operations on it to the process capacity is the largest.
    These machines are the bottleneck of the process and should be prioritized to avoid delays.

    This class is a subclass of PDFramework, which implements the basic priority dispatching
    algorithm.

    Attributes:
        workload (Dict[str, float]): A dictionary that maps machine names to their workload, which is a measure of how
            busy the machine is. The workload is computed in the reset() method.

    Methods:
        sort_actions(action_list: List[Action]) -> List[Action]: Sorts a list of actions according to several criteria,
            including the workload of the machine, the waiting time on the machine, the minimum start time of the
            action, the wait cost of the job, and the priority of the action. Returns the sorted list of actions.
        reset(offset: float = 10): Resets the state of the algorithm and computes the workload of each machine based on
            the jobs assigned to it. The offset parameter is passed to the superclass method.
        get_algorithm_info() -> AlgorithmInfo: Returns an AlgorithmInfo object that describes the algorithm.
    """

    workload: dict[str, float]

    def sort_actions(self, action_list: list[Action]) -> list[Action]:
        wait_costs = {}
        for action in action_list:
            job = action.operations[0]
            if job.wait_cost:
                wait_costs[job.name] = max(job.wait_cost.values())
            else:
                wait_costs[job.name] = 0

        # adds several criteria to the list sorting (lexicographic order). The last one is most important.

        now = datetime.today()
        action_list = sorted(
            action_list,
            key=lambda action: (
                self.workload[action.machine.name],
                -(action.wait_machine * self.workload[action.machine.name]),
                now - action.min_start,
                wait_costs[action.operations[0].name],
                action.priority,
            ),
        )

        # an action that can be completed before another can be started, the first should have priority
        action_list = super().sort_actions(action_list)
        change = True

        def finishes_before_last(a: Action):
            _last = action_list[-1]
            finish = max(a.min_start + timedelta(seconds=job.duration) for job in a.operations)
            return finish < _last.min_start

        while change:
            last = action_list[-1]

            action_list = sorted(action_list, key=finishes_before_last)
            action_list = super().sort_actions(action_list)
            change = last != action_list[-1]

        return action_list

    def is_doable(self, action: Action) -> bool:
        # TODO: This is a workaround to a Greifswald specific problem. Find a general solution.
        rotanta_transfer_capacity = 4
        doable = super().is_doable(action)
        op = action.operations[0]
        if (
            isinstance(op, MoveOperation)
            and op.target_machine.preferred == "Rotanta_Transfer"
            and op.origin_machine.preferred != "Rotanta"
        ):
            load_sum = self.load["Rotanta_Transfer"] + self.load["Rotanta"]
            if load_sum >= rotanta_transfer_capacity:
                return False
        return doable

    def reset(self, offset: float = 10):
        super().reset(offset=offset)
        self.workload = {}
        for name, machine in self.machine_by_name.items():
            op_on_machine = [op for op in self.jssp.operations_by_id.values() if op.main_machine.preferred == name]
            self.workload[name] = sum(len(op.preceding_operations) for op in op_on_machine) / machine.max_capacity
            logger.debug(f"workload of {name}: {self.workload[name]}")

    @staticmethod
    def get_algorithm_info() -> AlgorithmInfo:
        return AlgorithmInfo(name="BottleneckPD", is_optimal=False, success_guaranty=False, max_problem_size=700)


class Random(PDFramework):
    def sort_actions(self, action_list: list[Action]) -> list[Action]:
        action_list = sorted(action_list, key=lambda a: randint(1, 1_000_000))  # noqa: S311
        return super().sort_actions(action_list)
        # FIXME: I believe this function ultimately randomly shuffles the list.
        # If that is the case, it would be better to rename the function to reflect that.
        # either way, this function looks overly complex for what it does.

    @staticmethod
    def get_algorithm_info() -> AlgorithmInfo:
        return AlgorithmInfo(name="RandomPD", is_optimal=False, success_guaranty=False, max_problem_size=1000)


class LPTF(PDFramework):
    def sort_actions(self, action_list: list[Action]) -> list[Action]:
        action_list = sorted(action_list, key=lambda a: a.min_start, reverse=True)
        return super().sort_actions(action_list)

    @staticmethod
    def get_algorithm_info() -> AlgorithmInfo:
        return AlgorithmInfo(name="LPTFPD", is_optimal=False, success_guaranty=False, max_problem_size=1000)
