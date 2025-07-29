import importlib
import itertools
import pkgutil
import time
import traceback
from collections.abc import Iterable
from pathlib import Path
from threading import Lock
from types import ModuleType

import labscheduler.solvers
from labscheduler.dev_tools.eval_schedule import is_feasible_solution
from labscheduler.dev_tools.utilities import parse_jobshop_from_yaml_file
from labscheduler.logging_manager import scheduler_logger as logger
from labscheduler.scheduler_interface import SchedulerInterface
from labscheduler.solver_interface import AlgorithmInfo, JSSPSolver
from labscheduler.solvers.simple_scheduler import SimpleSolver
from labscheduler.solvers.specialized_pd_implementation import LPTF, BottleneckPD
from labscheduler.structures import JSSP, Machine, MoveOperation, Operation, Schedule, SolutionQuality

static_load = False


class Scheduler(SchedulerInterface):
    jssp_solver: JSSPSolver
    available_solvers_by_name: dict[str, type[JSSPSolver]]

    def __init__(
        self,
        algorithm: str = "CP-Solver",
        labconfig_yaml_filename: str = "lab_config_example.yaml",
        labconfig_path: Path | str | None = None,
    ) -> None:
        """
        Other default algorithms are "BottleNeckPD" and "MIP-Solver".
        Other default labconfig_yaml_filenames are "platform_config.yml" and "lara_platform_config.yml"
        Note that the file lara_platform_config is not part of the repository
        """
        if labconfig_path is None:
            labconfig_path = Path(__file__).resolve().parent.parent / "tests" / "test_data"

        if static_load:
            self.static_load_solvers()
        else:
            self.inject_solvers()
        self.computation_lock = Lock()
        self.select_algorithm(algorithm)
        yaml_file_path = Path(labconfig_path) / labconfig_yaml_filename

        if yaml_file_path.is_file():
            with open(yaml_file_path) as reader:
                content = reader.read()
                job_shop = parse_jobshop_from_yaml_file(content)
                self.configure_job_shop(machine_list=job_shop)

    def static_load_solvers(self):
        self.available_solvers_by_name = {
            "BottleneckPD": BottleneckPD,
            "LPTFPD": LPTF,
            "Simple": SimpleSolver,
        }
        try:
            from labscheduler.solvers.cp_solver import CPSolver

            self.available_solvers_by_name["CP-Solver"] = CPSolver
        except ModuleNotFoundError:
            logger.warning("CP-Solver will not be available")
        try:
            from labscheduler.solvers.MIP_solver import MIPSolver

            self.available_solvers_by_name["MIP-Solver"] = MIPSolver
        except ModuleNotFoundError:
            logger.warning("MIP-Solver will not be available")

    def inject_solvers(self):
        """
        Searches for classes implementing the JSSPSolver interface in all modules in the solvers/ directory.
        Any matching Class is added as a solver and made available.
        """
        pck = labscheduler.solvers
        self.available_solvers_by_name = {}
        for _finder, mod_name, ispkg in pkgutil.iter_modules(pck.__path__, prefix=pck.__name__ + "."):
            try:
                submodule = importlib.import_module(mod_name)
                if not ispkg:
                    self._load_solvers_from_module(submodule)
            except ImportError:
                logger.warning(f"Module {mod_name} could not be loaded.")

    def _load_solvers_from_module(self, module: ModuleType):
        """
        Loads potential solver classes from a given module and registers them in the available solvers dictionary.
        """
        for attr in dir(module):
            buff = getattr(module, attr)
            try:
                if issubclass(buff, JSSPSolver):
                    solver_name = buff.get_algorithm_info().name
                    self.available_solvers_by_name[solver_name] = buff
                    logger.info(f"Found solver {buff}")
            except (TypeError, AttributeError):
                logger.debug(f"Attribute {attr} of module {module} could not be recognized as a solver.")

    def configure_job_shop(self, machine_list: list[Machine]):
        self.job_shop = machine_list

    def select_algorithm(self, algorithm_name: str) -> bool:
        """
        Changes the current algorithm of the solver. The names of all available algorithms can be requested
        via the available_algorithms attribute.
        :param algorithm_name: Name of the chosen algorithm.
        :return: Returns whether there is an algorithm with the given name
        """
        if algorithm_name not in self.available_solvers_by_name:
            logger.error(f"Solver named {algorithm_name} not found")
            return False
        # create an instance of the selected solver type
        self.jssp_solver = self.available_solvers_by_name[algorithm_name]()
        return True

    @property
    def available_algorithms(self) -> list[AlgorithmInfo]:
        return [solver.get_algorithm_info() for solver in self.available_solvers_by_name.values()]

    @property
    def current_algorithm_info(self) -> AlgorithmInfo:
        return self.jssp_solver.get_algorithm_info()

    def compute_schedule(
        self,
        operations: Iterable[Operation],
        computation_time: float,
    ) -> tuple[Schedule | None, SolutionQuality]:
        try:
            start = time.time()
            # FIXme: change to context manager
            self.computation_lock.acquire()
            jssp = JSSP(operations=operations, machines=self.job_shop)
            # compute the schedule
            jssp.add_dummys()
            logger.info(f"Computing schedule for {len(list(operations))} operations")
            schedule, quality = self.jssp_solver.compute_schedule(jssp, computation_time, computation_time)
            if not is_feasible_solution(inst=jssp, sol=schedule):
                if quality in {SolutionQuality.OPTIMAL, SolutionQuality.FEASIBLE}:
                    logger.warning("Solver marked the solution as feasible, but it is not.")
                quality = SolutionQuality.INFEASIBLE
            if quality == SolutionQuality.INFEASIBLE:
                logger.warning("The computed solution is not feasible")
            if schedule:
                jssp.remove_dummys(schedule)
                if quality != SolutionQuality.INFEASIBLE:
                    self._enforce_precedences(schedule)
                    self._enforce_min_capacities(list(operations), schedule)
            logger.info(f"Computation took {time.time() - start} seconds. Solution is {quality.name}")
        except Exception:  # noqa: BLE001
            logger.exception(traceback.print_exc())
            return None, SolutionQuality.INFEASIBLE
        else:
            return schedule, quality
        finally:
            self.computation_lock.release()

    def _enforce_precedences(self, schedule: Schedule):
        """
        Adds machine precedences between steps that definitively need to be executed without overlapping.
        This is already implicitly given by the schedule, but adding it explicitly might help executing the schedule.
        :param schedule:
        :return:
        """
        # get the names of all devices with a capacity of one
        machine_names = [machine.name for machine in self.job_shop if machine.max_capacity == 1]
        for name in machine_names:
            # get all the steps on this device
            steps = [idx for idx, assign in schedule.items() if assign.machines_to_use["main"] == name]
            sorted_steps = sorted(steps, key=lambda idx: schedule[idx].start)
            for step1, step2 in itertools.pairwise(sorted_steps):
                schedule[step2].machine_precedences.append(step1)

    def _enforce_min_capacities(self, operations: list[Operation], schedule: Schedule):
        """
        Searches for movements, that are necessary for certain operations due to minimum capacities.
        Adds machine precedence constraints between those
        :param schedule:
        :return:
        """
        try:
            # sort all movements by start time
            movements = [op for op in operations if isinstance(op, MoveOperation)]
            sorted_moves = sorted(movements, key=lambda m: schedule[m.name].start)
            machine_by_name: dict[str, Machine] = {m.name: m for m in self.job_shop}
            for idx, assignment in schedule.items():
                main_name = assignment.machines_to_use["main"]
                main = machine_by_name[main_name]
                if main.min_capacity > 1:
                    # filter all movements, that involve the main device and start before this operation
                    relevant_moves = [
                        m
                        for m in sorted_moves
                        if main_name in schedule[m.name].machines_to_use.values()
                        and schedule[m.name].start < assignment.start
                    ]
                    # find the last movement, that gets the min capacity fulfilled and enforce precedence
                    curr_load = 0
                    deciding_filler = None
                    # will be all loadings since the last unloading
                    load_moves = []
                    for move in relevant_moves:
                        # elegant way to cover the edge case when both origin and target are main_name
                        change = int(schedule[move.name].machines_to_use["target"] == main_name) - int(
                            schedule[move.name].machines_to_use["origin"] == main_name,
                        )
                        if curr_load < main.min_capacity <= curr_load + change:
                            deciding_filler = move
                        if change >= 0:
                            load_moves.append(move)
                        else:
                            load_moves = []
                        curr_load += change
                    if deciding_filler:
                        logger.debug(
                            f"for operation {idx}, we have deciding filler {deciding_filler.name}"
                            f" and loading operations {[m.name for m in load_moves]}",
                        )
                        if main.allows_overlap:
                            # enforce precedence of the deciding filler
                            assignment.machine_precedences.append(deciding_filler.name)
                        else:
                            # if interrupts are not allowed also enforce precedence to all loadings since last unloading
                            for move in load_moves:
                                assignment.machine_precedences.append(move.name)
                    else:
                        logger.warning(f"The device executing {idx} seems to be not sufficiently filled")
        except Exception:  # noqa: BLE001
            logger.debug(schedule)
            logger.exception(f"In _enforce_min_capacities\n{traceback.print_exc()}")
