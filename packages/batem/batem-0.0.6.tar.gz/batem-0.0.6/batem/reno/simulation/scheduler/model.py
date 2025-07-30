

import csv
from batem.reno.community.creation import CommunityBuilder
from batem.reno.community.model import EnergyCommunity
from batem.reno.simulation.member.model import Member
from batem.reno.simulation.manager.model import Manager
from batem.reno.utils import FilePathBuilder, TimeSpaceHandler, parse_args


class Scheduler:
    def __init__(self, community: EnergyCommunity):
        """
        Initialize the community.
        The number of steps is the number of hours in the simulation period,
        defined by the time space handler of the community.
        """
        self.community = community
        self.steps = len(self.community.time_space_handler.range_hourly)
        self.k = 0

        self.manager = Manager(self)

        self.members: list[Member] = []
        self._create_members()

    def _create_members(self):
        """
        Create the members of the community.
        """
        for house in self.community.houses:
            member = Member(self, house)
            self.members.append(member)

    def run(self):
        """
        Run a simulation step by step.
        A step is an hour.
        """
        for k in range(self.steps):
            self._step(k)

    def _step(self, k: int):
        """
        Run a simulation step.
        """
        recommendation = self.manager.step(k)

        for member in self.members:
            member.step(k, recommendation)

    def to_csv(self):
        """
        Export the simulation results to a CSV file.
        """
        file_path = FilePathBuilder().get_simulation_results_path(
            self.community.time_space_handler)

        header = ["timestamp"]
        for member in self.members:
            header.append(f"member_{member.house.house_id}")
        header.append("manager")
        header.append("pv")

        with open(file_path, "w") as f:
            writer = csv.writer(f)

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


if __name__ == "__main__":
    # python batem/reno/simulation/scheduler/model.py

    args = parse_args()

    time_space_handler = TimeSpaceHandler(
        location=args.location,
        start_date=args.start_date,
        end_date=args.end_date)

    community = CommunityBuilder(time_space_handler
                                 ).build(
        panel_peak_power_kW=8,
        number_of_panels_per_array=1,
        exposure_deg=0.0,
        slope_deg=152.0)

    scheduler = Scheduler(community)
    scheduler.run()
