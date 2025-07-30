

from batem.reno.member.model import Member
from batem.reno.scheduler.model import Scheduler


class MemberBuilder:
    def __init__(self, scheduler: Scheduler):
        self.scheduler = scheduler

    def build(self):
        for house in self.scheduler.community.houses:
            member = Member(house)
            self.scheduler.members.append(member)
