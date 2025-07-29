"""
Implementation of the JSSPSolver interface using MIPs and PySCIPOpt.
Solving JSSP with MIP models gets very time-consuming with increasing size.
This module can include any other implementation of the JSSPSolver interface as primal heuristic.
Find the documentation of SCIP here: https://www.scipopt.org/
"""

# ruff: noqa: N999, N806

from __future__ import annotations

import time
import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta

import numpy as np

try:
    from pyscipopt import SCIP_HEURTIMING, SCIP_RESULT, SCIP_STAGE, Heur, Model, quicksum, scip
except ModuleNotFoundError as e:
    msg = (
        "The required optional dependency 'pyscipopt' is not installed. Please install it using "
        "'pip install .[mipsolver]'. to use the MIP solver."
    )
    raise ModuleNotFoundError(msg) from e

from labscheduler.config import ALPHA, VERBOSE
from labscheduler.logging_manager import scheduler_logger as logger
from labscheduler.solver_interface import AlgorithmInfo, JSSPSolver
from labscheduler.solvers.specialized_pd_implementation import LPTF, BottleneckPD
from labscheduler.structures import JSSP, MoveOperation, Schedule, ScheduledAssignment, SolutionQuality


def cap(list1, list2):
    """
    Utility method to construct a list containing all elements, that are in both lists
    """
    return list(set(list1).intersection(set(list2)))


class JSSPHeuristicWrapper(Heur):
    """
    Wrapper to include any implementation of the interface solver_interface.JSSPSolver as primal heuristic in SCIP.
    This primal heuristic will run once in the beginning of the MIP solving process to try to find a upper bound
    (i.e. feasible solution). Multiple instances can be added to include more than one algorithm implementation.
    """

    # algorithm used to find a primal solution
    solver: JSSPSolver
    # original JSSP instance
    inst: JSSP
    # original JSSP instance transformed into a MIP model
    jssp_model: JSSPModel
    # timelimit to spend on heuristic
    timelimit: float

    def __init__(self, solver: JSSPSolver, inst: JSSP, jssp_model: JSSPModel, offset: float = 0, timelimit: float = 60):
        super().__init__()
        self.solver = solver
        self.inst = inst
        self.jssp_model = jssp_model
        self.timelimit = timelimit
        self.offset = offset
        # count, how often the heuristic was called
        self.num_called = 0

    def heurexec(self, heurtiming, nodeinfeasible):
        """
        Interface method of SCIP calling the heuristic execution
        """
        timer_start = time.time()
        # since all current solving heuristic are deterministic, we only want to call it once
        if self.num_called > 0:
            return {"result": SCIP_RESULT.DIDNOTFIND}
        self.num_called += 1

        schedule, quality = self.solver.compute_schedule(inst=self.inst, time_limit=self.timelimit, offset=self.offset)
        logger.debug("heuristic solution is ", quality.name)
        if quality == SolutionQuality.INFEASIBLE:
            return {"result": SCIP_RESULT.DIDNOTFIND}
        # this is needed to translate a solution back into scip
        var_by_name = {var.name: var for var in self.jssp_model.scip_model.getVars()}
        logger.debug(f"heuristic took {time.time() - timer_start} seconds")
        to_fix = []
        fix_vals = []
        # fix the starting times
        for idx, assignment in schedule.items():
            x_idx = (assignment.start - self.jssp_model.ref_time).total_seconds()
            to_fix.append(var_by_name[self.jssp_model.x[idx].name])
            fix_vals.append(x_idx)
        len_s, len_f, len_h = 0, 0, 0
        J = self.inst.operations_by_id
        # fix the s and f variables
        for idx_o, assgn_o in schedule.items():
            for idx_i, assgn_i in schedule.items():
                if not (idx_i == idx_o or assgn_o.start == assgn_i.start):
                    s_oi_orig = self.jssp_model.s[idx_o][idx_i]
                    if isinstance(s_oi_orig, scip.Variable):
                        s_oi_val = int(assgn_o.start < assgn_i.start)
                        s_oi_var = var_by_name[s_oi_orig.name]
                        to_fix.append(s_oi_var)
                        fix_vals.append(s_oi_val)
                        len_s += 1
                    finish_o = assgn_o.start + timedelta(seconds=J[idx_o].duration)
                    if finish_o != assgn_i.start:
                        f_oi_orig = self.jssp_model.f[idx_o][idx_i]
                        if isinstance(f_oi_orig, scip.Variable):
                            f_oi_val = int(finish_o < assgn_i.start)
                            f_oi_var = var_by_name[f_oi_orig.name]
                            to_fix.append(f_oi_var)
                            fix_vals.append(f_oi_val)
                            len_f += 1
        logger.debug(f"identifying to_fix variables took {time.time() - timer_start} seconds")
        logger.debug(f"Variables fixed: s:{len_s}, f:{len_f}, h:{len_h}")
        timer_start = time.time()
        m2 = self.jssp_model.scip_model.copyLargeNeighborhoodSearch(to_fix, fix_vals)
        MIPSolver.tune_params(m2, self.timelimit)
        if not VERBOSE:
            m2.hideOutput()
        m2.optimize()
        accepted = False
        if len(m2.getSols()) > 0:
            opt = m2.getBestSol()
            translated = self.jssp_model.scip_model.translateSubSol(m2, opt, self)
            accepted = self.jssp_model.scip_model.trySol(translated)
        m2.freeProb()  # this probably still has some effect on memory consumption
        if accepted:
            return {"result": SCIP_RESULT.FOUNDSOL}
        return {"result": SCIP_RESULT.DIDNOTFIND}


