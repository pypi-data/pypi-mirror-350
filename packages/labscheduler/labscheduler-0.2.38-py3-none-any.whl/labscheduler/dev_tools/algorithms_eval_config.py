from pathlib import Path

# directory containing all test instances
default_test_data = Path(__file__).resolve().parent.parent.parent / "tests" / "test_data" / "benchmark_inst"
# where to write the results
table_dir = Path(__file__).resolve().parent / "table"
# the lab configuration file to use for the solver
lab_config_file = default_test_data / "lab_config_example.yaml"

time_limit = 60  # in seconds

# to create a result table using existing results.
# No computation is dene in that case
use_existing_results = True
# json file containing the existing results
existing_results = table_dir / "data_with_heur.json"

# list of algorithms to test
algorithms = [
    "LPTFPD",
    "BottleneckPD",
    "MIP-Solver",
    "CP-Solver",
]
short_name = {
    "LPTFPD": "LPTF",
    "BottleneckPD": "PDH",
    "MIP-Solver": "MIP",
    "CP-Solver": "CP",
}
# list of algorithms that can prove optimality, i.e.,
# a list of columns where a an optimality gap of 0 and not fully used runtime will result in an 'opt' in the results
exact_algorithms = [
    "MIP-Solver",
    "CP-Solver",
    "only_cp",
    "only_mip",
]

# a list of which instances will be marked as real world problems
real_instances = [
    "SolvabilityAssay",
    "Repetitive4PlateProcess",
    "KWETransaminaseAssay",
    "CultivationHarvest",
    "Repetitive12Plates",
    "Kinetic2Plates",
]

# Configurations for the resulting table format
add_percentage_sign = False
transfer_results = [
    ("MIP-Solver", "BottleneckPD"),
    ("MIP-Solver", "LPTFPD"),
    ("CP-Solver", "BottleneckPD"),
    ("CP-Solver", "LPTFPD"),
]
add_additional_columns = False
additional_data = table_dir / "data_no_heur.json"
# given as tuples (original name, new name)
additional_columns = [("CP-Solver", "only_cp"), ("MIP-Solver", "only_mip")]
new_order = [
    "size",
    "real",
    "LPTFPD",
    "T_LPTFPD",
    "BottleneckPD",
    "T_BottleneckPD",
    "only_mip",
    "T_only_mip",
    "MIP-Solver",
    "T_MIP-Solver",
    "only_cp",
    "T_only_cp",
    "CP-Solver",
    "T_CP-Solver",
]
new_header = [
    "size",
    "real",
    "LPTF",
    "time",
    "PDH",
    "time",
    "MIP",
    "time",
    "MIP$^+$",
    "time",
    "CP",
    "time",
    "CP$^+$",
    "time",
]

# table layout
col_format = "l|l" + "|rr" * len(algorithms)
standard_order = ["size", "real"]
standard_header = ["size", "real"]
for algorithm in algorithms:
    standard_order.extend([algorithm, f"T_{algorithm}"])
    standard_header.extend([short_name[algorithm], "time"])
