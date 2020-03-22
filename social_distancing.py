from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector

import numpy as np


class PersonAgent(Agent):
    """An agent in our small town that's practicing social distancing"""

    def __init__(self, unique_id, model, pos, speed, heading):
        super().__init__(unique_id, model)
        self.model_space = self.model.space
        self.pos = np.array(pos)
        self.speed = speed
        self.heading = heading
        self.norm_heading = self.heading / np.linalg.norm(self.heading)

    def step(self):
        self.move()

    def move(self):
        new_pos = self.pos + (self.norm_heading * self.speed)
        self.model_space.move_agent(self, new_pos)


class SocialDistanceModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        self.num_agents = N
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = np.array((x, y))
            speed = 5
            heading = np.random.random(2) * 2 - 1
            a = PersonAgent(i, self, pos=pos, speed=speed, heading=heading)
            self.space.place_agent(a, (x, y))
            self.schedule.add(a)

        self.datacollector = DataCollector(
            model_reporters={}, agent_reporters={"pos": "pos"}
        )

    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()
