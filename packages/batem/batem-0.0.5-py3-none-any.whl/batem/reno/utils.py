
import argparse
from datetime import datetime
import os

from pandas import date_range

from batem.core.timemg import stringdate_to_datetime


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--location", type=str,
                        required=False, default="Grenoble")
    parser.add_argument("--start_date", type=str,
                        required=False, default="01/3/1998")
    parser.add_argument("--end_date", type=str,
                        required=False, default="01/3/1999")
    return parser.parse_args()


def get_lat_lon_from_location(location: str) -> tuple[float, float]:
    """
    Get the latitude and longitude from the location.
    """
    if location == "Grenoble":
        return 45.19154994547585, 5.722065312331381
    elif location == "Bucharest":
        return 44.426827, 26.103731
    else:
        raise ValueError(f"Location {location} not supported")


class TimeSpaceHandler:
    def __init__(self, location: str, start_date: str, end_date: str):
        """
        The start and end time are in the format "DD/MM/YYYY".
        """
        self.location: str = location

        latitude_north_deg, longitude_east_deg = get_lat_lon_from_location(
            location)
        self.latitude_north_deg = latitude_north_deg
        self.longitude_east_deg = longitude_east_deg

        self.start_date: str = start_date
        self.end_date: str = end_date

        self.start_time_str: str = f"{start_date} 00:00:00"
        self.end_time_str: str = f"{end_date} 00:00:00"

        self.start_time: datetime = stringdate_to_datetime(
            self.start_time_str, timezone_str="UTC")  # type: ignore
        self.end_time: datetime = stringdate_to_datetime(
            self.end_time_str, timezone_str="UTC")  # type: ignore

        self.range_10_min: list[datetime] = date_range(
            self.start_time, self.end_time).tolist()  # type: ignore
        self.range_hourly: list[datetime] = date_range(
            self.start_time, self.end_time, freq="h").tolist()  # type: ignore

    def get_range_10_min(self) -> list[datetime]:
        return self.range_10_min

    def get_range_hourly(self) -> list[datetime]:
        return self.range_hourly


class FilePathBuilder:
    def __init__(self):
        pass

    def get_irise_db_path(self):
        return os.path.join("data", "irise.sqlite3")

    def get_house_consumption_path(self, house_id: int,
                                   hourly: bool = False):
        """
        Get the path to the house consumption data.
        """
        if hourly:
            file_name = f"{house_id}_consumption_hourly.csv"
        else:
            file_name = f"{house_id}_consumption.csv"

        return os.path.join("batem", "reno", "csv_data", file_name)

    def get_trimmed_house_consumption_path(
            self, house_id: int,
            time_space_handler: TimeSpaceHandler,
            hourly: bool = False) -> str:
        """
        Get the path to the trimmed house consumption data.
        """
        start_time = time_space_handler.start_date.replace("/", "_")
        end_time = time_space_handler.end_date.replace("/", "_")
        if hourly:
            file_name = f"{house_id}_consumption_hourly_trimmed_{start_time}_"
            file_name = f"{file_name}_{end_time}.csv"
        else:
            file_name = f"{house_id}_consumption_trimmed_{start_time}_"
            file_name = f"{file_name}_{end_time}.csv"
        return os.path.join("batem", "reno", "csv_data", file_name)

    def get_pv_plant_path(self, time_space_handler: TimeSpaceHandler):
        """
        Get the path to the PV plant data.
        Start time and end time are in the format "DD/MM/YYYY".
        """
        start_time = time_space_handler.start_date.replace("/", "_")
        end_time = time_space_handler.end_date.replace("/", "_")
        file_name = (f"pv_plant_{time_space_handler.location}_{start_time}_"
                     f"{end_time}.csv")
        return os.path.join("batem", "reno", "csv_data", file_name)

    def get_plots_folder(self) -> str:
        """
        Get the path to the plots folder.
        """
        folder_name = "plots"
        path = os.path.join("batem", "reno", folder_name)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_community_valid_houses_path(
            self, time_space_handler: TimeSpaceHandler) -> str:
        """
        Get the path to the community valid houses file.
        """
        file_name = (f"community_valid_houses_{time_space_handler.location}_"
                     f"{time_space_handler.start_date.replace('/', '_')}_"
                     f"{time_space_handler.end_date.replace('/', '_')}.json")
        return os.path.join("batem", "reno", "community", file_name)
