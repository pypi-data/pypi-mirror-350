import os
from batem.reno.community.model import EnergyCommunity
from batem.reno.community.time_checker import TimeChecker
from batem.reno.house.creation import HouseBuilder
from batem.reno.house.model import House
from batem.reno.utils import FilePathBuilder, TimeSpaceHandler, parse_args


class CommunityBuilder:
    def __init__(self, time_space_handler: TimeSpaceHandler):
        self.time_space_handler: TimeSpaceHandler = time_space_handler

    def generate_houses_consumption_csv(self):
        """
        Generate the consumption CSV files for the houses.
        Its easier to generate the CSV files for the houses
        and then use them to build the community.
        """
        valid_houses_ids = TimeChecker(
            self.time_space_handler).get_valid_houses_ids_from_json()

        for house_id in valid_houses_ids:
            house = HouseBuilder().build_house_by_id(house_id)
            path = FilePathBuilder().get_house_consumption_path(house.house_id)
            house.to_csv(path)

    def build(self):
        """
        Build the community.
        """
        self._check_and_generate_houses_consumption_csv()

        houses = self.get_valid_houses_from_csv()

        community = EnergyCommunity(self.time_space_handler)
        community.houses = houses
        community.compute_total_consumption()
        return community

    def _check_and_generate_houses_consumption_csv(self):
        """
        Check if the houses consumption CSV files exist.
        If not, generate them.
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
        Get the houses from the CSV files.
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
    community = CommunityBuilder(time_space_handler).build()
