import numpy as np
from particle_envs.multiagent.core import World, Agent, Landmark
from particle_envs.multiagent.scenario import BaseScenario

class Scenario(BaseScenario):
    def make_world(self):
        world = World()
        # add agents
        world.agents = [Agent() for i in range(1)]
        for i, agent in enumerate(world.agents):
            agent.name = 'agent %d' % i
            agent.collide = False
            agent.silent = True
        # add landmarks
        world.landmarks = [Landmark() for i in range(1)]
        for i, landmark in enumerate(world.landmarks):
            landmark.name = 'landmark %d' % i
            landmark.collide = False
            landmark.movable = False
        # make initial conditions
        self.reset_world(world)
        return world

    def reset_world(self, world):
        # random properties for agents
        for i, agent in enumerate(world.agents):
            agent.color = np.array([0.25,0.25,0.25])
        # random properties for landmarks
        for i, landmark in enumerate(world.landmarks):
            landmark.color = np.array([0.75,0.75,0.75])
        world.landmarks[0].color = np.array([0.75,0.25,0.25])
        # set random initial states
        for agent in world.agents:
            agent.state.p_pos = np.random.uniform(-1,+1, world.dim_p)
            agent.state.p_vel = np.zeros(world.dim_p)
            agent.state.c = np.zeros(world.dim_c)
        for i, landmark in enumerate(world.landmarks):
            # landmark.state.p_pos = np.random.uniform(-1,+1, world.dim_p)
            landmark.state.p_pos = np.array([0,0])
            landmark.state.p_vel = np.zeros(world.dim_p)

    def reward(self, agent, world):
        dist2 = np.sum(np.square(agent.state.p_pos - world.landmarks[0].state.p_pos))
        if dist2 > 0.01:  # If dist^2 is slightly greater than landmark radius(0.05) 
            return -dist2
        else:
            return 2

    def observation(self, agent, world):
        # get positions of all entities in this agent's reference frame
        entity_pos = []
        for entity in world.landmarks:
            entity_pos.append(entity.state.p_pos - agent.state.p_pos)
        return np.concatenate([agent.state.p_vel] + entity_pos)

    def done(self, agent, world):
        # # Return True if total distance of agents from goal  otherwise return False
        # if np.sum(np.square(agent.state.p_pos - world.landmarks[0].state.p_pos)) < 0.7:
        #     return True
        # else:
        #     return False
        if np.any(agent.state.p_pos > 1) or np.any(agent.state.p_pos < -1):
            return True
        else:
            return False
