import csv
from datetime import datetime
from typing import Optional
import pandas as pd
from batem.reno.constants import APPLIANCES
from batem.reno.utils import TimeSpaceHandler


class House:
    def __init__(self, house_id: int,
                 zip_code: Optional[str] = None,
                 location: Optional[str] = None,
                 weather_station_id: Optional[int] = None):
        self.house_id = house_id
        self.zip_code = zip_code
        self.location = location
        self.weather_station_id = weather_station_id
        self.start_time: datetime
        self.end_time: datetime

        self.appliances: list[Appliance] = []
        self.total_consumption_10min: dict[datetime, float] = {}
        self.total_consumption_hourly: dict[datetime, float] = {}

    def set_total_consumption(self):
        """
        Set the total consumption for a house based on the appliances.
        Sums the consumption of all appliances for each timestamp.
        """
        # Get 10-minute consumption
        self.total_consumption_10min = self._sum_consumption_by_timestamp(
            [appliance.consumption_10min for appliance in self.appliances]
        )

        # Get hourly consumption by properly grouping 10-minute data
        # This properly aggregates all 10-minute readings within each hour
        # We do this because resmapling adds the timestamp for DST transitions
        consumption_series = pd.Series(self.total_consumption_10min)
        hourly_consumption = consumption_series.groupby(
            consumption_series.index.floor('h')  # type: ignore
        ).sum()

        self.total_consumption_hourly = hourly_consumption.to_dict()

    def _sum_consumption_by_timestamp(
        self,
        consumption_dicts: list[dict[datetime, float]]
    ) -> dict[datetime, float]:
        """
        Sum consumption values across multiple dictionaries for each timestamp.

        Args:
            consumption_dicts: List of consumption dictionaries to sum

        Returns:
            Dictionary with summed consumption values for each timestamp
        """
        # Get all unique timestamps
        all_timestamps = set()
        for consumption_dict in consumption_dicts:
            all_timestamps.update(consumption_dict.keys())

        # Sum consumption for each timestamp
        return {
            timestamp: sum(
                consumption_dict.get(timestamp, 0.0)
                for consumption_dict in consumption_dicts
            )
            for timestamp in sorted(all_timestamps)
        }

    def to_csv(self, path: str, hourly: bool = False):
        """
        Save the house data to a CSV file.
        The CSV file is expected to have a header
        row with the following format:
        timestamp,total,appliance_1,appliance_2,...
        The timestamp is expected to be in the format YYYY-MM-DD HH:MM:SS.
        The total consumption is expected to be in kW.
        The other columns are the consumption of each appliance in kW.
        """

        if hourly:
            consumption_by_time = self.total_consumption_hourly
        else:
            consumption_by_time = self.total_consumption_10min

        with open(path, "w") as f:
            writer = csv.writer(f)

            header = ["timestamp", "total"]
            for appliance in self.appliances:
                key = f'{appliance.ID}_{appliance.name}_{appliance.type.value}'
                header.append(key)
            writer.writerow(header)

            for timestamp, consumption in consumption_by_time.items():

                result = {'timestamp': timestamp, 'total': consumption}
                for appliance in self.appliances:
                    if hourly:
                        if timestamp in appliance.consumption_hourly:
                            appliance_consumption = \
                                appliance.consumption_hourly[timestamp]
                        else:
                            appliance_consumption = 0.0
                    else:
                        if timestamp in appliance.consumption_10min:
                            appliance_consumption = \
                                appliance.consumption_10min[timestamp]
                        else:
                            appliance_consumption = 0.0
                    result[appliance.name] = appliance_consumption
                writer.writerow(result.values())

        print(f"House {self.house_id} saved to csv.")

    def trim_consumption(self, time_space_handler: TimeSpaceHandler):
        """
        Trim the consumption data to the given start and end times.
        """

        for appliance in self.appliances:
            appliance.trim_consumption(time_space_handler)
        self.set_total_consumption()
        self.start_time = time_space_handler.start_time
        self.end_time = time_space_handler.end_time
        print(
            (f"House {self.house_id} trimmed consumption"
             f" from {self.start_time} to {self.end_time}"))


class Appliance:
    def __init__(self, ID: int,
                 house: House, name: str,
                 type_name: APPLIANCES,
                 consumption_10min: dict[datetime, float]):
        """
        Consumption is stored in kW.
        """
        self.ID = ID
        self.house = house
        self.name = name
        self.type = type_name
        self.consumption_10min = consumption_10min
        self.consumption_hourly = self._get_consumption_hourly()

    def _get_consumption_hourly(self) -> dict[datetime, float]:
        """
        Get the consumption data for an appliance in hourly intervals.
        Using floor('h') instead of resample('h') to prevent creating
        extra timestamps during DST transitions.
        """
        consumption_series = pd.Series(self.consumption_10min)
        hourly_consumption = consumption_series.groupby(
            consumption_series.index.floor('h')  # type: ignore
        ).sum()
        return hourly_consumption.to_dict()

    def trim_consumption(self, time_space_handler: TimeSpaceHandler):
        """
        Trim the consumption data to the given start and end times.
        """
        start_time = time_space_handler.start_time
        end_time = time_space_handler.end_time

        if start_time > end_time:
            msg = (f"start_time must be before end_time"
                   f" {start_time} > {end_time}")
            raise ValueError(msg)

        if self.house.start_time is None:
            msg = (f"house start time is not set"
                   f" {self.house.start_time}")
            raise ValueError(msg)

        if self.house.end_time is None:
            msg = (f"house end time is not set"
                   f" {self.house.end_time}")
            raise ValueError(msg)

        if start_time < self.house.start_time:
            msg = (f"start_time must be after the house start time"
                   f" {start_time} < {self.house.start_time}")
            raise ValueError(msg)

        if end_time > self.house.end_time:
            msg = (f"end_time must be before the house end time"
                   f" {end_time} > {self.house.end_time}")
            raise ValueError(msg)

        self.consumption_10min = {
            k: v for k, v in self.consumption_10min.items()
            if k >= start_time and k <= end_time}
        self.consumption_hourly = {
            k: v for k, v in self.consumption_hourly.items()
            if k >= start_time and k <= end_time}
