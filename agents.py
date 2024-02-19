import mesa
import numpy as np
import random
from scipy.stats import pareto, truncnorm

class agent(mesa.Agent):
    
    def __init__(self, unique_id, model):

        super().__init__(unique_id, model)

        inequality_wealth = 2 # parameter for the Pareto distribution, the higher, the higher the inequality

        inequality_skills = 2 # parameter for the Pareto distribution, the higher, the higher the inequality
        weight_gen_skills = 0.5 # theta in the paper

        self.qualities = 10 # Q in the paper
        varieties = 10 # J in the paper

        self.wealth = pareto.rvs(inequality_wealth)

        self.past_wealth = 0

        self.gen_skills = (self.wealth*(1-weight_gen_skills) + pareto.rvs(inequality_skills)*weight_gen_skills)

        self.sp_skills = np.round(np.random.default_rng().uniform(0.5 , varieties + 0.5),0)

        self.pref_low = np.round(np.random.default_rng().uniform(0.5 , varieties + 0.5),0)

        self.pref_high = np.round(np.random.default_rng().uniform(0.5 + self.pref_low , varieties + 0.5),0)

        self.min_connectivity = 1 # This is the N^0 of the paper
        self.max_connectivity = self.model.num_agents # This is the \tilde{N} of the paper. Note that it must be fixed to \tilde{N}-1, as I am not sure a link to myself would make sense

        self.connectivity = max(min(np.round(pareto.cdf(self.wealth, inequality_wealth)*self.model.num_agents),self.max_connectivity),self.min_connectivity) # As a number, the cumulative probability (between 0 and 1, wealthier -> larger)

        self.animal_spirits = truncnorm.rvs(-1,1)

        self.moral_behavior = truncnorm.rvs(-1,1)

        self.political_view = truncnorm.rvs(-1,1)

        self.max_consumption = 0
        self.consumed = 0
        self.revenue = 0

        a = 1 # a in the paper
        alpha = 1 # alpha in the paper

        self.price = a * self.gen_skills ** alpha

    def update_consumption(self):
        self.max_consumption = self.wealth * self.propensity_to_consume()

    def update_connectivity(self):
        w = 0.5 # w in the paper
        b = 0.5 # b in the paper
        self.connectivity = self.connectivity + np.round((w * (self.wealth - self.past_wealth) + b * self.moral_behavior ) * self.connectivity)

        if self.connectivity > self.model.num_agents:
            self.connectivity = self.model.num_agents - 1

        elif self.connectivity < 1:
            self.connectivity = 1   

    def update_animal_spirits(self, friends):

        def gamma(x):
            ga = 0.5 # gamma constant in the paper
            if x < 0:
                return -ga * (1+x)
            elif x == 0 :
                return 0
            else:
                return ga * (1-x)
        
        g = 0.5 # g constant in the paper

        Am_temp = []

        for a in friends:
            Am_temp.append(a.animal_spirits)

        Am = np.mean(Am_temp)

        self.animal_spirits = self.animal_spirits + g * (Am - self.animal_spirits) + gamma(self.animal_spirits)

    def propensity_to_consume(self):
        c_l = 0.1 # paper's c_l
        c_h = 0.9 # paper's c_h

        a = 0.5 # a in the paper

        to_return = 0.5*((c_h + c_l)+(c_h - c_l)*(np.arctan(a/2*self.animal_spirits))/(np.arctan(a/2)))
        return to_return

    def update_moral_behavior(self, friends):

        z = 0.5 # constant z in the paper
        
        def zeta(x):
            zet = 0.5 # constant greez zeta in the paper

            if x < 0 :
                return -zet * (1+x)
            elif x == 0:
                return 0
            else:
                return zet * (1-x)
                
        Bm_temp = []

        for a in friends:
            Bm_temp.append(a.moral_behavior)

        Bm = np.mean(Bm_temp)

        self.moral_behavior = self.moral_behavior + z*(Bm-self.moral_behavior) + zeta(self.moral_behavior)

    def update_political_view(self, friends):

        x = 0.5 # constant x in the paper

        def omega(x):
            ome = 0.5
            if x == 0:
                return 0
            if x < 0:
                return - ome * (1+x)
            else:
                return ome * (1-x)

        Xm_temp = []

        for a in friends:
            Xm_temp.append(a.political_view)

        Xm = np.mean(Xm_temp)

        self.political_view = self.political_view + x*(Xm-self.political_view) + omega(self.political_view)

        return 0

    def update_wealth(self):
        
        new_wealth = self.revenue + self.wealth * (1 + self.model.interest_rate) - self.consumed
        self.past_wealth = self.wealth
        self.wealth = new_wealth
        self.consumed = 0
        self.update_consumption()

    def get_friends(self):
        
        agents_to_interact = []
        aux_agents = []

        for ag in self.model.schedule.agents:
            if ag != self:
                aux_agents.append(ag)
        
        my_agents_list = aux_agents.copy()
        random.shuffle(my_agents_list)
        agents_to_interact = my_agents_list[0 : max(int(self.connectivity), len(my_agents_list))]

        return agents_to_interact

    def step(self):

        my_agents_list = self.get_friends()

        self.update_animal_spirits(my_agents_list)
        self.update_political_view(my_agents_list)
        self.update_moral_behavior(my_agents_list)

        self.update_wealth()

        random.shuffle(my_agents_list)
        agents_to_interact = my_agents_list[0:max(int(self.connectivity), len(my_agents_list))]
        
        agents_to_interact.sort(key = lambda x: x.connectivity, reverse = True)
        self.max_consumption = self.propensity_to_consume() * self.wealth

        for a in agents_to_interact:
            if (self.max_consumption - self.consumed > a.price) and (a.sp_skills >= self.pref_low) and (a.sp_skills <= self.pref_high):
                self.consumed = self.consumed + a.price
                a.wealth = a.wealth + a.price

        self.wealth = self.wealth - self.consumed