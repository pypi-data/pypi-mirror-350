"""
Interface of JSSP solver
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from labscheduler.structures import JSSP, Schedule, SolutionQuality


class JSSPSolver(ABC):
    """
    The interface of a JSSP solver used in the LabScheduler
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "compute_schedule")
            and callable(subclass.compute_schedule)
            and hasattr(subclass, "is_solvable")
            and callable(subclass.is_solvable)
            and hasattr(subclass, "get_algorithm_info")
            and callable(subclass.get_algorithm_info)
        )

    @abstractmethod
    def compute_schedule(
        self,
        inst: JSSP,
        time_limit: float,
        offset: float,
        **kwargs,
    ) -> tuple[Schedule | None, SolutionQuality]:
        """
        Tries to compute a schedule for the given JSSP instance. Depending on the algorithm there might be no guaranty
        a solution is found.
        :param inst: The Problem instance
        :param time_limit: Maximum computation time(in seconds) the solver is allowed
        :param offset: Minimum time(in seconds) between call of the function and start time scheduled for any operation
        :param kwargs: Optional arguments custom to a solver
        :return: A valid schedule or None
        """

    @abstractmethod
    def is_solvable(self, inst: JSSP) -> bool:
        """
        Checks whether the JSSP instance is solvable at all
        """

    @staticmethod
    @abstractmethod
    def get_algorithm_info() -> AlgorithmInfo:
        """
        Every algorithm should provide this basic information about itself
        :return: A typing.NamedTuple containing name, optimality, success guaranty and recommended maximum problem size
        """


class AlgorithmInfo(NamedTuple):
    """
    Every algorithm should provide this basic information
    """

    name: str
    is_optimal: bool
    success_guaranty: bool
    max_problem_size: int
