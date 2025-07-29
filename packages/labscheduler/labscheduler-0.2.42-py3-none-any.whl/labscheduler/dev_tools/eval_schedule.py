import logging
from datetime import datetime, timedelta
from typing import NamedTuple

from labscheduler.structures import JSSP, MoveOperation, Schedule

DEFAULT_ALPHA = 20

logger = logging.getLogger(__name__)


class LevelChange(NamedTuple):
    machine: str
    time: datetime
    change: int


def check_completeness(inst: JSSP, sol: Schedule) -> bool:
    return all(idx in sol for idx in inst.operations_by_id)


def check_spacial_capacities(inst: JSSP, sol: Schedule) -> bool:
    filling = dict.fromkeys(inst.machine_collection.machine_by_id, 0)
    changes = []
    for idx, op in inst.operations_by_id.items():
        if isinstance(op, MoveOperation):
            origin = sol[idx].machines_to_use["origin"]
            target = sol[idx].machines_to_use["target"]
            changes.append(LevelChange(target, sol[idx].start, 1))
            end = sol[idx].start + timedelta(seconds=op.duration - 0.1)
            changes.append(LevelChange(origin, end, -1))
    changes = sorted(changes, key=lambda ch: ch.time)
    # simulate through all movements and check whether spacial capacities get violated
    for change in changes:
        filling[change.machine] += change.change
        if filling[change.machine] > inst.machine_collection.machine_by_id[change.machine].max_capacity:
            logger.warning(f"capacity of {change.machine} gets exceeded.")
            return False
    return True


def check_process_capacities(inst: JSSP, sol: Schedule) -> bool:
    workload = dict.fromkeys(inst.machine_collection.machine_by_id, 0)
    changes = []
    for idx, op in inst.operations_by_id.items():
        executor = sol[idx].machines_to_use["main"]
        changes.append(LevelChange(executor, sol[idx].start, 1))
        end = sol[idx].start + timedelta(seconds=op.duration - 0.1)
        changes.append(LevelChange(executor, end, -1))
    changes = sorted(changes, key=lambda ch: ch.time)
    # simulate through all executions and check whether process capacities get violated
    for change in changes:
        workload[change.machine] += change.change
        if workload[change.machine] > inst.machine_collection.machine_by_id[change.machine].process_capacity:
            logger.warning(f"processing capacity of {change.machine} gets exceeded.")
            return False
    return True


WAIT_TOLERANCE = 2


def check_waiting(inst: JSSP, sol: Schedule) -> bool:
    for idx, op in inst.operations_by_id.items():
        for idx_o in op.preceding_operations:
            preceding = inst.operations_by_id[idx_o]
            wait_time = (sol[idx].start - sol[idx_o].start).total_seconds() - preceding.duration
            if wait_time + WAIT_TOLERANCE < op.min_wait[idx_o]:
                logger.warning(
                    f"Waiting time between {idx_o} and {idx} is {op.min_wait[idx_o] - wait_time} seconds too short",
                )
                return False
            if wait_time - WAIT_TOLERANCE > op.max_wait[idx_o]:
                logger.warning(f"Waiting time between {idx_o} and {idx} is {wait_time - op.max_wait[idx_o]} too long")
                return False
    return True


def check_load_while_work(inst: JSSP, sol: Schedule) -> bool:
    return True


def is_feasible_solution(inst: JSSP, sol: Schedule) -> bool:
    """ """
    try:
        return (
            check_process_capacities(inst, sol)
            and check_spacial_capacities(inst, sol)
            and check_process_capacities(inst, sol)
            and check_waiting(inst, sol)
            and check_load_while_work(inst, sol)
        )
    except Exception:
        logger.exception("Checking solution failed")
        return False


def objective_value(inst: JSSP, sol: Schedule, alpha: float = DEFAULT_ALPHA) -> float:
    """ """
    start = min(sol[idx].start for idx in sol)
    finish_id = {idx: sol[idx].start + timedelta(seconds=op.duration) for idx, op in inst.operations_by_id.items()}
    finish = max(finish_id.values())
    makespan = (finish - start).total_seconds()
    total_wait_cost = 0
    for idx, op in inst.operations_by_id.items():
        for idx_o in op.preceding_operations:
            wait_time = sol[idx].start - finish_id[idx_o]
            wait_cost = op.wait_cost[idx_o] * wait_time.total_seconds()
            total_wait_cost += wait_cost

    return alpha * makespan + total_wait_cost
