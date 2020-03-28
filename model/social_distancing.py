from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace

from redis.client import Redis
import numpy as np

from typing import Tuple, List, Dict


class SocialDistanceModel(Model):
    """A model with some number of agents."""

    def __init__(
        self,
        db: Redis,
        N: int,
        width: int,
        height: int,
        p_stationary: float = 0.75,
        speed: float = 5,
    ):
        self.db = db
        self.num_agents = N
        self.width, self.height = width, height
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.p_stationary = p_stationary
        self.speed = speed
        self.id = self.get_id_string(
            ["num_agents", "width", "height", "p_stationary", "speed"]
        )

        # Create agents
        for i in range(self.num_agents):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = np.array((x, y))
            heading = np.random.random(2) * 2 - 1
            is_social_distancing = self.random.random() < self.p_stationary
            a = PersonAgent(
                i,
                self,
                pos=pos,
                speed=self.speed,
                heading=heading,
                social_distancing=is_social_distancing,
            )
            if i == 0:
                a.state = "sick"
                a.social_distancing = False
            self.space.place_agent(a, (x, y))
            self.schedule.add(a)

    def get_id_string(
        self, attributes: List[str] = ["num_agents", "width", "height"]
    ) -> str:
        id_str = ",".join((f"{field}={getattr(self, field)}" for field in attributes))
        return id_str

    def step(self):
        """Advance the model by one step."""
        self.save_agent_data()
        self.schedule.step()

    def save_agent_data(self):
        """Saves all agent data to redis"""
        agent_data = (a.collect_data() for a in self.schedule.agents)
        pipe = self.db.pipeline()
        for data in agent_data:
            pipe.xadd(self.id, data)
        pipe.execute()


class PersonAgent(Agent):
    """An agent in our small town that's practicing social distancing"""

    def __init__(
        self,
        unique_id: int,
        model: SocialDistanceModel,
        pos: Tuple[float, float],
        speed: float,
        heading: Tuple[float, float],
        state: str = "healthy",
        social_distancing: bool = False,
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
        # infection radius
        # recovery time

    def step(self) -> None:
        if not self.social_distancing:
            self.move()
        self.recover_check()
        self.infect()

    def move(self) -> None:
        new_pos = self.pos + (self.norm_heading * self.speed)
        self.model_space.move_agent(self, new_pos)

    def recover_check(self) -> None:
        """Check if an agent is in the sick state
        if they are, add 1 to their recovery time counter.

        If they've been sick for 100 steps, they're recovered"""

        if self.state == "sick":
            self.recovery_time += 1
            if self.recovery_time == 100:
                self.state = "recovered"

    def infect(self) -> None:
        if self.state == "sick":
            neighbors = self.model_space.get_neighbors(self.pos, 10)
            if neighbors:
                for n in neighbors:
                    if n.state == "healthy":
                        n.state = "sick"

    def collect_data(self) -> Dict:
        data = {
            "unique_id": self.unique_id,
            "state": self.state,
            "x": self.pos[0],
            "y": self.pos[1],
            "social_distancing": int(self.social_distancing),
            "recovery_time": self.recovery_time,
        }
        return data
