"""
A solver implementation using google OR-tools to model and solve the JSSP as a constraint program(CP)
"""

import contextlib
import time
import traceback
from copy import deepcopy
from datetime import datetime, timedelta
from math import ceil, floor

try:
    from ortools.sat.cp_model_pb2 import CpSolverStatus
    from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, UNKNOWN, CpModel, CpSolver, IntervalVar, IntVar
except ModuleNotFoundError as e:
    msg = (
        "The required optional dependency 'ortools' is not installed. Please install it using "
        "'pip install .[cpsolver]' to use the CP solver."
    )
    raise ModuleNotFoundError(msg) from e

from labscheduler.logging_manager import scheduler_logger as logger
from labscheduler.solver_interface import AlgorithmInfo, JSSPSolver
from labscheduler.solvers.cp_solver_structures import CPVariables, solver_status_to_solution_quality
from labscheduler.solvers.specialized_pd_implementation import LPTF, BottleneckPD
from labscheduler.structures import (
    JSSP,
    MoveOperation,
    Operation,
    RequiredMachine,
    Schedule,
    ScheduledAssignment,
    SolutionQuality,
)

ALPHA = 20  # the balance between makespan and waiting costs
# When infeasibility is detected the solver tries again turning hard waiting constraints into soft constraints
# adding this penalty per second of violation
PENALTY = 1000
VERBOSE = False  # set true to print the ortools search progress
HEURISTICS: list[JSSPSolver] = [BottleneckPD(), LPTF()]


