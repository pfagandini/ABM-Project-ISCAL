from agents import agent
import numpy as np
import mesa

class model(mesa.Model):

    def __init__(self, N):

        self.tax = 0
        self.av_pol_view = 0
        self.av_wealth = 0

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

        self.datacollector = mesa.DataCollector(
            agent_reporters = {'Wealth':'wealth'}
        )

    def step(self):

        self.schedule.step()

        # Get average wealth and political views
        pol_views = []
        wealth = []

        for a in  self.schedule.agents:
            pol_views.append(a.political_view)
            wealth.append(a.wealth)

        self.av_pol_view = np.mean(pol_views)
        self.av_wealth = np.mean(wealth)

        # Compute tax
        u = 0.5
        self.tax = 0.5*(1-(np.arctan(u/2*self.av_pol_view))/(np.arctan(u/2)))

        # Redistribute
        for a in self.schedule.agents:
            a.wealth = a.wealth + self.tax * (self.av_wealth - a.wealth)