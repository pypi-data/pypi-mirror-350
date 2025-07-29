"""
A simple commandline script to run the scheduler on a specific instance with a specific solver.
Lab_config file, timelimit and solver can be set via command line options.
Example usage:
python schedule_problem.py tests/test_data/IncubateAbsorbance.json -t 20 -s CP-Solver
"""

import json
import logging
import re
import time
from datetime import datetime
from pathlib import Path

import typer
from typer import Argument, Option

from labscheduler.dev_tools.utilities import parse_jobshop_from_yaml_file
from labscheduler.scheduler_implementation import Scheduler
from labscheduler.structures import Operation
from labscheduler.utilities import create_operations_from_json

logger = logging.getLogger(__name__)


def extract_timestamp(filename: str) -> datetime | None:
    match = re.search(r"(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})", filename)
    if match:
        y, mo, d, h, mi, s = map(int, match.groups())
        return datetime(y, mo, d, h, mi, s)
    return None


def adapt_times(operations: list[Operation], timestamp: datetime):
    """
    Adds the difference between now and the given timestamp to start and finish of all operations it that is not None
    and thereby reverts the problem to the state at timestamp.
    """
    diff = datetime.now() - timestamp
    for op in operations:
        if op.start:
            op.start += diff
        if op.finish:
            op.finish += diff


def main(
    instance: str = Argument(help="The JSON or Python file containing the instance to solve."),
    lab_config: str | None = Option(
        None,
        "-l",
        help="The lab configuration file. If none is provided, the default configuration "
        "(default argument in the Scheduler constructor) is used.",
    ),
    solver: str = Option("BottleneckPD", "-s", help="Name of the solver to use."),
    time_limit: float = Option(3, "-t", help="Time limit for the solver in seconds."),
):
    """
    Solves a scheduling problem instance using the specified solver and configuration.

    Args:
        instance: Path to the problem instance file. Must be a JSON or Python file.
        lab_config: Path to the lab configuration file. Optional.
        solver: Name of the solver to use. Defaults to "BottleneckPD".
        time_limit: Time limit for the solver in seconds. Defaults to 3 seconds.

    The instance file can either be:
    - A JSON file containing the problem description.
    - A Python file (requires the laborchestrator package for PythonLab descriptions).

    If a lab configuration file is provided, it will be used to configure the job shop.
    """
    scheduler = Scheduler()
    scheduler.select_algorithm(solver)

    if lab_config:
        if not Path.exists(Path(lab_config)):
            logger.error(f"File {lab_config} does not exist.")
            return
        with open(lab_config) as reader:
            content = reader.read()
            try:
                job_shop = parse_jobshop_from_yaml_file(content)
                scheduler.configure_job_shop(machine_list=job_shop)
            except Exception:
                logger.exception(f"Failed to parse Job Shop from file {lab_config}. Wrong format?")

    filepath = Path(instance)
    if filepath.suffix == ".py":
        try:
            problem = []
            # TODO: create the problem using the PythonLab reader
        except ModuleNotFoundError:
            logger.exception("To schedule problems in PythonLab description, install the laborchestrator.")
            return
    elif filepath.suffix == ".json":
        if not Path.exists(filepath):
            logger.info(f"Problem file {instance} does not exist.")
            return
        with open(filepath) as reader:
            sila_wfg = json.load(reader)
        problem = create_operations_from_json(sila_wfg)
        if extract_timestamp(filepath.name):
            adapt_times(list(problem.values()), extract_timestamp(filepath.name))
    else:
        msg = f"{instance} must be a Python or JSON file."
        raise ValueError(msg)
    logger.info(f"Problem has {len(problem)} operations.")
    start = time.time()
    schedule, quality = scheduler.compute_schedule(problem.values(), time_limit)
    print(f"Solution is {quality} after {time.time() - start} seconds.")  # noqa: T201


if __name__ == "__main__":
    typer.run(main)
