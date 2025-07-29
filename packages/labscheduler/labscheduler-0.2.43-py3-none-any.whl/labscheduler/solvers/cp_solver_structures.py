"""
Collection of utility structures used by the CP solver
"""

from dataclasses import dataclass, field
from datetime import datetime

try:
    from ortools.sat.cp_model_pb2 import CpSolverStatus
    from ortools.sat.python.cp_model import (
        FEASIBLE,
        OPTIMAL,
        Constraint,
        IntervalVar,
        IntVar,
        LinearExpr,
    )
except ModuleNotFoundError as e:
    msg = (
        "The required optional dependency 'ortools' is not installed. Please install it using "
        "'pip install .[cpsolver]'."
    )
    raise ModuleNotFoundError(msg) from e

from labscheduler.logging_manager import scheduler_logger as logger
from labscheduler.structures import JSSP, Operation, SolutionQuality


@dataclass
class IntervalBundle:
    """
    Contains all information about the interval variables corresponding to an operation.
    """

    op_idx: str  # name of the operation
    # list of interval vars together with a dictionary {tag: machine_name} to specify the executors and a is_present
    # variable(which might be a fix integer or an actual variable)
    interval_vars: list[tuple[IntervalVar, dict[str, str], bool | IntVar]] = field(default_factory=list)

    def __str__(self):
        return f"{self.op_idx}:\n" + "\n".join(str(tupl[1]) for tupl in self.interval_vars)


class CPVariables:
    operation_by_machine: dict[str, list[IntervalVar]]
    reference_time: datetime
    offset: int
    # some generous upper bound for the makespan
    horizon: int
    intervals: dict[str, IntervalBundle]
    # provides the is_present variable to interval variable_name
    presence = dict[str, int | IntVar]
    objective: LinearExpr | int
    hard_time_cons: list[Constraint] | None = None

    def __init__(self, inst: JSSP, offset: int):
        self.operation_by_machine = {name: [] for name in inst.machine_collection.machine_by_id}
        self.reference_time = datetime.now()
        self.horizon = 2**31 - 1
        self.offset = offset
        self.intervals = {}
        self.presence = {}
        self.inst = inst
        self.objective = 0
        self.aux_vars = []
        if self.hard_time_cons is None:
            self.hard_time_cons = []

    def intervals_by_id(self, idx: str) -> list[IntervalVar]:
        intervals = []
        for interval, _roles, _is_present in self.intervals[idx].interval_vars:
            intervals.append(interval)
        return intervals

    @property
    def all_intervals(self) -> list[IntervalVar]:
        intervals = []
        for bundle in self.intervals.values():
            for interval, _roles, _is_present in bundle.interval_vars:
                intervals.append(interval)
        return intervals

    def add_interval(self, o: Operation, interval: IntervalVar, is_present: int | IntVar = 1, **kwargs):
        """
        Adds the interval var into the correct bundle.
        In the kwargs must be specified which machine shall execute which required role
        if that is not already specified in the operation (i.e. for pooling).
        """
        # create an entry if necessary
        if o.name not in self.intervals:
            self.intervals[o.name] = IntervalBundle(o.name)
        roles = {}
        for required in o.required_machines:
            # the executing machine is either fixed by the operation....
            if required.preferred:
                roles[required.tag] = required.preferred
            # ... or specified in the kwargs
            elif required.tag not in kwargs:
                logger.error(f"The executor for {required} in operation {o.name} is unclear")
            else:
                roles[required.tag] = kwargs[required.tag]
        # add the tuple of interval-var and role assignments
        self.intervals[o.name].interval_vars.append((interval, roles, is_present))
        self.operation_by_machine[roles["main"]].append(interval)
        # links variable name and is_present variable
        self.presence[interval.name] = is_present


def solver_status_to_solution_quality(status: CpSolverStatus) -> SolutionQuality:
    if status == OPTIMAL:
        return SolutionQuality.OPTIMAL
    if status == FEASIBLE:
        return SolutionQuality.FEASIBLE
    return SolutionQuality.INFEASIBLE
