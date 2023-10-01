from agents import agent
import mesa

class model(mesa.Model):

    def __init__(self, N):

        self.num_agents = N
        self.schedule = mesa.time.RandomActivation(self)

        for i in range(self.num_agents):
            a = agent(i, self)
            self.schedule.add(a)

    def step(self):

        self.schedule.step()