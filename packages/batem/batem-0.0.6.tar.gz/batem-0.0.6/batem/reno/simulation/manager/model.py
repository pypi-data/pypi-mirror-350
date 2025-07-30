

from batem.reno.simulation.recommendation import (
    Recommendation, RecommendationType)

from batem.reno.simulation.scheduler.model import Scheduler


class Manager:

    def __init__(self, scheduler: Scheduler):
        self.scheduler = scheduler

    def step(self, k: int) -> Recommendation:
        """
        Run the manager step.
        """
        return Recommendation(RecommendationType.DECREASE)
