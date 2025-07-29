import logging

import yaml

from labscheduler.structures import Machine

logger = logging.getLogger(__name__)


def parse_jobshop_from_yaml_file(yaml_file: str) -> list[Machine]:
    """
    Parses a YAML file to create a list of Machine objects.
    The YAML file should contain a dictionary with two keys:
    - pythonlab_translation: a dictionary mapping device types to their corresponding classes
    - sila_servers: a dictionary where each key is a device type and the value is a list of devices
    with their parameters.
    Each device in the sila_servers list should have a name and a dictionary of parameters,
    including capacity, min_capacity, process_capacity, and allows_overlap.
    The function returns a list of Machine objects created from the data in the YAML file.

    """
    config_dict = yaml.safe_load(yaml_file)
    pythonlab_translation = dict(config_dict["pythonlab_translation"])
    job_shop = []
    for device_type, device_list in config_dict["sila_servers"].items():
        device_class = pythonlab_translation[device_type]
        for device_name, param_dict in device_list.items():
            max_capacity = param_dict["capacity"]
            min_capacity = param_dict.get("min_capacity", 1)
            process_capacity = param_dict.get("process_capacity", max_capacity)
            allows_overlap = bool(param_dict["allows_overlap"]) if "allows_overlap" in param_dict else True
            job_shop.append(
                Machine(
                    name=device_name,
                    max_capacity=max_capacity,
                    type=device_class,
                    min_capacity=min_capacity,
                    process_capacity=process_capacity,
                    allows_overlap=allows_overlap,
                ),
            )

    logger.info("Available instruments:")
    for m in job_shop:
        logger.info(m)
    return job_shop
