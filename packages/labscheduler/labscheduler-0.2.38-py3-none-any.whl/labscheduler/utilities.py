"""
A collection of useful functions to use the labscheduler.
"""

import re
from datetime import datetime, timedelta

from labscheduler.structures import MoveOperation, Operation, RequiredMachine


def create_operations_from_json(workflow_graph):
    operation_by_id = {}
    for node in workflow_graph[0]:
        idx = node[0]
        duration = node[1]
        start = None if node[3] == "None" else datetime.fromisoformat(node[3])
        finish = None if node[4] == "None" else datetime.fromisoformat(node[4])
        requirements = [
            RequiredMachine(type=rm[0], tag=rm[1], preferred=None if rm[2] == "None" else rm[2]) for rm in node[2]
        ]
        is_movement = "target" in [rm.tag for rm in requirements]
        if is_movement:
            operation = MoveOperation(
                name=idx,
                duration=duration,
                required_machines=requirements,
                start=start,
                finish=finish,
            )
        else:
            operation = Operation(
                name=idx,
                duration=duration,
                required_machines=requirements,
                start=start,
                finish=finish,
            )
        operation_by_id[idx] = operation
    for edge in workflow_graph[1]:
        u = edge[1]
        v = edge[0]
        operation_by_id[v].preceding_operations.append(u)
        # for stability reasons we want wait_costs
        operation_by_id[v].wait_cost[u] = edge[2]
        operation_by_id[v].max_wait[u] = edge[3]
        min_wait = 0 if not edge[4] else edge[4]
        operation_by_id[v].min_wait[u] = min_wait
    return operation_by_id


def extract_timestamp(filename: str) -> datetime | None:
    match = re.search(r"(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})", filename)
    if match:
        y, mo, d, h, mi, s = map(int, match.groups())
        return datetime(y, mo, d, h, mi, s)
    return None


def add_timedelta_to_datetimes(data: list | dict | str, delta: timedelta):
    """
    Recursively traverse the JSON structure and add a given timedelta
    to any string that is a valid datetime in ISO format.

    Parameters:
        data: The JSON-loaded data (can be list, dict, or other types)
        delta: A datetime.timedelta object to add to found datetimes

    Returns:
        Updated data with all datetime strings incremented by delta.
    """
    if isinstance(data, list):
        # Process each element in the list recursively.
        return [add_timedelta_to_datetimes(item, delta) for item in data]
    if isinstance(data, dict):
        # Process each key-value pair recursively.
        return {key: add_timedelta_to_datetimes(value, delta) for key, value in data.items()}
    if isinstance(data, str):
        # Skip if the string is "None" or does not look like a datetime.
        if data == "None":
            return data
        try:
            # Try parsing the string as a datetime.
            dt = datetime.fromisoformat(data)
            new_dt = dt + delta
            # Return the new datetime as a string in the same format.
            return new_dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            # Not a datetime string; return as is.
            return data
    else:
        # For other data types (e.g., numbers), return as is.
        return data