@dataclass
class JSSPModel:
    """
    Container class to contain a SCIP model and the various variables. For their Documentation see
    [https://gitlab.com/opensourcelab/labscheduler/-/blob/develop/docs/tex_files/mip_translation.tex?ref_type=heads]
    """

    # TODO: The link is to the tex file but it is not properly included in the documentation

    scip_model: Model
    T: scip.Variable
    x: dict[str, scip.Variable]
    y: dict[str, dict[str, list[scip.Variable]]]
    s: dict[str, dict[str, scip.Variable]]
    f: dict[str, dict[str, scip.Variable]]
    h: dict[str, dict[str, dict[str, list[scip.Variable]]]]
    ref_time: datetime

    @property
    def solution_found(self) -> bool:
        n_solutions = self.scip_model.getNSolsFound()
        return n_solutions > 0


class MIPSolver(JSSPSolver):
    heuristics: list[JSSPSolver]

    def __init__(self):
        super().__init__()
        self.heuristics = [BottleneckPD(), LPTF()]
        self.ref_time = None

    def compute_schedule(
        self,
        inst: JSSP,
        time_limit: float,
        offset: float,
        **kwargs,
    ) -> tuple[Schedule | None, SolutionQuality]:
        logger.info(
            f"computing optimum (offset={offset}, timelimit={time_limit}"
            f" for {len(inst.operations_by_id)} operations)...",
        )
        try:
            start = time.time()
            jssp_model = self.setup_mip(inst, offset)
            logger.debug(f"creation took {time.time() - start} seconds")
            len_s = sum(sum(isinstance(v, scip.Variable) for v in d.values()) for d in jssp_model.s.values())
            len_f = sum(sum(isinstance(v, scip.Variable) for v in d.values()) for d in jssp_model.f.values())
            len_y = sum(sum(len(l_) for l_ in d.values()) for d in jssp_model.y.values())
            len_h = sum(
                sum(sum(len(l_) for l_ in d_i.values()) for d_i in d_o.values()) for d_o in jssp_model.h.values()
            )
            logger.debug(f"Variable counts: s:{len_s}, f:{len_f}, y:{len_y}, h:{len_h}")
            for solver in self.heuristics:
                self.include_heuristic(inst, jssp_model, solver, offset, time_limit)
            time_spent = time.time() - start
            logger.info(f"Start solving after {time_spent} seconds")
            time_left = max(time_limit - time_spent, 0.1)
            MIPSolver.tune_params(jssp_model.scip_model, time_limit=time_left)
            quality = SolutionQuality.INFEASIBLE
            if not VERBOSE:
                jssp_model.scip_model.hideOutput()
            jssp_model.scip_model.optimize()
            if not jssp_model.solution_found:
                logger.warning("MIP solver did not find a solution")
                return None, quality
            quality = SolutionQuality.FEASIBLE
            if jssp_model.scip_model.getStage() == SCIP_STAGE.SOLVED:
                quality = SolutionQuality.OPTIMAL
            schedule = self.translate_assignments(inst, jssp_model)
        except Exception:  # noqa: BLE001
            logger.exception(traceback.print_exc())
        else:
            return schedule, quality
        return None, SolutionQuality.INFEASIBLE

    @staticmethod
    def get_algorithm_info() -> AlgorithmInfo:
        return AlgorithmInfo(name="MIP-Solver", is_optimal=True, success_guaranty=True, max_problem_size=40)

    def is_solvable(self, inst: JSSP):
        available_machines = {m.type for m in inst.machine_collection.machine_by_id.values()}
        for job in inst.operations_by_id.values():
            for used_machine in job.required_machines:
                D_k = used_machine.type
                if D_k not in available_machines:
                    return False
        return True

    @staticmethod
    def include_heuristic(inst: JSSP, jssp_model: JSSPModel, solver: JSSPSolver, offset: float, timelimit: float):
        heur = JSSPHeuristicWrapper(solver, inst, jssp_model, offset, timelimit)
        jssp_model.scip_model.includeHeur(
            heur,
            solver.get_algorithm_info().name,
            "custom heuristic implemented in python",
            "Y",
            timingmask=SCIP_HEURTIMING.BEFOREPRESOL,
            usessubscip=True,
        )

    @staticmethod
    def setup_mip(inst: JSSP, offset: float) -> JSSPModel:  # noqa: PLR0912, PLR0915, C901
        # FIXME: this function is highly complex, consider refactoring and re-activating rules above
        """
        Sets up all variables and constraints and saved them into a container class
        :param inst: scheduling problem instance
        :param offset: time until first scheduled job may start
        :return: container with scip model and structured links to variables
        """
        J = inst.operations_by_id
        mc = inst.machine_collection
        # we need a reference time to use seconds instead of timestamps
        ref_time = datetime.now()
        if any(j.start for j in J.values()):
            ref_time = min(j.start for j in J.values() if j.start is not None)
        # link the durations for convenience
        d = {idx: j.duration for idx, j in J.items()}
        # have the list of each job's used resources ready for convenience
        used_resources = {idx: [d.type for d in j.required_machines] for idx, j in J.items()}
        # extract all machine classes we are going to use
        D = []
        for used in used_resources.values():
            D.extend(used)
        # remove doubles
        D = list(set(D))
        # some big number greater than T. here sum of all durations + all waiting times + ofset
        total_min_wait = sum(sum(o.min_wait.values()) for o in J.values() if o.min_wait)
        M = sum(d.values()) + offset + total_min_wait
        # A is defined as dictionary of integers {machine_class -> # machines}
        A = mc.machine_class_sizes
        model = Model("scheduling MIP")
        T = model.addVar(name="T", vtype="C", lb=0, obj=ALPHA)
        # sum up the coefficients for the waiting costs
        coeff = dict.fromkeys(J, 0)
        constant_costs = 0
        for idx, j_i in J.items():
            for j_o in j_i.preceding_operations:
                if j_o in J:
                    c_io = j_i.wait_cost[j_o]
                    coeff[idx] += c_io
                    # We would like to use the ending time of j_o but have no variable for that...
                    coeff[j_o] -= c_io
                    # ... this accounts for the difference
                    constant_costs += d[j_o] * c_io
            if not j_i.preceding_operations:
                coeff[idx] += j_i.wait_to_start_costs
        model.addObjoffset(-constant_costs)
        # remove the constant costs from
        x = {idx: model.addVar(name=f"x_{idx}", vtype="C", lb=0, obj=coeff[idx]) for idx, j in J.items()}
        # make not-yet-started jobs wait for the offset to pass
        earliest_start = (datetime.today() - ref_time).total_seconds() + offset
        for idx, j in J.items():
            if j.start is None:
                model.addCons(x[idx] >= earliest_start)
        # make sense of T (x_i+d_i <= T)
        for idx, j in J.items():
            model.addCons(x[idx] + j.duration <= T)
        # ensure correct order of jobs
        for idx, j_i in J.items():
            for j_o in j_i.preceding_operations:
                if j_i.start is None and j_o in J:  # afterwards, nobody cares ;-)
                    model.addCons(x[j_o] + d[j_o] <= x[idx])
        # enforce maximum waiting times
        for idx, j_i in J.items():
            if j_i.start is None:
                for j_o, w_io in j_i.max_wait.items():
                    if w_io == np.inf:
                        continue
                    model.addCons(x[idx] <= x[j_o] + d[j_o] + w_io)
                for j_o, w_min_io in j_i.min_wait.items():
                    if w_min_io > 0:
                        model.addCons(x[j_o] + d[j_o] + w_min_io <= x[idx])
        # add the y-variables
        y = {}
        count = 0
        for idx in J:
            y[idx] = {}
            for D_k in used_resources[idx]:
                y[idx][D_k] = []
                for A_kl in range(A[D_k]):
                    y_ikl = model.addVar(name=f"y_{idx},{D.index(D_k)},{A_kl}", vtype="B", obj=0.1)
                    count += 1
                    y[idx][D_k].append(y_ikl)
        # used for convenience
        names = {D_k: [machine.name for machine in mc.machines_by_class[D_k]] for D_k in D}
        # fix the starting time of already started jobs (for dynamic scheduling)
        for idx, j in J.items():
            if j.start is not None:
                diff = (j.start - ref_time).total_seconds()
                model.fixVar(x[idx], diff)
                # fix all machine assignments for jobs that already started
                for used_machine in j.required_machines:
                    D_k = used_machine.type
                    name = used_machine.preferred
                    if name not in names[D_k]:
                        logger.warning(f"job {j} is missing a assigned machine")
                    else:
                        model.fixVar(y[idx][D_k][names[D_k].index(name)], 1)
            else:
                # account for wishes regarding executing machine
                for used_machine in j.required_machines:
                    if used_machine.preferred is not None:
                        name = used_machine.preferred
                        D_k = used_machine.type
                        if name not in names[D_k]:
                            logger.warning(f"Sorry, preferred machine {name} for {j} was not found in lab")
                        else:
                            for machine_name, y_ikl in zip(names[D_k], y[idx][D_k]):
                                model.fixVar(y_ikl, int(machine_name == name))
        # every job needs exactly one machine to do it
        for idx in J:
            for D_k in used_resources[idx]:
                model.addCons(quicksum(y[idx][D_k][A_kl] for A_kl in range(A[D_k])) == 1)
        # make sure, jobs are shared machines use the same machine instance
        for idx, j in J.items():
            if j.start is None:
                for idx_o in j.preceding_operations:
                    if idx_o in J:
                        shared = cap(used_resources[idx], used_resources[idx_o])
                        for D_k in shared:
                            for l_ in range(A[D_k]):
                                y_ikl = y[idx][D_k][l_]
                                y_okl = y[idx_o][D_k][l_]
                                model.addCons(y_ikl == y_okl)
        # introduce variables to enforce capacities
        s = {idx_o: {} for idx_o in J}
        f = {idx_o: {} for idx_o in J}
        for idx_o, j_o in J.items():
            for idx_i, j_i in J.items():
                if idx_i == idx_o:
                    continue
                if j_o.start is None:
                    if j_i.start is None:
                        s[idx_o][idx_i] = model.addVar(name=f"s_{idx_o},{idx_i}", vtype="B")
                        f[idx_o][idx_i] = model.addVar(name=f"f_{idx_o},{idx_i}", vtype="B")
                    else:
                        s[idx_o][idx_i] = 0
                        f[idx_o][idx_i] = 0
                else:
                    if j_i.start is None:
                        s[idx_o][idx_i] = 1
                    else:
                        s[idx_o][idx_i] = int(j_o.start < j_i.start)
                    if j_o.finish is None:
                        if j_i.start is None:
                            f[idx_o][idx_i] = model.addVar(name=f"f_{idx_o},{idx_i}", vtype="B")
                        else:
                            f[idx_o][idx_i] = 0
                    elif j_i.start is None:
                        f[idx_o][idx_i] = 1
                    else:
                        f[idx_o][idx_i] = int(j_o.finish < j_i.start)
        h = {
            idx_o: {
                idx_i: {
                    D_k: [model.addVar(name=f"h_{idx_i},{idx_o},{D_k},{l_}", vtype="B") for l_ in range(A[D_k])]
                    for D_k in cap(used_resources[idx_i], used_resources[idx_o])
                }
                for idx_i, j_i in J.items()
                if idx_i != idx_o and j_i.finish is None
            }
            for idx_o, j_o in J.items()
            if j_o.finish is None
        }
        # enforce capacities
        for idx_i, j_i in J.items():
            if j_i.finish is None:
                for D_k in used_resources[idx_i]:
                    C_k = mc.machines_by_class[D_k][0].process_capacity
                    for A_kl in range(A[D_k]):
                        model.addCons(
                            quicksum(
                                h[idx_o][idx_i][D_k][A_kl]
                                for idx_o, j_o in J.items()
                                if D_k in used_resources[idx_o] and idx_i != idx_o and j_o.finish is None
                            )
                            <= M - M * y[idx_i][D_k][A_kl] + C_k - 1,
                        )
        # other way of enforcing capacities
        # capacity additions to machines by an operation
        cp = {idx: [] for idx in J}
        # capacity reductions to machines by an operation
        cn = {idx: [] for idx in J}
        # here, we assume, only MoveJobs change the occupancy of machines
        for idx, j in J.items():
            if isinstance(j, MoveOperation):
                cp[idx].append(j.target_machine.type)
                cn[idx].append(j.origin_machine.type)
        # add capacity constraints
        for i in J:
            for D_k in cp[i]:
                if D_k == "ContainerStorageResource":  # TODO: can this be replaced ?
                    continue
                # TODO we can skip this constraint if the total amount labware is lower than the capacity
                for l_ in range(A[D_k]):
                    C_l = mc.machines_by_class[D_k][l_].max_capacity
                    in_moves = {o: y[o][D_k][l_] for o in J if o != i and D_k in cp[o]}
                    out_moves = {o: y[o][D_k][l_] for o in J if o != i and D_k in cn[o]}
                    # this is only relevant if y[i][D_k][l_]
                    model.addCons(
                        quicksum(y_okl * s[o][i] for o, y_okl in in_moves.items())
                        - quicksum(y_okl * f[o][i] for o, y_okl in out_moves.items())
                        <= C_l - 1 + (1 - y[i][D_k][l_]) * M,
                    )
        # enforce the h_oikl to have the correct values^
        for idx_o, j_o in J.items():
            if j_o.finish is None:
                for idx_i, j_i in J.items():
                    if j_i.finish is None and idx_o != idx_i:
                        for D_k in cap(used_resources[idx_i], used_resources[idx_o]):
                            for A_kl in range(A[D_k]):
                                s_oi = s[idx_o][idx_i]
                                f_oi = f[idx_o][idx_i]
                                y_okl = y[idx_o][D_k][A_kl]
                                h_oikl = h[idx_o][idx_i][D_k][A_kl]
                                model.addCons(s_oi - f_oi + y_okl <= h_oikl + 1)
                                model.addCons(h_oikl <= s_oi - f_oi)
                                model.addCons(h_oikl <= y_okl)
                                allows_overlap = mc.machines_by_class[D_k][0].allows_overlap
                                if not allows_overlap:
                                    # enforce jobs to either have identical times or not to overlap at all
                                    x_i = x[idx_i]
                                    x_o = x[idx_o]
                                    d_i = d[idx_i]
                                    d_o = d[idx_o]
                                    model.addCons(M - M * h_oikl >= x_i - x_o)
                                    model.addCons(M - M * h_oikl >= x_o - x_i)
                                    model.addCons(M - M * h_oikl >= d_i - d_o)
                                    model.addCons(M - M * h_oikl >= d_o - d_i)
        # enforce the s_io and f_io to have the correct values
        for idx_o, j_o in J.items():
            for idx_i, j_i in J.items():
                if idx_o != idx_i:
                    x_i = x[idx_i]
                    x_o = x[idx_o]
                    s_oi = s[idx_o][idx_i]
                    f_oi = f[idx_o][idx_i]
                    d_o = d[idx_o]
                    if j_i.start is None and j_o.start is None:
                        model.addCons(x_i <= x_o + M * s_oi)
                        model.addCons(x_o <= x_i + M - M * s_oi)
                    if j_o.finish is None and j_i.start is None:
                        model.addCons(x_i <= x_o + d_o + M * f_oi)
                        model.addCons(x_o + d_o <= x_i + M - M * f_oi)
                    # this avoids numerical issues in the corner case, with x_i = x_o
                    if idx_i < idx_o and j_i.start is None and j_o.start is None:
                        model.addCons(s_oi + s[idx_i][idx_o] == 1)
        return JSSPModel(model, T, x, y, s, f, h, ref_time)

    @staticmethod
    def translate_assignments(inst: JSSP, jssp_model: JSSPModel) -> Schedule:
        schedule = {}
        sol = jssp_model.scip_model.getBestSol()
        # translate the solution for y to assignments of jobs to machines
        for idx, job in inst.operations_by_id.items():
            x_var = jssp_model.x[idx]
            start_time = jssp_model.ref_time + timedelta(seconds=sol[x_var])
            machine_assignments = {}
            for used_machine in job.required_machines:
                y_ik_vars = jssp_model.y[idx][used_machine.type]
                # get the rounded values of the binary variables
                y_ik = [round(sol[var]) for var in y_ik_vars]
                if 1 not in y_ik:
                    logger.exception(
                        f"There is no value 1 in y_ik for operation {idx},"
                        f" machine_type {used_machine.type}. y_ik={y_ik}.",
                    )
                    return schedule
                if sum(y_ik) != 1:
                    msg = "Exactly one binary variable should be 1, indicating which machine to use."
                    logger.warning(msg)
                machine_index = y_ik.index(1)
                machine_name = inst.machine_collection.machines_by_class[used_machine.type][machine_index].name
                machine_assignments[used_machine.tag] = machine_name
            schedule[idx] = ScheduledAssignment(start=start_time, machines_to_use=machine_assignments)
        return schedule

    @staticmethod
    def tune_params(m: Model, time_limit: float):
        """
        Some SCIP parameter settings to tune the solver
        """
        m.setParam("limits/time", time_limit)
        m.setParam("numerics/checkfeastolfac", 1e4)
        m.setParam("presolving/abortfac", 0.2)
        m.setParam("presolving/restartfac", 0.1)
        m.setParam("presolving/maxrounds", 2)
        for cons_type in [
            "linear",
            "nonlinear",
            "and",
            "countsols",
            "cumulative",
            "integral",
            "knapsack",
            "linking",
            "logicor",
            "or",
            "orbisack",
            "setppc",
            "symresack",
            "xor",
            "components",
        ]:
            param = f"constraints/{cons_type}/presoltiming"
            m.setParam(param, 4)
        for prob_type in ["probing", "obbt", "redcost", "rootredcost"]:
            param = f"propagating/{prob_type}/presoltiming"
            m.setParam(param, 4)

        m.setParam("propagating/probing/maxprerounds", 2)
        m.setParam("propagating/probing/proprounds", 2)
        m.setParam("propagating/probing/freq", -1)
        m.setParam("heuristics/clique/maxproprounds", 2)
        m.setParam("propagating/probing/maxuseless", 2)
        m.setParam("propagating/probing/maxtotaluseless", 1)
