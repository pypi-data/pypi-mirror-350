"""
A very basic solver.

The code excerpt is from the `simple_scheduler.py` file and contains the implementation of the `SimpleSolver` class,
which is a solver for the Job Shop Scheduling Problem (JSSP). The class inherits from the `JSSPSolver` class and
implements the `compute_schedule` method, which takes an instance of the JSSP and computes a schedule for it. The method
uses a simple algorithm that schedules the operations sequentially, i.e. no operations will be done in parallel.

The `SimpleSolver` class contains several instance variables, including the JSSP instance, a list of operations, a list
of machines, and a minimum start time. The class also contains several methods, including `is_solvable`, which always
returns `True`, and `compute_schedule`, which computes a schedule for the JSSP instance.

The `compute_schedule` method computes a schedule for the JSSP instance using a simple algorithm that schedules the
operations sequentially. The method first initializes a dictionary to store the schedule and sets the minimum start time
to the current time plus an offset. The method then identifies the operations that have already started and the
operations that have not yet started. The method computes the minimum start time for the operations that have not yet
started based on the start times of the operations that have already started.

The method then creates a directed acyclic graph (DAG) representing the JSSP instance and performs a topological sort on
the graph to determine the order in which the operations should be scheduled. The method then iterates over the
operations in the sorted order and assigns each operation to a machine. The method updates the schedule and the start
time based on the duration of the operation.

Overall, the `SimpleSolver` class implements a simple algorithm that schedules the operations sequentially to solve the
JSSP. The algorithm is relatively simple and easy to implement, making it a good choice for demonstration and test
purposes. However, the algorithm does not take into account machine capacities or other constraints and may not be
suitable for more complex JSSP problems.

(GitHub Copilot)

"""

from datetime import datetime, timedelta

import networkx as nx

from labscheduler.solver_interface import AlgorithmInfo, JSSPSolver
from labscheduler.structures import JSSP, Schedule, ScheduledAssignment, SolutionQuality


class SimpleSolver(JSSPSolver):
    """
    A very simple algorithm, that schedules the operations sequentially, i.e. no operations will be done in parallel.
    It is only intended for demonstration and test purposes
    """

    def is_solvable(self, inst: JSSP) -> bool:
        """
        Check if the given JSSP instance is solvable by this algorithm.

        Args:
            inst (JSSP): The JSSP instance to check.

        Returns:
            bool: True if the instance is solvable, False otherwise.
        """
        return True

    def compute_schedule(
        self,
        inst: JSSP,
        time_limit: float,
        offset: float,
        **kwargs,
    ) -> tuple[Schedule | None, SolutionQuality]:
        """
        Compute a schedule for the given JSSP instance using this algorithm.

        Args:
            inst (JSSP): The JSSP instance to compute the schedule for.
            time_limit (float): The maximum time limit for the computation.
            offset (float): The offset time to start the schedule from.
            **kwargs: Additional keyword arguments.

        Returns:
            Optional[Schedule]: The computed schedule, or None if no schedule could be computed.
        """
        schedule = {}
        operations = inst.operations_by_id
        machines = inst.machine_collection
        min_start = datetime.today() + timedelta(seconds=offset)
        started = [idx for idx, op in operations.items() if op.start is not None]
        not_started = [idx for idx, op in operations.items() if op.start is None]
        if started:
            min_start2 = max(operations[idx].start + timedelta(seconds=operations[idx].duration) for idx in started)
            min_start = max(min_start, min_start2)

        graph = inst.create_wfg()
        top_sort = nx.topological_sort(graph)
        to_schedule = [n for n in top_sort if n in not_started]
        start = min_start
        for idx in to_schedule:
            operation = operations[idx]
            machine_assignments = {}
            for requirement in operation.required_machines:
                machine_name = machines.machines_by_class[requirement.type][0].name
                machine_assignments[requirement.tag] = machine_name

            schedule[idx] = ScheduledAssignment(start=start, machines_to_use=machine_assignments)
            start += timedelta(seconds=operation.duration)
        return schedule, SolutionQuality.FEASIBLE

    @staticmethod
    def get_algorithm_info() -> AlgorithmInfo:
        """
        Get information about this algorithm.

        Returns:
            AlgorithmInfo: An object containing information about this algorithm.
        """
        return AlgorithmInfo(name="Simple", is_optimal=False, success_guaranty=False, max_problem_size=1000)
