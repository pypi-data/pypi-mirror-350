"""
This is the main class for the LabScheduler. Its methods are interfaced by the SiLA feature implementations or
via console script.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable

from labscheduler.solver_interface import AlgorithmInfo, JSSPSolver
from labscheduler.structures import Machine, Operation, Schedule, SolutionQuality


class SchedulerInterface(ABC):
    """
    A collection of required attributes of a labscheduler.
    """

    # The solver implementation
    jssp_solver: JSSPSolver
    # The collection of machines to schedule on.
    job_shop: list[Machine]

    @abstractmethod
    def configure_job_shop(self, machine_list: list[Machine]):
        """
        Sets the set of available machines to schedule workflows on. This will be kept until this method is called again
        :param machine_list: List of machines making up the job-shop
        :return:
        """

    @abstractmethod
    def select_algorithm(self, algorithm_name: str) -> bool:
        """
        Selects the algorithm to use for computing schedules until another algorithm is chosen.
        You can get the names of all available algorithms by calling get_available_algorithms() and retrieving the
        'name' attribute of each.
        :param algorithm_name: Name of the algorithm
        :return:
        """

    @property
    @abstractmethod
    def available_algorithms(self) -> list[AlgorithmInfo]:
        """
        Lists the basic information of each available algorithm
        :return:
        """

    @property
    @abstractmethod
    def current_algorithm_info(self) -> AlgorithmInfo:
        """
        Retrieves the basic information of the currently selected algorithm.
        :return: A typing.NamedTuple containing name, optimality, success guaranty and recommended maximum problem size
        """

    @abstractmethod
    def compute_schedule(
        self,
        operations: Iterable[Operation],
        computation_time: float,
    ) -> tuple[Schedule | None, SolutionQuality]:
        """
        Uses the currently selected algorithm to compute a schedule for the given workflow in the currently configured
        lab. This workflow must be given as a list of Operations.
        :param operations: List of operations
        :param computation_time: The maximum computation time. No scheduled start will be earlier than now + this
        parameter
        :return: An assignment of machines, precedence constraints and start time to each operation or None if no
        valid schedule was found. Additionally, an enum whether the schedule is optimal, feasible or infeasible.
        Sometimes even infeasible, but almost feasible solution is better than nothing.
        """
