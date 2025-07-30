import os
from batem.reno.community.model import EnergyCommunity
from batem.reno.community.time_checker import TimeChecker
from batem.reno.house.creation import HouseBuilder
from batem.reno.house.model import House
from batem.reno.pv.creation import PVPlantBuilder
from batem.reno.utils import FilePathBuilder, TimeSpaceHandler, parse_args


class CommunityBuilder:
    def __init__(self, time_space_handler: TimeSpaceHandler):
        self.time_space_handler: TimeSpaceHandler = time_space_handler

    def generate_houses_consumption_csv(self):
        """
        Generate the 10min consumption CSV files for the houses.
        Its easier to generate the CSV files for the houses
        and then use them to build the community.
        Only the valid houses are used.
        """
        valid_houses_ids = TimeChecker(
            self.time_space_handler).get_valid_houses_ids_from_json()

        for house_id in valid_houses_ids:
            house = HouseBuilder().build_house_by_id(house_id)
            path = FilePathBuilder().get_house_consumption_path(house.house_id)
            house.to_csv(path)

    def build(self, panel_peak_power_kW: float,
              number_of_panels_per_array: int,
              exposure_deg: float = 0.0,
              slope_deg: float = 152.0):
        """
        Build the community.
        """
        self._check_and_generate_houses_consumption_csv()

        houses = self.get_valid_houses_from_csv()

        community = EnergyCommunity(self.time_space_handler)
        community.houses = houses
        community.compute_total_consumption()

        community.pv_plant = PVPlantBuilder().build(
            time_space_handler=self.time_space_handler,
            exposure_deg=exposure_deg,
            slope_deg=slope_deg,
            peak_power_kW=panel_peak_power_kW,
            number_of_panels_per_array=number_of_panels_per_array)

        return community

    def _check_and_generate_houses_consumption_csv(self):
        """
        Check if the houses consumption CSV files exist.
        If not, generate them.
        The trimmed consumption CSV files are used to build the community.
        The trimmed consumption is the consumption
        between the start and end date
        of the simulation period.
        """
        valid_houses_ids = TimeChecker(
            self.time_space_handler).get_valid_houses_ids_from_json()

        for house_id in valid_houses_ids:
            path = FilePathBuilder().get_trimmed_house_consumption_path(
                house_id, self.time_space_handler)
            if not os.path.exists(path):
                house = HouseBuilder().build_house_by_id(house_id)
                house.trim_consumption(self.time_space_handler)
                house.to_csv(path)

    def get_valid_houses_from_csv(self) -> list[House]:
        """
        Get the houses from the trimmed consumption CSV files.
        The trimmed consumption is the consumption
        between the start and end date
        of the simulation period.
        """
        valid_houses_ids = TimeChecker(
            self.time_space_handler).get_valid_houses_ids_from_json()

        houses: list[House] = []

        for house_id in valid_houses_ids:
            path = FilePathBuilder().get_trimmed_house_consumption_path(
                house_id, self.time_space_handler)
            house = HouseBuilder().build_house_from_csv(house_id, path)
            houses.append(house)

        return houses


if __name__ == "__main__":
    # python batem/reno/community/creation.py

    args = parse_args()

    time_space_handler = TimeSpaceHandler(
        location=args.location,
        start_date=args.start_date,
        end_date=args.end_date)

    community = CommunityBuilder(time_space_handler).build(
        panel_peak_power_kW=8,
        number_of_panels_per_array=1,
        exposure_deg=0.0,
        slope_deg=152.0
    )
