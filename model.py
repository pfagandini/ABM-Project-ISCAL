from agents import agent
import numpy as np
import mesa

class model(mesa.Model):

    def __init__(self, N):

        self.num_agents = N
        self.schedule = mesa.time.RandomActivation(self)

        gen_skills = []

        for i in range(self.num_agents):
            a = agent(i, self)
            gen_skills.append(a.gen_skills)
            self.schedule.add(a)

        max_g_skills = max(gen_skills)

        for a in self.schedule.agents:
            a.gen_skills = np.round(a.gen_skills/max_g_skills * (a.qualities-1)+1)

    def step(self):

        self.schedule.step()