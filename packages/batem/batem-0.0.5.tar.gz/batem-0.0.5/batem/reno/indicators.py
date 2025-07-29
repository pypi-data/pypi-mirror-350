

from datetime import datetime


def self_consumption(load_by_time: dict[datetime, float],
                     production_by_time: dict[datetime, float]) -> float:
    """
    Calculate the self-consumption ratio of a house.
    """
    if len(load_by_time) != len(production_by_time):
        msg = (f"load_by_time and production_by_time must have the same length"
               f" {len(load_by_time)} != {len(production_by_time)}")
        raise ValueError(msg)

    if len(production_by_time) == 0:
        print("warning: production_by_time is empty")
        return 0

    self_consumption = 0
    total_production = sum(production_by_time.values())
    for timestamp, load in load_by_time.items():
        self_consumption += min(load, production_by_time[timestamp])

    return self_consumption / total_production


def self_sufficiency(load_by_time: dict[datetime, float],
                     production_by_time: dict[datetime, float]) -> float:
    """
    Calculate the self-sufficiency ratio of a house.
    """
    if len(load_by_time) != len(production_by_time):
        msg = (f"load_by_time and production_by_time must have the same length"
               f" {len(load_by_time)} != {len(production_by_time)}")
        raise ValueError(msg)

    if len(production_by_time) == 0:
        print("warning: production_by_time is empty")
        return 0

    if len(load_by_time) == 0:
        print("warning: load_by_time is empty")
        return 0

    self_consumption = 0
    total_consumption = sum(load_by_time.values())
    for timestamp, load in load_by_time.items():
        self_consumption += min(load, production_by_time[timestamp])

    return self_consumption / total_consumption
