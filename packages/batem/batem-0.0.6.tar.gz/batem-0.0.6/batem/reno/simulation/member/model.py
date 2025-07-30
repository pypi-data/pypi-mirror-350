
from batem.reno.house.model import House
from batem.reno.simulation.recommendation import (
    Recommendation, RecommendationType)
from batem.reno.simulation.scheduler.model import Scheduler


class Member:
    def __init__(self, scheduler: Scheduler, house: House):
        self.scheduler = scheduler
        self.house = house
        self.init_consumption()

    def init_consumption(self):
        """
        Initialize the expected and simulated consumption.
        """
        self.exp_consumption = self.house.total_consumption_hourly.copy()
        self.sim_consumption = {date: 0.0 for date in self.exp_consumption}

    def step(self, k: int, recommendation: Recommendation):
        """
        Run the member step.
        """
        time_space_handler = self.scheduler.community.time_space_handler
        current_datetime = time_space_handler.get_datetime_from_k(k)

        if recommendation.type == RecommendationType.DECREASE:
            self.sim_consumption[current_datetime] = (
                self.exp_consumption[current_datetime] * 0.9)
        elif recommendation.type == RecommendationType.INCREASE:
            self.sim_consumption[current_datetime] = (
                self.exp_consumption[current_datetime] * 1.1)
        else:
            self.sim_consumption[current_datetime] = (
                self.exp_consumption[current_datetime])