class CPSolver(JSSPSolver):
    # HACK useful until ortools adds the bugfix to their release.
    # Currently, solutions found through hints sometimes get lost.
    backup_sol: Schedule | None

    def compute_schedule(
        self,
        inst: JSSP,
        time_limit: float,
        offset: float,
        **kwargs,
    ) -> tuple[Schedule | None, SolutionQuality]:
        try:
            model, vars_ = self.create_model(inst, offset)
            solver, state = self.solve_cp(model, vars_, time_limit=time_limit)
            if state in {OPTIMAL, FEASIBLE}:
                schedule = self.extract_schedule(solver, vars_, inst)
            # useful until ortools releases their bugfix
            elif state == UNKNOWN and CPSolver.backup_sol:
                logger.warning("ortools seems to be still buggy. using computed backup solution")
                schedule = CPSolver.backup_sol
                state = FEASIBLE
            else:
                schedule = None
            quality = solver_status_to_solution_quality(state)
        except Exception:  # noqa: BLE001
            logger.exception(f"Exception during schedule computation.\n{traceback.print_exc()}")
        else:
            return schedule, quality

    def is_solvable(self, inst: JSSP) -> bool:
        model, vars_ = self.create_model(inst, 0)
        # TODO: there is a method in OR-tools to check solvability
        state = self.solve_cp(model, vars_, 5)
        return state in {OPTIMAL, FEASIBLE}

    @staticmethod
    def get_algorithm_info() -> AlgorithmInfo:
        return AlgorithmInfo(
            name="CP-Solver",
            is_optimal=True,
            success_guaranty=True,
            max_problem_size=60,
        )

    @staticmethod
    def create_model(inst: JSSP, offset: float) -> tuple[CpModel, CPVariables]:
        model = CpModel()
        vars_ = CPSolver.create_variables(model, inst, ceil(offset))
        CPSolver.set_objective(model, vars_, inst)
        CPSolver.add_precedence_constraints(model, vars_, inst)
        CPSolver.add_processing_capacity_constraints(model, vars_, inst)
        CPSolver.add_spacial_capacity_constraints(model, vars_, inst)
        CPSolver.add_load_while_processing_constraints(model, vars_, inst)
        return model, vars_

    @staticmethod
    def apply_heuristics(cp: CpModel, solver: CpSolver, vars_: CPVariables) -> Schedule | None:
        solver.parameters.fix_variables_to_their_hinted_value = True
        inst = deepcopy(vars_.inst)

        # HACK: OR-Tools doesn't provide a clean way to get all variables, so we brute-force indices.
        all_vars: list[IntVar] = []
        with contextlib.suppress(Exception):
            all_vars.extend(cp.get_int_var_from_proto_index(i) for i in range(2**30))

        # round the start, finish and duration to match the CP problem
        for idx, o in inst.operations_by_id.items():
            interval = vars_.intervals_by_id(idx)[0]
            o.duration = interval.size_expr()

        solutions = []
        for heur in HEURISTICS:
            schedule, quality = heur.compute_schedule(inst, time_limit=1, offset=vars_.offset)
            if quality in {SolutionQuality.FEASIBLE, SolutionQuality.OPTIMAL}:
                # apply hints
                for idx, assign in schedule.items():
                    if inst.operations_by_id[idx].start:
                        continue
                    # get from date times to integers like used in the CP solver
                    start = round((assign.start - vars_.reference_time).total_seconds())
                    start_suggestion = start
                    for cp_interval_var in vars_.intervals_by_id(idx):
                        cp.add_hint(cp_interval_var.start_expr(), start_suggestion)

                # try the solution
                status = solver.solve(cp)
                msg = f"Heuristic found a {solver.status_name(status)} solution"
                # save the solution and objective
                if status in {CpSolverStatus.OPTIMAL, CpSolverStatus.FEASIBLE}:
                    solutions.append((solver.values(all_vars), solver.objective_value, schedule))
                    msg += f" with objective value: {solutions[-1][1]}"
                logger.info(msg)
                # clear the hints
                cp.clear_hints()
        # allow the solver to ignore our hints (hopefully it at least tests it)
        solver.parameters.fix_variables_to_their_hinted_value = False
        # give the best hints we have
        if solutions:
            sorted_solutions = sorted(solutions, key=lambda t: t[1])
            best_sol = sorted_solutions[0]
            for var, val in zip(all_vars, best_sol[0]):
                cp.add_hint(var, val)
            return best_sol[2]
        return None

    @staticmethod
    def solve_cp(cp: CpModel, vars_: CPVariables, time_limit: float) -> tuple[CpSolver, CpSolverStatus]:
        logger.info("start solving....")
        start = time.time()
        solver = CpSolver()
        # enforce the time limit
        solver.parameters.max_time_in_seconds = round(time_limit)
        CPSolver.backup_sol = CPSolver.apply_heuristics(cp, solver, vars_)
        logger.info(f"\nHeuristics done after {round(time.time() - start, 2)}seconds. optimizing... ")

        if VERBOSE:
            solver.parameters.log_search_progress = True
        status = solver.Solve(cp)
        logger.info(
            f"... solver done. result: {solver.status_name(status)} (obj:{solver.objective_value})"
            f" after {round(time.time() - start, 2)}seconds",
        )
        if status == CpSolverStatus.INFEASIBLE:
            logger.info("Try with hard waiting constraints turned soft")
            solver, status = CPSolver.try_soft_time_constraints(cp, vars_, time_limit - (time.time() - start))
        return solver, status

    @staticmethod
    def try_soft_time_constraints(cp: CpModel, vars_, time_limit) -> tuple[CpSolver, CpSolverStatus]:
        solver = CpSolver()
        # enforce the time limit
        solver.parameters.max_time_in_seconds = time_limit
        for cons in vars_.hard_time_cons:
            cons.only_enforce_if(False)
        CPSolver.add_soft_waiting_constraints(cp, vars_)
        status = solver.Solve(cp)
        logger.info(
            f"... solver done trying soft constraints."
            f"result: {solver.status_name(status)} (obj:{solver.objective_value})",
        )
        logger.debug("auxilary variables:")
        for aux in vars_.aux_vars:
            logger.debug(aux, solver.Value(aux))
        return solver, status

    @staticmethod
    def extract_schedule(solver: CpSolver, vars_: CPVariables, inst: JSSP) -> Schedule:
        schedule = {}
        for idx, bundle in vars_.intervals.items():
            for var, roles, is_present in bundle.interval_vars:
                used = solver.value(is_present)
                # get the found start time
                start_value = solver.value(var.start_expr())
                logger.debug(
                    f"{var.name} is used: {bool(used)}, start: {start_value}, end: {solver.value(var.end_expr())}",
                )
                if used:
                    # convert it to datetime using the reference time
                    start = vars_.reference_time + timedelta(seconds=start_value)
                    schedule[idx] = ScheduledAssignment(start=start, machines_to_use=roles)
        return schedule

    @staticmethod
    def create_interval_var(
        lb: int,
        ub: int,
        o: Operation,
        cp: CpModel,
        ref_time: datetime,
        optionality: IntVar | None = None,
    ) -> IntervalVar:
        """
        Utility method to create and add a new interval variable to the model. Returns the created variable.
        """
        if optionality is not None:
            name = optionality.name
        else:
            name = f"I_{o.name}"
        if o.start:
            start = round((o.start - ref_time).total_seconds())
        else:
            start = cp.new_int_var(lb, ub, name=f"start_{o.name}")
        if o.finish:
            end = round((o.finish - ref_time).total_seconds())
            size = end - start
        else:
            size = ceil(o.duration)
            end = cp.new_int_var(lb, ub, name=f"end_{o.name}")

        if optionality is not None:
            interval_var = cp.new_optional_interval_var(
                start=start,
                size=size,
                end=end,
                name=name,
                is_present=optionality,
            )
        else:
            interval_var = cp.new_interval_var(start=start, size=size, end=end, name=name)
        return interval_var

    @staticmethod
    def create_variables(cp: CpModel, inst: JSSP, offset: int) -> CPVariables:
        vars_ = CPVariables(inst, offset)
        pooling_operations = []
        for o in inst.operations_by_id.values():
            ambiguous_executors = [r for r in o.required_machines if not r.preferred]
            if ambiguous_executors:
                pooling_operations.append(o)
                if len(ambiguous_executors) > 1:
                    logger.warning(
                        f"We can not yet handle operations with multiple ambiguous executors: {o.required_machines}",
                    )
            else:
                var = CPSolver.create_interval_var(offset, vars_.horizon, o, cp, vars_.reference_time)
                vars_.add_interval(o, var)
        # handle all the operations which have multiple machines to possibly be executed by (flexible JSSP)
        CPSolver.handle_pooling(cp, vars_, pooling_operations, inst)
        return vars_

    @staticmethod
    def handle_pooling(cp: CpModel, vars_: CPVariables, operations: list[Operation], inst: JSSP):
        """
        Creates the part of the model which assigns executing machines to operations which can be executed by different
        machines.
        """
        # Add optional intervals for every possible executor
        for op in operations:
            # find the ambiguous executor(s)...
            # ... we currently assume, there is only one such required machine
            for ambiguous in [rm for rm in op.required_machines if not rm.preferred]:
                # iterate over all possible executors
                for machine in inst.machine_collection.machines_by_class[ambiguous.type]:
                    # create and add a matching optional interval
                    is_present = cp.new_int_var(0, 1, name=f"{op.name}_{ambiguous.tag}->{machine.name}")
                    interval = CPSolver.create_interval_var(
                        vars_.offset,
                        vars_.horizon,
                        op,
                        cp,
                        vars_.reference_time,
                        optionality=is_present,
                    )
                    vars_.add_interval(op, interval, **{ambiguous.tag: machine.name}, is_present=is_present)
            # enforce exactly one of those intervals to be chosen
            is_present_vars = [t[2] for t in vars_.intervals[op.name].interval_vars]
            cp.add_exactly_one(is_present_vars)

        # for subsequent operations, the main/target of the first must match the source/main of the second
        def relevant_machine(op: Operation, is_first: bool) -> RequiredMachine:
            if isinstance(op, MoveOperation):
                if is_first:
                    return op.target_machine
                return op.origin_machine
            return op.main_machine

        # find all pairs of subsequent operations where matching executors must be enforced
        for idx, op in inst.operations_by_id.items():
            for idx_prev in op.preceding_operations:
                op_prev = inst.operations_by_id[idx_prev]
                machine_post = relevant_machine(op, is_first=False)
                machine_prev = relevant_machine(op_prev, is_first=True)
                if not (machine_prev.preferred and machine_post.preferred):
                    for _i1, roles_prev, is_present_prev in vars_.intervals[idx_prev].interval_vars:
                        for _i2, roles_post, is_present_post in vars_.intervals[idx].interval_vars:
                            # check whether the relevant executing machines match
                            if roles_prev[machine_prev.tag] == roles_post[machine_post.tag]:
                                # either both intervals must be chosen or none
                                cp.add(is_present_prev == is_present_post)

    @staticmethod
    def set_objective(cp: CpModel, vars_: CPVariables, inst: JSSP):
        makespan = cp.new_int_var(lb=0, ub=vars_.horizon, name="makespan")
        cp.add_max_equality(
            makespan,
            [interval.end_expr() for interval in vars_.all_intervals],
        )

        # create the variable for total waiting costs
        # we need some upper bound: Use horizon*maximum waiting costs per second
        max_wait_cost = 100
        for op in inst.operations_by_id.values():
            if op.wait_cost:
                for costs in op.wait_cost.values():
                    max_wait_cost = max(max_wait_cost, costs)
        wc_ub = ceil(vars_.horizon * max_wait_cost)
        wait_cost = cp.new_int_var(lb=0, ub=wc_ub, name="waitcost")

        # create waiting cost variables for every precedence constraint
        wait_costs_per_op = []
        for idx, op in inst.operations_by_id.items():
            if op.wait_cost:
                for second in vars_.intervals_by_id(idx):
                    for idx_o, cost_per_second in op.wait_cost.items():
                        wc = cp.new_int_var(lb=0, ub=wc_ub, name=f"wc_{idx}->{idx_o}")
                        # TODO: this gives wrong waiting costs for pooling operations
                        for first in vars_.intervals_by_id(idx_o):
                            cp.add(wc >= (second.start_expr() - first.end_expr()) * round(cost_per_second))
                        wait_costs_per_op.append(wc)
        # add costs for waiting until start
        for idx in inst.start_operation_ids():
            # when it has already started this is redundant
            if not inst.operations_by_id[idx].start:
                wc = cp.new_int_var(lb=0, ub=wc_ub, name=f"wc_{idx}-start")
                for interval in vars_.intervals_by_id(idx):
                    wait_to_start_costs = round(inst.operations_by_id[idx].wait_to_start_costs)
                    cp.add(wc >= interval.start_expr() * wait_to_start_costs)
                wait_costs_per_op.append(wc)
        # sum up all waiting costs
        cp.add_abs_equality(wait_cost, sum(wait_costs_per_op))
        # set the objective
        vars_.objective = ALPHA * makespan + wait_cost
        cp.minimize(vars_.objective)

    @staticmethod
    def add_precedence_constraints(cp: CpModel, vars_: CPVariables, inst: JSSP):
        for idx, o in inst.operations_by_id.items():
            for idx_prev in o.preceding_operations:
                for prev_interval in vars_.intervals_by_id(idx_prev):
                    for post_interval in vars_.intervals_by_id(idx):
                        # for operations of the past, this is irrelevant
                        if not o.start:
                            # normal precedence
                            cp.add(prev_interval.end_expr() <= post_interval.start_expr())
                            min_wait = ceil(o.min_wait[idx_prev])
                            if min_wait:
                                constraint = cp.add(min_wait <= post_interval.start_expr() - prev_interval.end_expr())
                                vars_.hard_time_cons.append(constraint)
                            max_wait = floor(min(o.max_wait[idx_prev], vars_.horizon))
                            # only add a constraint when relevant
                            if max_wait < vars_.horizon:
                                constraint = cp.add(post_interval.start_expr() - prev_interval.end_expr() <= max_wait)
                                vars_.hard_time_cons.append(constraint)

    @staticmethod
    def add_soft_waiting_constraints(cp: CpModel, vars_: CPVariables):
        # linear expressions that SHOULD be <=0
        lin_expr = []
        for idx, o in vars_.inst.operations_by_id.items():
            for idx_prev in o.preceding_operations:
                for prev_interval in vars_.intervals_by_id(idx_prev):
                    for post_interval in vars_.intervals_by_id(idx):
                        # for operations of the past, this is irrelevant
                        if not o.start:
                            min_wait = ceil(o.min_wait[idx_prev])
                            if min_wait:
                                lin_expr.append(min_wait + prev_interval.end_expr() - post_interval.start_expr())
                            max_wait = floor(min(o.max_wait[idx_prev], vars_.horizon))
                            # only add a constraint when relevant
                            if max_wait < vars_.horizon:
                                lin_expr.append(post_interval.start_expr() - prev_interval.end_expr() - max_wait)
        # auxiliary variables to allow costly violation of constraints
        aux_vars = []
        for i, expr in enumerate(lin_expr):
            aux_var = cp.new_int_var(0, vars_.horizon, f"aux_{i}")
            cp.add(expr - aux_var <= 0)
            aux_vars.append(aux_var)
        new_objective = PENALTY * sum(aux_vars) + vars_.objective
        cp.minimize(new_objective)
        vars_.aux_vars = aux_vars

    @staticmethod
    def add_processing_capacity_constraints(cp: CpModel, vars_: CPVariables, inst: JSSP):
        for name, machine in inst.machine_collection.machine_by_id.items():
            operations_on_machine = vars_.operation_by_machine[name]
            if operations_on_machine:
                # handle maximum capacity constraints
                if machine.process_capacity == 1:
                    cp.add_no_overlap(operations_on_machine)
                else:
                    cp.add_cumulative(
                        operations_on_machine,
                        capacity=machine.process_capacity,
                        demands=[1 for op in operations_on_machine],
                    )
                # handle minimum capacity constraints
                if machine.min_capacity > 1:
                    num_inactive_intervals = (
                        floor(len(operations_on_machine) / machine.min_capacity) + 1
                    )  # one more than the max number of periods of activity
                    actives = [1]
                    level_changes = [-machine.min_capacity]
                    times = [0]
                    # model the changes to/from inactivity as optional level changes
                    for i in range(num_inactive_intervals):
                        actives.append(cp.new_int_var(0, 1, name=f"start_inactive_{machine.name}_{i}_p"))
                        actives.append(cp.new_int_var(0, 1, name=f"end_inactive_{machine.name}_{i}_p"))
                        level_changes += [machine.max_capacity, -machine.max_capacity]
                        times.append(cp.new_int_var(0, vars_.horizon, name=f"start_inactive_{machine.name}_{i}"))
                        times.append(cp.new_int_var(0, vars_.horizon, name=f"end_inactive_{machine.name}_{i}"))
                    for interval in operations_on_machine:
                        is_present = vars_.presence[interval.name]
                        actives += [is_present, is_present]
                        level_changes += [1, -1]
                        times += [interval.start_expr(), interval.end_expr()]
                    cp.add_reservoir_constraint_with_active(
                        times=times,
                        level_changes=level_changes,
                        actives=actives,
                        min_level=0,
                        max_level=machine.max_capacity - machine.min_capacity,
                    )

    @staticmethod
    def add_spacial_capacity_constraints(cp: CpModel, vars_: CPVariables, inst: JSSP):
        machine_names = inst.machine_collection.machine_by_id.keys()
        start_occupation = inst.start_occupations()
        changes = {name: [] for name in machine_names}
        times = {name: [] for name in machine_names}
        actives = {name: [] for name in machine_names}
        for idx, bundle in vars_.intervals.items():
            if isinstance(inst.operations_by_id[idx], MoveOperation):
                for interval, roles, is_present in bundle.interval_vars:
                    origin = roles["origin"]
                    target = roles["target"]
                    # during the move both locations are considered occupied
                    times[origin].append(interval.end_expr())
                    times[target].append(interval.start_expr())
                    changes[target].append(1)
                    changes[origin].append(-1)
                    # by adding is_present to the actives, the solver ignores non-present intervals
                    actives[target].append(is_present)
                    actives[origin].append(is_present)
        for name in machine_names:
            capacity = inst.machine_collection.machine_by_id[name].max_capacity
            # TODO for some strange reason the first call creates a variable fixed to 1
            cp.add_reservoir_constraint_with_active(
                times=[0] + times[name],
                level_changes=[start_occupation[name]] + changes[name],
                actives=[1] + actives[name],
                min_level=-1000,
                max_level=capacity,
            )

    @staticmethod
    def add_load_while_processing_constraints(cp: CpModel, vars_: CPVariables, inst: JSSP):
        for name, machine in inst.machine_collection.machine_by_id.items():
            if not machine.allows_overlap:
                for idx, op in inst.operations_by_id.items():
                    # iterate over all move operations
                    if isinstance(op, MoveOperation):
                        for move_interval, roles, _is_present in vars_.intervals[idx].interval_vars:
                            # check whether the move involves this machine
                            if name in {roles["origin"], roles["target"]}:
                                # iterate over all operations on this machine
                                for op_interval in vars_.operation_by_machine[name]:
                                    # add pair wise no-overlap constraints
                                    cp.add_no_overlap([op_interval, move_interval])

    @staticmethod
    def add_group_constraints(cp: CpModel, vars_: CPVariables, inst: JSSP):
        """
        Not strictly necessary in the sense of the JSSP definition. We define a group of operations as an operation
        together with all its directly preceding options which must be more than one. The constraints added in this
        function enforce all operations of a group to be started before another one can be started.

        """
