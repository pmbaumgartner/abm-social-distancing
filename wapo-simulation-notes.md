# Properties of Simulation

- Agents need to transition between states: healthy, sick, recovered
  - Healthy -> sick when a sick person comes in contact with a healthy person
  - Sick -> Recovered: after some time (t)
  - After recovered, can't be infected again
- Every agent has a starting position and a starting vector
- When agents "touch", if the agent is sick it has to infect a healthy agent.
- Space: width: 800, height: 400
- Agents have a movement speed: How do we figure that out?
- Advanced model: "social distancing" means some agents are stationary
  - 25% continues to move, 75% stationary
  - 12.5% move, 87.5% stationary


## Things that will be different in our model

- Bouncing? 
- Walls? 

## Implementation Notes

- Can we get one agent to move in continuous space?
  - randomly positioned
  - random vector
  - figure out speed?
- Can we display that agent moving for some number of steps?
  - plotly animations: https://plot.ly/python/animations/ 


## Todo
- Review linear algebra / norm 
  - Understand how the movement heading is actually calculated and what each of these steps do
- Add type hints via mypy / refactor
- Fix plotly animation - check out: https://plot.ly/python/animations/#using-a-slider-and-buttons