"""
A python script to evaluate multiple solvers of a given test set.
The results will be saved in json format with a timestamp and as a latex table (algo_eval_table.tex)
Both will be saved in ./table/. You can subsequently call
$ pdflatex table.tex
to produce a pdf file from the results.
solving time and the directory containing the test files can be set via commands line. Defaults and further settings
can be configured in algo_eval_config.py.
Example call:
$ python labschedulerools/algo_eval.py -d tests/test_data/benchmark_inst/
"""

import argparse
import json
import logging
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from labscheduler.dev_tools import algorithm_eval_config as cfg
from labscheduler.dev_tools.eval_schedule import is_feasible_solution, objective_value
from labscheduler.dev_tools.utilities import parse_jobshop_from_yaml_file
from labscheduler.scheduler_implementation import Scheduler
from labscheduler.structures import JSSP, Machine, Schedule
from labscheduler.utilities import create_operations_from_json

logger = logging.getLogger(__name__)


def get_lab() -> list[Machine]:
    with open(cfg.lab_config_file) as reader:
        return parse_jobshop_from_yaml_file(reader.read())


def run_test_series(
    scheduler: Scheduler,
    algorithm_name: str,
    test_instances: list[str | Path],
    time_limit: int,
) -> tuple[list[Schedule], list[float]]:
    scheduler.select_algorithm(algorithm_name)
    scheduler.configure_job_shop(get_lab())
    results = []
    times = []
    for filename in test_instances:
        if Path(filename).suffix == ".json":
            with open(filename) as reader:
                sila_wfg = json.load(reader)
            logger.info(f"testing {Path(filename).stem}")
            op_by_id = create_operations_from_json(sila_wfg)
            start_computation = time.time()
            schedule, _quality = scheduler.compute_schedule(op_by_id.values(), time_limit)
            times.append(time.time() - start_computation)
            results.append(schedule)
    return results, times


def createJSSPs(files: list[str]):
    instances = []
    for filename in files:
        with open(filename) as reader:
            sila_wfg = json.load(reader)
        op_by_id = create_operations_from_json(sila_wfg)
        jssp = JSSP(op_by_id.values(), get_lab())
        instances.append(jssp)
    return instances


def parse_command_line():
    """Looking for command line arguments"""
    parser = argparse.ArgumentParser(description="Algorithm evaluation")
    parser.add_argument("-d", "--test_data", action="store", default=cfg.default_test_data)
    return parser.parse_args()


def gap_tostring(gap: float) -> str:
    if cfg.add_percentage_sign:
        return f"{gap} \\,\\%"
    return f"{gap}"


def make_latex_table(data: list[dict[str, str | float | None]]):
    # add artificial/real column
    for row in data:
        row["real"] = "Yes" if row["real"] else "No"

        objective_values = [row[algo] for algo in cfg.algorithms if row[algo] != "FAIL"]
        # nothing to do if no algorithm found a result
        if not objective_values:
            continue
        best_objective_found = min(objective_values)
        for algo in cfg.algorithms:
            # show the results as difference to the best found solution as percentage
            if row[algo] != "FAIL":
                gap = round((row[algo] / best_objective_found - 1) * 100, 2)
                # changes 0.0 to 0
                if int(gap) == gap:
                    gap = int(gap)
                row[algo] = gap_tostring(gap)
                # check whether the algorithm definitely found the optimum
                solution_optimal = algo in cfg.exact_algorithms and row[f"T_{algo}"] < cfg.time_limit and gap == 0
                if solution_optimal:
                    row[algo] = "opt"
                # make the best result bold
                if not gap:
                    row[algo] = "\\textbf{" + row[algo] + "}"

        # round times to two digits after comma
        for key, val in row.items():
            if "T_" in key:
                row[key] = f"{round(max(val, 0.01), 2)}\\,s"
    # create a data frame
    data_frame_latex = pd.DataFrame(data)
    logger.info(data_frame_latex)
    # sort rows and columns
    data_frame_latex = data_frame_latex.sort_values(by="size")
    if cfg.add_additional_columns:
        order = cfg.new_order
        header = cfg.new_header
        cfg.col_format += "|rr" * len(cfg.additional_columns)
    else:
        order = cfg.standard_order
        header = cfg.standard_header

    # create the .tex file
    data_frame_latex = data_frame_latex.sort_values(by="size").loc[:, order]
    data_frame_latex.to_latex(
        buf=(cfg.table_dir / "algo_eval_table.tex").as_posix(),
        header=header,
        column_format=cfg.col_format,
        index=False,
    )


def transfer_results(data: list[dict[str, str | float | None]], transfer_to: str, transfer_from: str):
    """
    Used the better result of the two algorithms transfer_to and transfer_from as result for transfer_to.
    That is useful when theoretical one algorithm (usually a heuristic) is used as primal heuristic for the other
    algorithm, but due to errors on the underlying solver (SCIP or ortools) side, the results gets not transferred.
    """
    if {transfer_to, transfer_from}.issubset(cfg.algorithms):
        for row in data:
            result1 = None if row[transfer_to] == "FAIL" else row[transfer_to]
            result2 = None if row[transfer_from] == "FAIL" else row[transfer_from]
            # if only transfer_from found a result or it found a better one we copy its result to transfer_to
            if (result1 and not result2) or (result1 and result2 and result2 < result1):
                row[transfer_to] = row[transfer_from]
                logger.info(f"taking result from {transfer_from} on {row['Instance']} for {transfer_to}")


if __name__ == "__main__":
    args = parse_command_line()
    if cfg.use_existing_results:
        raw_df = pd.read_json(cfg.existing_results)
    else:
        testfiles = [file for file in Path(args.test_data).iterdir() if file.suffix == ".json"]
        instances = createJSSPs(testfiles)

        logger.info(cfg.algorithms)
        logger.info("\n".join(str(t) for t in testfiles))
        results = {}
        times = {}
        scheduler = Scheduler()
        for algo in cfg.algorithms:
            results[algo], times[algo] = run_test_series(
                scheduler,
                algo,
                test_instances=testfiles,
                time_limit=cfg.time_limit,
            )
        data = []
        for num, test_file in enumerate(testfiles):
            row = {}
            inst = instances[num]
            row["Instance"] = Path(test_file).stem
            row["size"] = len(instances[num].operations_by_id)
            row["real"] = row["Instance"] in cfg.real_instances
            for algo in cfg.algorithms:
                schedule = results[algo][num]
                is_feasible = is_feasible_solution(inst, schedule)
                if is_feasible:
                    row[algo] = round(objective_value(inst, schedule), 1)
                else:
                    row[algo] = "FAIL"
                row[f"T_{algo}"] = round(times[algo][num], 1)
            data.append(row)
        raw_df = pd.DataFrame(data)
        raw_df.to_json(cfg.table_dir / f"data{datetime.today()}.json")
    data = raw_df.to_dict("records")
    logger.info(raw_df)

    for transfer_to, transfer_from in cfg.transfer_results:
        transfer_results(data, transfer_to, transfer_from)

    if not Path.exists(cfg.additional_data):
        logger.error(f"data file {cfg.additional_data} does not exist. Proceeding without additional data")
        cfg.add_additional_data = False

    if cfg.add_additional_columns:
        df3 = pd.read_json(cfg.additional_data)
        add_data = df3.to_dict("records")
        for col, new_name in cfg.additional_columns:
            cfg.algorithms.append(new_name)
            for new_row, row in zip(add_data, data):
                row[new_name] = new_row[col]
                row["T_" + new_name] = new_row["T_" + col]

    make_latex_table(data)
