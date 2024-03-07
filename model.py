from agents import agent
import numpy as np
import mesa

class model(mesa.Model):

    def __init__(self, data):

        super().__init__(self, data)

        self.data = data

        self.interest_rate = data['interest_rate'] # r in the paper

        self.tax = 0
        self.av_pol_view = 0
        self.av_wealth = 0

        self.num_agents = data['agents']
        self.schedule = mesa.time.RandomActivation(self)

        self.first_step = True

############ BEGIN DATA COLLECTOR ##################

        self.datacollector = mesa.DataCollector(
            model_reporters = {
                "n_agents": lambda m: m.schedule.get_agent_count(),
                "tax" : "tax"
             },
            agent_reporters = {
                "wealth" : "wealth",
                "moral_behavior" : "moral_behavior",
                "connectivity" : "connectivity",
                "animal_spirits" : "animal_spirits",
                "political_view" : "political_view",
                "consumption" : "consumed",
                "max_consumption" : "max_consumption",
                "past_wealth" : "past_wealth",
                "gen_skills" : "gen_skills",
                "revenue" : 'revenue'
            }
        )

############ END DATA COLLECTOR ##################

        gen_skills = []
        wealths = []

        for i in range(int(self.num_agents)):
            a = agent(i, self)
            gen_skills.append(a.gen_skills)
            wealths.append(a.wealth)
            self.schedule.add(a)

        max_g_skills = max(gen_skills)

        wealths = sorted(wealths)

        def gen_connect(w, ws, min, max):
            from scipy.stats import percentileofscore

            ps = percentileofscore(ws, w, kind = 'weak')

            bins = range(max - min)
            return min + int(len(bins)*ps/100)


        for a in self.schedule.agents:
            a.gen_skills = np.round(a.gen_skills / max_g_skills * (a.qualities - 1) + 1)
            a.connectivity = gen_connect(a.wealth, wealths, a.min_connectivity, a.max_connectivity)

    def step(self):

        ## get initial data ##
        if self.first_step:
            self.datacollector.collect(self)
            self.first_step = False

        ########################
        ### Now agents move! ###
        ########################
        
        # reset intra period variables for all
        for a in self.schedule.agents:
            a.revenue = 0
            a.consumed = 0

        self.schedule.step()

        ########################
        ########################

        # Update wealth levels with consumption and revenue

        for a in self.schedule.agents:
            a.update_wealth()
            a.update_connectivity()

        # Get average wealth and political views
        # to compute tax
        self.av_pol_view = np.mean([a.political_view for a in self.schedule.agents])
        self.av_wealth = np.mean([a.wealth for a in self.schedule.agents])

        # Compute tax
        u = 0.5
        self.tax = 0.5 * (1 - (np.arctan(u / 2 * self.av_pol_view)) / (np.arctan(u / 2)))

        # Redistribute
        for a in self.schedule.agents:
            a.wealth = a.wealth + self.tax * (self.av_wealth - a.wealth)

        for a in self.schedule.agents:
            a.update_animal_spirits(a.my_friends)
            a.update_moral_behavior(a.my_friends)
            a.update_political_view(a.my_friends)

        self.datacollector.collect(self)