

from enum import Enum


class RecommendationType(Enum):
    NONE = "none"
    INCREASE = "increase"
    DECREASE = "decrease"


class Recommendation:
    def __init__(self, type: RecommendationType):
        self.type = type
