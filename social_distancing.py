from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector

import numpy as np


class PersonAgent(Agent):
    """An agent in our small town that's practicing social distancing"""

    def __init__(
        self,
        unique_id,
        model,
        pos,
        speed,
        heading,
        state="healthy",
        social_distancing=False,
    ):
        super().__init__(unique_id, model)
        self.model_space = self.model.space
        self.pos = np.array(pos)
        self.speed = speed
        self.heading = heading
        self.norm_heading = self.heading / np.linalg.norm(self.heading)
        self.state = state
        self.recovery_time = 0
        self.social_distancing = social_distancing

    def step(self):
        if not self.social_distancing:
            self.move()
        self.recover_check()
        self.infect()

    def recover_check(self):
        if self.state == "sick":
            self.recovery_time += 1
            if self.recovery_time == 100:
                self.state = "recovered"

    def infect(self):
        if self.state == "sick":
            neighbors = self.model_space.get_neighbors(self.pos, 10)
            if neighbors:
                for n in neighbors:
                    if n.state == "healthy":
                        n.state = "sick"

    def move(self):
        new_pos = self.pos + (self.norm_heading * self.speed)
        self.model_space.move_agent(self, new_pos)


class SocialDistanceModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, social_distancing_p=0.75):
        self.num_agents = N
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.social_distancing_p = social_distancing_p

        # Create agents
        for i in range(self.num_agents):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = np.array((x, y))
            speed = 5
            heading = np.random.random(2) * 2 - 1
            is_social_distancing = self.random.random() < self.social_distancing_p
            if i == 0:
                a = PersonAgent(
                    i,
                    self,
                    pos=pos,
                    speed=speed,
                    heading=heading,
                    state="sick",
                    social_distancing=False,
                )
            else:
                a = PersonAgent(
                    i,
                    self,
                    pos=pos,
                    speed=speed,
                    heading=heading,
                    social_distancing=is_social_distancing,
                )
            self.space.place_agent(a, (x, y))
            self.schedule.add(a)

        self.datacollector = DataCollector(
            model_reporters={
                "n_healthy": n_healthy,
                "n_sick": n_sick,
                "n_recovered": n_recovered,
            },
            agent_reporters={"pos": "pos", "state": "state"},
        )

    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()


def n_healthy(model):
    return len([a for a in model.schedule.agents if a.state == "healthy"])


def n_sick(model):
    return len([a for a in model.schedule.agents if a.state == "sick"])


def n_recovered(model):
    return len([a for a in model.schedule.agents if a.state == "recovered"])
