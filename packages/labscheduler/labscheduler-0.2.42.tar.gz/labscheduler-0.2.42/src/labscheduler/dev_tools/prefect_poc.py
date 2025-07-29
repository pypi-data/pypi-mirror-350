import time

from prefect import flow, task


@task(name="Incubate")
def incubate(labware: str, duration: float):
    time.sleep(duration)
    return labware


@task(name="Move")
def move(labware: str, target: str):
    time.sleep(1)
    return labware


@task(name="Pipett")
def transfer_liquid(labware1, labware2, protocol_name: str):
    time.sleep(2)
    return labware1, labware2


@flow
def example_workflow():
    plate1 = "plate1"
    plate2 = "plate2"

    plate1 = incubate(plate1, 5)
    plate1 = move(plate1, "Liquid Handler")
    plate2 = incubate(plate2, 5)
    plate2 = move(plate2, "Liquid Handler")
    # does not work to have plate1 and plate2 in some structure
    # like for example transfer_liquid([plate1, plate2], "transfer_100yl.pro", "buff")
    transfer_liquid(plate1, plate2, "transfer_100yl.pro")


if __name__ == "__main__":
    example_workflow.visualize()
